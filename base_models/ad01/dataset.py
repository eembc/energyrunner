import os
import numpy as np
import matplotlib.pyplot as plt

from librosa import load
from librosa.feature import melspectrogram

# Wrapper to load wav file and generate spectrogram with log10 scaling
def spectrogram_l(wav_file, hop_length, win_length, n_mels):
    y, sr = load(wav_file, sr=None, mono=True, dtype='float32')
    n_fft = 2**np.ceil(np.log2(win_length))
    S = melspectrogram(y=y, sr=sr, n_fft=4096, hop_length=hop_length, win_length=win_length, n_mels=n_mels)
    return np.log10(S+1e-6).transpose()

def load_dataset(base_dir, model, cases, log_dir, validation_split, do_extraction, seed):
    # Spectrogram parameters, fixed
    hop_length = 1536
    win_length = 3072
    n_mels = 128

    # First step is to ge the number of all cases
    normal_len = 0
    anomalous_len = 0
    for case in cases:
        normal_dir = f"{base_dir}/{model}/case{case}/NormalSound_IND"
        normal_len += len(os.listdir(normal_dir))
        anomalous_dir = f"{base_dir}/{model}/case{case}/AnomalousSound_IND"
        anomalous_len += len(os.listdir(anomalous_dir))

    # Now peek and get one normal and anomalous case
    S_normal = spectrogram_l(f"{normal_dir}/{os.listdir(normal_dir)[0]}", hop_length, win_length, n_mels)
    S_anomalous = spectrogram_l(f"{anomalous_dir}/{os.listdir(anomalous_dir)[0]}", hop_length, win_length, n_mels)

    # Display the spectrograms
    fig = plt.figure()
    plt.suptitle(f"LIBROSA {model} spectrograms")

    ax = fig.add_subplot(2,1,1)
    plt.imshow(S_normal.transpose())
    plt.text(.5,.5,f"{os.listdir(normal_dir)[0]}", 
        horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        bbox=dict(edgecolor='gray', fill=False))
    plt.ylabel('frequency')
    plt.show(block=False)

    ax = fig.add_subplot(2,1,2)
    plt.imshow(S_anomalous.transpose())
    plt.text(.5,.5,f"{os.listdir(anomalous_dir)[0]}", 
        horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
        bbox=dict(edgecolor='gray', fill=False))
    plt.xlabel('time')
    plt.ylabel('frequency')
    plt.show(block=False)
    plt.pause(0.1)

    spectrograms_file_name = f"{log_dir}/spectrograms.npz"
    if do_extraction | (not os.path.exists(spectrograms_file_name)):
        # Allocate buffers
        X_normal = np.zeros((normal_len, S_normal.shape[0], S_normal.shape[1],1), dtype=np.float32)
        X_anomalous = np.zeros((anomalous_len, S_anomalous.shape[0], S_anomalous.shape[1],1), dtype=np.float32)

        # Loop and load
        normal_counter, anomalous_counter = 0, 0
        for case in cases:
            print(f"Extracting normal spectrograms for {model}, case{case}")
            normal_dir = f"{base_dir}/{model}/case{case}/NormalSound_IND"
            for file in os.listdir(normal_dir):
                X_normal[normal_counter,:,:,0] = spectrogram_l(f"{normal_dir}/{file}", hop_length, win_length, n_mels)
                normal_counter += 1

            print(f"Extracting anomalous spectrograms for {model}, case{case}")
            anomalous_dir = f"{base_dir}/{model}/case{case}/AnomalousSound_IND"
            for file in os.listdir(anomalous_dir):
                X_anomalous[anomalous_counter,:,:,0] = spectrogram_l(f"{anomalous_dir}/{file}", hop_length, win_length, n_mels)
                anomalous_counter += 1

        # Normalize and scale in the int8 range
        mmin = X_normal.min()
        mmax = X_normal.max()
        X_normal = (X_normal-mmin)/(mmax-mmin)
        X_normal = 255*X_normal-128
        X_anomalous = (X_anomalous-mmin)/(mmax-mmin)
        X_anomalous = 255*X_anomalous-128

        # Split X_normal into training and validation, seeded for reproducible results
        np.random.seed(seed=seed)
        indexes = np.arange(len(X_normal))
        np.random.shuffle(indexes)
        validation_limit = int(validation_split*len(indexes))
        X_normal_train = X_normal[indexes[validation_limit:]]
        X_normal_val = X_normal[indexes[0:validation_limit]]

        # Save dataset
        np.savez(spectrograms_file_name, a=X_normal_train, b=X_normal_val, c=X_anomalous)
    else:
        # Load dataset
        with np.load(spectrograms_file_name) as data:
            X_normal_train = data['a']
            X_normal_val = data['b']
            X_anomalous = data['c']

    return X_normal_train, X_normal_val, X_anomalous 
