# Model

* Name: Image Classification v0.1
* Code: `ic01`
* Base: CIFAR10_ResNetv1

# Sources
* Dataset
    * [https://www.cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html)
* Model Topology
    * [https://arxiv.org/pdf/1512.03385.pdf](https://arxiv.org/pdf/1512.03385.pdf)
    * [https://keras.io/api/applications/resnet/](https://keras.io/api/applications/resnet/)

# Required software packages
- Python [3.7.x or 3.8.x](https://www.python.org/downloads/)

# To run the code
To simply train and test, do the following:
```
cd <git repo root>/eembc/CIFAR10_ResNetv1
# Create virtual environment
python -m venv venv
# Activate virtual environment (Linux)
source ./venv/bin/activate (Linux)
# Activate virtual environment (Windows)
.\venv\Scripts\activate (Windows)
# Install python dependencies
pip install -r requirements.txt
# Run training and evaluation script
python cifar10_main.py
```
The code will train the network and show the training history. Then it will test with the validation data and show accuracy, AUC and confusion matrix.
Type `python cifar10_main.py --help` to see all available options.

# Training details

## Optimizer
The optimizer is Adam with default options.
```python
#optimizer
optimizer = tf.keras.optimizers.Adam()
```

## Learning rate
We start with rate of .001 and follow an exponential decay
``` python
#learning rate schedule
def lr_schedule(epoch):
    initial_learning_rate = 0.001
    decay_per_epoch = 0.99
    lrate = initial_learning_rate * (decay_per_epoch ** epoch)
    print(f"Learning rate = {lrate:.5f}")
    return lrate
```
For code reference see [`callbacks.py`](./callbacks.py).

## Augmentation
```python
#define data generator
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    #brightness_range=(0.9, 1.2),
    #contrast_range=(0.9, 1.2)
)
```
For the code reference see [`cifar10_main.py`](./cifar10_main.py#L86).

# Performance (floating point model)
* Accuracy
    * 86.2%
* AUC
    * .989

# Performance (quantized tflite model)
* Accuracy
    * 86.1%
* AUC
    * .988