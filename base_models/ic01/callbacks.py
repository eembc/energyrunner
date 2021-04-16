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
        self.best = 0

    def on_epoch_end(self, epoch, logs=None):
        # Check the accuracy and update if it's the best
        current = logs.get("val_accuracy")
        if np.less(self.best, current):
            print(f"Epoch={epoch+1}, accuracy={current:.4f}, setting weights")
            self.best = current
            self.best_weights = self.model.get_weights()

    def on_train_end(self, logs=None):
        # Set the weights to be the best recorded set
        self.model.set_weights(self.best_weights)
