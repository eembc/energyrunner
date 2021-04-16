# Import all modules
import numpy as np
import tensorflow as tf

# Learning rate schedule
def lr_schedule(epoch):
    initial_learning_rate = 0.001
    decay_per_epoch = 0.99
    lrate = initial_learning_rate * (decay_per_epoch ** epoch)
    print(f"Learning rate = {lrate:.5f}")
    return lrate

# Class for all training callbacks, used to select the best weights
class TrainingCallbacks(tf.keras.callbacks.Callback):
    def __init__(self):
        super(TrainingCallbacks, self).__init__()
        # best_weights to store the weights at which the maximum accuracy occurs.
        self.best_weights = None

    def on_train_begin(self, logs=None):
        # Initialize the best as zero.
        self.best = np.inf

    def on_epoch_end(self, epoch, logs=None):
        # Check the accuracy and update if it's the best
        current = logs.get("val_mean_squared_error")
        if np.less(current, self.best):
            print(f"Epoch={epoch+1}, mse={current:.4f}, setting weights")
            self.best = current
            self.best_weights = self.model.get_weights()

    def on_train_end(self, logs=None):
        # Set the weights to be the best recorded set
        self.model.set_weights(self.best_weights)

# Class to control how we present training data
class TrainingSequence(tf.keras.utils.Sequence):
    def __init__(self, x, batch_size, is_training=True, window=5):
        super(TrainingSequence, self).__init__()
        self.x = x
        self.batch_size = batch_size
        self.is_training = is_training
        self.window = window
        self.shape = int(self.batch_size*np.floor(len(self.x) / self.batch_size))

    def __len__(self):
        return int(np.floor(len(self.x) / self.batch_size))

    def on_epoch_end(self):
        # DO nothing, we may shuffle if need be
        pass

    def __getitem__(self, idx):
        if self.is_training:
            start = np.random.randint(50, self.x.shape[1]-100 )
        else:
            start = int(self.x.shape[1]/2)
        batch_x = self.x[idx * self.batch_size:(idx + 1) * self.batch_size,start:start+self.window]

        #breakpoint()
        #print(f"__getitem__, idx={idx}")
        return batch_x, batch_x