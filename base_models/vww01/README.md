# Model

* Name: Visual Wake Word v0.1
* Code: `vww01`
* Base: Person_detection

# Sources
* Dataset
    * MSCOCO14 based [https://cocodataset.org/#download]
    * Extraction based on COCO API [https://github.com/cocodataset/cocoapi]
    * Person minimal bounding box 2.5%
    * 96x96 images resized with antialias filtering, no aspect ratio preservation
    * All images converted to RGB
    * Training and validation sets combined
    * Dataset generation script (buildPersonDetectionDatabase.py) is included in repo
* Extracted Reference Dataset
   * [vw_coco2014_96.tar.gz](https://www.silabs.com/public/files/github/machine_learning/benchmarks/datasets/vw_coco2014_96.tar.gz)
* Model Topology
    * Based on [https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet_v1.md)
        * Chosen configuration is a MobileNet_v1_0.25_96

# Training details
``` python
#learning rate schedule
epochs = 50
def lr_schedule(epoch):
    lrate = 0.001
    if epoch > 20:
        lrate = 0.0005
    if epoch > 30:
        lrate = 0.00025
    return lrate

#optimizer
optimizer = tf.keras.optimizers.Adam()
batch_size = 50
validation_split = 0.1

#define data generator
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=.1,
    horizontal_flip=True,
    validation_split=validation_split
)
```

# Performance (floating point model)
* Accuracy
    * 85.4%
* AUC
    * .931

# Performance (quantized tflite model)
* Accuracy
    * 85.0%
* AUC
    * .928