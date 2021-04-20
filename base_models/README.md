# Overview

This folder contains the models used by ULPMark-ML and MLCommons tinyMLPerf. The baseline Keras models were created by EEMBC and trained by MLCommons. The actual training process and scripts for each model are stored in the [tinyMLPerf training repository](https://github.com/mlcommons/tiny).

Both groups agreed to starting points that contain pre-trained, pre-quantized INT8 models. To prevent mixups, each official INT8 model has an MD5 sum associated with it.

This repo is intended for hosting open-source models for general and benchmarking use. All models are presented in the `tensorflow.keras` API and intended to run in TensorFlow.

# Model Genealogy

There are three main categories of genealogy:

* Models generated from scratch by SiLabs ML R&D
* Models derived from common open-source/public architectures such as MobileNets, ResNets
* Open-source models which have been ported from either textual or non-standard formats into a `tensorflow.keras` representation

# Directory Structure & Licenses

Due to the diversity in genealogy of models, each model is placed in a separate directory with its appropriate `LICENSE.md` file. It is the intent that all models are derived from and/or released as non-viral licenses such as MIT or Apache 2.0

# Naming Convention

Both EEMBC's ULPMark-ML and MLCommon's tinyMLPerf use these models. You will often see them referred to by codenames:

| Code Name | Description |
| --------- | ----------- |
| ad01      | Anomaly Detection |
| ic01      | Image Classification |
| kws01     | Keyword Spotting |
| vww01     | Visual wake word, aka person detection |

See each models' README file for links to the model paper, repositories, training methodology, etc.
