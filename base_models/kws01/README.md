# Model

* Name: Keyword Spotting v0.1
* Code: `kws01`
* Base: KWS10_ARM_DSConv

# Sources
* Dataset
    * [http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz](http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz)
* Model Topology
    * [https://arxiv.org/pdf/1711.07128.pdf](https://arxiv.org/pdf/1711.07128.pdf)
    * [https://github.com/ARM-software/ML-KWS-for-MCU](https://github.com/ARM-software/ML-KWS-for-MCU)
* Spectrogram Characteristics
    * Front-end: [https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/experimental/microfrontend](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/experimental/microfrontend)
    * Configuration: window=30ms, stride=20ms, bins=10, Upper frequency limit=4KHz

# Performance (floating point model)
* Accuracy
    * 94.3%
* AUC
    * .998

# Performance (quantized tflite model)
* Accuracy
    * 94.3%
* AUC
    * .997