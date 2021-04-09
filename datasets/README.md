# File Specifics

| Model | Source            | Dimensions  | Min Accuracy  | File Format                                  | # Stimuli |
| ----- | --------          | ----------  | ------------- | ----------------------                       | --------- |
| vww01 | COCO2014/val2017  | 96x96       | 80%           | U8C3, RGB, where [0]=ulc and [9215]=lrc      | 500 true, 500 false|
| ic01  | CIFAR-10          | 32x32       | 86%           | U8C3, RGB, where [0]=ulc and [1024]=lrc; this is different from original CiFAR-10 array which is 1024R, 1024G, 1024B | 250, 10 classes |
| ad01  | ToyADMOS/car      | n/a         | AUC: 0.86     | Spectrogram, 200 slices, 128 samples, FP32LE | 108 anomaly, 140 normal |
| kws01 | Tensforlow        | n/a         | 90%           | Spectrogram, 49 frames x 10 MFCCs as INT8    | 1000, 12 classes |

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
