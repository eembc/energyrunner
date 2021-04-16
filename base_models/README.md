# Overview
This repo is intended for hosting open-source models for general and benchmarking use. All models are presented in the `tensorflow.keras` API and intended to run in TensorFlow

## Model Genealogy
There are three main categories of genealogy:

* Models generated from scratch by SiLabs ML R&D
* Models derived from common open-source/public architectures such as MobileNets, ResNets
* Open-source models which have been ported from either textual or non-standard formats into a `tensorflow.keras` representation

## Directory Structure & Licenses
Due to the diversity in genealogy of models, each model is placed in a separate directory with its appropriate `LICENSE.md` file. It is the intent that all models are derived from and/or released as non-viral licenses such as MIT or Apache 2.0

# Naming Convention

Both EEMBC's ULPMark-ML and MLCommon's tinyMLPerf use these models. You will often see them referred to by codenames:

| Code Name | Description |
| --------- | ----------- |
| ad01      | Anomaly Detection |
| ic01      | Image Classification |
| kws01     | Key-word Spotting |
| vww01     | Visual wake word, aka person detection |

See each models' README file for links to the model paper, repositories, training methodology, etc.
