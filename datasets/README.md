# File Specifics

| Model | Source       | Dimensions | File Format                                               | # Stimuli |
| ----- | --------     | ---------- | -----------------------------------                       | --------- |
| vww01 | COCO2014     | 96x96      | Flat array of U8C3, RGB, where [0]=ulc and [9215]=lrc     | 1000; 500 true, 500 false, val2017 |
| ic01  | CIFAR-10     | 32x32      | 1024 R, 1024 G, 1024 B; [0]=ulc and [1023]=lrc            | 50 from test set       |
| ad01  | ToyADMOS/car | tbd        | Spectrogram, 200 slices, 128 samples, FP32, little-endian | 25 anomoly, 25 normal       |
| aww01 | tbd          | tbd        | tbd                                                       | tbd       |
