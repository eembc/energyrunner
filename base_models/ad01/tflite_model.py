# Import all modules
import numpy as np
import tensorflow as tf
import time

# Class for all tflite support
class TfliteModel():
    def __init__(self, model=None, datagen_flow=None):
        self.model = model
        self.datagen_flow = datagen_flow

    # Callback to quantize based on training dataset
    def representative_dataset(self):
        sample_count = 0
        done = False
        for batch, _ in self.datagen_flow:
            if done: 
                break 
            for sample in batch:
                if done: 
                    break 
                sample_count += 1
                if sample_count > 1000:
                    done = True 
                yield [np.expand_dims(sample, axis=0)]

    # Convert main FP model to quantized tflite model
    def convert(self):
        # Convert and save tflite model
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = self.representative_dataset
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8  # or tf.uint8
        converter.inference_output_type = tf.int8  # or tf.uint8
        self.tflite_flatbuffer_data = converter.convert()

    # Save tflite model to file
    def save(self, file):
        with open(file, 'wb') as f:
            f.write(self.tflite_flatbuffer_data)

    # Load tflite model from file
    def load(self, file):
        self.interpreter = tf.lite.Interpreter(model_path=file)

    # Prediction on some test set data
    def predict(self, x_test, batch_size=1):
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Get quantization details, necessary for proper input/output scaling and offset (zero point)
        input_scaler, input_zero_point = input_details[0]['quantization']
        output_scaler, output_zero_point = output_details[0]['quantization']

        # Allocate the output vector
        y_pred = np.zeros(np.append(x_test.x.shape[0],output_details[0]['shape'][1:]),dtype='float32')

        # Infer on all test data.
        text = "{index:4d}/{ll:4d} "
        bar_n = 30
        print('\n'+text.format(index=0,ll=int(len(x_test)/batch_size))+ '[' + '>' + '.'*bar_n + ']', end='', flush=True)
        t = time.time()
        for i in range(len(x_test)):
            # Get input data (in correct INT8 range)
            input_data, _ = x_test[i]

            for j in range(len(input_data)):

                # Get data and apply optimal quantization
                scaled_input = (input_data[j] / input_scaler) + input_zero_point
                self.interpreter.set_tensor(input_details[0]['index'], scaled_input[np.newaxis].astype('int8'))

                # Run model on data
                self.interpreter.invoke()

                # The function `get_tensor()` returns a copy of the tensor data.
                # Use `tensor()` in order to get a pointer to the tensor.
                output_data = self.interpreter.get_tensor(output_details[0]['index'])
                y_pred[j+i*len(input_data)] = output_data.astype('float32')

                # Update display
                index = i+1
                if( (index % batch_size) == 0 ):
                    elapsed = time.time() - t
                    step = elapsed*batch_size/index
                    if( (len(x_test)-index) < batch_size ):
                        eta = 'elapsed: '+str(int(elapsed))+'s'
                    else:
                        eta = 'ETA: '+str(int(step*(len(x_test)-index)/batch_size))+'s   '
                    eq_n = int(index*bar_n/len(x_test))
                    dot_n = bar_n-eq_n
                    print('\r' + text.format(index=int(index/batch_size),ll=int(len(x_test)/batch_size)) + '[' + '='*eq_n + '>' + '.'*dot_n + '] - '+eta, end='', flush=True)

        print('\n')

        # Scale to right quantization
        return (y_pred - output_zero_point) * output_scaler

