# Import all modules
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import argparse
import csv

from distutils.util import strtobool

from tensorflow.keras.callbacks import LearningRateScheduler

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import sys
sys.path.append('../Methodology/')
from eval_functions_eembc import calculate_accuracy, calculate_auc, calculate_cm
from resnet_v1_eembc import resnet_v1_eembc
from tflite_model import TfliteModel
from callbacks import lr_schedule, TrainingCallbacks



def main():
    # Parse the args
    parser = argparse.ArgumentParser(description='This script evaluates an classification model')
    parser.add_argument("--training", '-t', default='True', help='Determines whether to run the training phase or just infer')
    parser.add_argument("--lite", '-l', default='False', help='Determines whether to use the the tflite or floating point model')
    parser.add_argument("--epochs", '-e', default='100', help='Number of epochs to run')
    args = parser.parse_args()

    try:
        do_training = bool(strtobool(args.training))
    except ValueError:
        do_training = True

    try:
        use_tflite_model = bool(strtobool(args.lite))
    except ValueError:
        use_tflite_model = False

    # Training parameters
    name = "resnet_v1_eembc"
    epochs = int(args.epochs)
    batch_size = 40
    log_dir = 'log_cifar10'

    # Dataset parameters
    classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    # Get data
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # Plot some for reference
    fig = plt.figure(figsize=(8,3))
    for i in range(len(classes)):
        ax = fig.add_subplot(2, 5, 1 + i, xticks=[], yticks=[])
        idx = np.where(y_train[:]==i)[0]
        features_idx = x_train[idx,::]
        img_num = np.random.randint(features_idx.shape[0])
        im = features_idx[img_num,::]
        ax.set_title(classes[i])
        plt.imshow(im)
    plt.show(block=False)
    plt.pause(0.1)    

    # Convert for training
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # Scale to INT8 range (simple non-adaptive)
    x_train = (x_train-128)/128
    x_test = (x_test-128)/128

    y_train = to_categorical(y_train,len(classes))
    y_test = to_categorical(y_test,len(classes))
    
    init_gpus()

    # Optimizer
    optimizer = tf.keras.optimizers.Adam()

    # Build model
    model = resnet_v1_eembc()
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.summary()

    # Augmentation
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        #brightness_range=(0.9, 1.2),
        #contrast_range=(0.9, 1.2)
    )
    datagen.fit(x_train)
    datagen_flow = datagen.flow(x_train, y_train, batch_size=batch_size)

    # Train model
    if( do_training ):
        callbacks = [LearningRateScheduler(lr_schedule), TrainingCallbacks()]
        model_t = model.fit(datagen_flow, epochs=epochs, validation_data=(x_test,y_test), callbacks=callbacks)

        # Plot training results
        plt.figure()
        plt.plot(model_t.history['accuracy'],'r')
        plt.plot(model_t.history['val_accuracy'],'g')
        plt.xticks(np.arange(0, epochs+1, 2.0))
        plt.rcParams['figure.figsize'] = (8, 6)
        plt.xlabel("Num of Epochs")
        plt.ylabel("Accuracy")
        plt.title("Training Accuracy vs Validation Accuracy")
        plt.legend(['train','validation'])
       
        plt.figure()
        plt.plot(model_t.history['loss'],'r')
        plt.plot(model_t.history['val_loss'],'g')
        plt.xticks(np.arange(0, epochs+1, 2.0))
        plt.rcParams['figure.figsize'] = (8, 6)
        plt.xlabel("Num of Epochs")
        plt.ylabel("Loss")
        plt.title("Training Loss vs Validation Loss")
        plt.legend(['train','validation'])
        
        plt.show(block=False)
        plt.pause(0.1)  
        
        # Save the weights
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        model.save_weights(log_dir + '/weights.hdf5')

        # Convert and save tflite model
        tflite_model = TfliteModel(model, datagen_flow)
        tflite_model.convert()
        tflite_model.save(log_dir + '/model.tflite')
      
    # Load and evaluate the quantized tflite model
    if( use_tflite_model ):
        tflite_model = TfliteModel()
        tflite_model.load(log_dir + '/model.tflite')
        y_pred = tflite_model.predict(x_test, batch_size)
    # Or else normal model
    else:
        model.load_weights(log_dir + '/weights.hdf5')
        y_pred = model.predict(x_test, verbose=1)

    # Accuracy and AUC metrics
    y_labels = np.argmax(y_test,axis=1)
    calculate_accuracy(y_pred, y_labels) 
    calculate_auc(y_pred, y_labels, classes, name)

    # Confusion matrix
    calculate_cm(y_pred, y_labels, classes, name)

    np.savetxt(log_dir + '/y_labels.csv', y_labels, delimiter=',',fmt='%2d')
    np.savetxt(log_dir + '/y_pred.csv', y_pred, delimiter=',',fmt='%.5f')
    with open(log_dir + '/classes.csv','w') as class_file:
        wr = csv.writer(class_file, dialect='excel')
        wr.writerows([classes])

    input('Press CTRL+C to exit')
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


def init_gpus():
    # Enable dynamic memory growth for GPUs
    # This works around potential issues on Windows
    try:
        tf_gpus = tf.config.list_physical_devices('GPU')
        for gpu in tf_gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except:
        pass


def tensorflow_import_error_workaround():
    """This works around an exception generated during TF-Lite conversion:
    "module 'tensorflow.lite.python.schema_py_generated' has no attribute 'Model'"
    The issue in Tensorflow 2.4 because:
    tensorflow.lite.python.schema_py_generated is empty.
    This work-around simply copies from tensorflow_lite_support.metadata.schema_py_generated
    to  tensorflow.lite.python.schema_py_generated  and reloads the module
    """
    # pylint: disable=import-outside-toplevel
    import importlib
    from tensorflow.lite.python import schema_py_generated as _tf_schema_fb
    import tensorflow_lite_support.metadata.schema_py_generated as _tflite_schema_fb

    if os.path.getsize(_tf_schema_fb.__file__) == 0:
        with open(_tflite_schema_fb.__file__, 'r') as src:
            with open(_tf_schema_fb.__file__, 'w') as dst:
                dst.write(src.read())
        importlib.reload(_tf_schema_fb)


if __name__ == '__main__':
    tensorflow_import_error_workaround()
    main()
   