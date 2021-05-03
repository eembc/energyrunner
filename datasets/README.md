# File Specifics

| Model | Source             | Dimensions  | Min Accuracy  | File Format                                   | # Stimuli |
| ----- | --------           | ----------  | ------------- | ----------------------                        | --------- |
| vww01 | COCO2014/val2017   | 96x96       | 80%           | U8C3, RGB, where [0]=ulc and [9215]=lrc       | 500 true, 500 false|
| ic01  | CIFAR-10           | 32x32       | 85%           | U8C3, RGB, where [0]=ulc and [1024]=lrc; this is different from original CiFAR-10 array which is 1024R, 1024G, 1024B | 200, 10 classes |
| ad01  | ToyADMOS/car       | n/a         | AUC: 0.85     | Spectrogram, 5 slices, 128 freq. bins, FP32LE | 108 anomaly, 140 normal |
| kws01 | Speech Commands v2 | n/a         | 90%           | Spectrogram, 49 frames x 10 MFCCs as INT8     | 1000 features, 12 classes |

# Ground Truth Format

For everything but anomaly detection, the y_labels.csv file format is:

```
input file name,total number of classes,predicted class number
```

For anomaly datection, the y_labels.csv file format specifies a sliding window for the input file

```
input file name,total number of classes,predicted classes,window width (bytes),stride (bytes)
```

Where number of classes is always 2 (anomaly, normal), and 0=normal, 1=anomaly.

# KWS open division

For this release of the benchmark, the tinyMLPerf "open" division allows the use of three other additional formats, which can be found in the `kws-open` folder. It is up to the user to copy the files from the `kws-open` folder to the `kws01` folder, the runner will not automatically do this.
