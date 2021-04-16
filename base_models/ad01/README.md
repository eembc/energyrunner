# Model

* Name: Anomaly Detection v0.1
* Code: `ad01`
* Base: ToyADMOS_FC_AE

# Sources
* Dataset
    * [https://zenodo.org/record/3351307](https://zenodo.org/record/3351307)
    * See https://arxiv.org/pdf/1908.03299.pdf for details. Individual patterns were downloaded and used - page 2, figure 2.
    * We have trained and tested the model with the toy car data, case 1 only. Code may be modified for more cases.
    * By default the dataset is assumed to be located in `./ToyAdmos`.
* Model Topology
    * [http://dcase.community/challenge2020/task-unsupervised-detection-of-anomalous-sounds](http://dcase.community/challenge2020/task-unsupervised-detection-of-anomalous-sounds)
    * [https://github.com/y-kawagu/dcase2020_task2_baseline](https://github.com/y-kawagu/dcase2020_task2_baseline)
* Spectrogram Characteristics
    * Front-end: [LIBROSA spectrogram](https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html) is what is used in the code, but we have also tested with [https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/experimental/microfrontend](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/experimental/microfrontend)
    * Configuration: window=64ms, stride=32ms, bins=128, Upper frequency limit=24KHz, use only 5 center time windows

# Required software packages
- Python [3.7.x or 3.8.x](https://www.python.org/downloads/)

# To run the code
To simply train and test, do the following:
```
cd <git repo root>/eembc/ToyADMOS_FC_AE
# Create virtual environment
python -m venv venv
# Activate virtual environment (Linux)
source ./venv/bin/activate (Linux)
# Activate virtual environment (Windows)
.\venv\Scripts\activate (Windows)
# Install python dependencies
pip install -r requirements.txt
# Run training and evaluation script
python toyadmos_autoencoder_main.py
```
The code will train the network and show the training history. Then it will test with the validation data and show accuracy and AUC.
Type `python toyadmos_autoencoder_main.py --help` to see all available options.

# Performance (floating point model)
* Accuracy
    * 92.0%
* AUC
    * .923

# Performance (quantized tflite model)
* Accuracy
    * 91.5%
* AUC
    * .923