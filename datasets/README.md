# File Specifics

| Model | Source       | Dimensions | File Format                                               | # Stimuli |
| ----- | --------     | ---------- | -----------------------------------                       | --------- |
| vww01 | COCO2014     | 96x96      | Flat array of U8C3, RGB, where [0]=ulc and [9215]=lrc     | 1000; 500 true, 500 false, val2017 |
| ic01  | CIFAR-10     | 32x32      | Location 0 is upper-left, location 3071 is lower right, data is U8C3x1024; this is different from original CiFAR-10 array which is 1024R, 1024G, 1024B    | 50 from test set       |
| ad01  | ToyADMOS/car | tbd        | Spectrogram, 200 slices, 128 samples, FP32, little-endian | 11 anomoly, 11 normal       |
| kws01 | Tensforlow Speech Commands   | tbd        | Spectrogram, 49 frames x 10 MFCCs as INT8                 | 50, 12 classes |

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
