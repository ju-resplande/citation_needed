# Citation_Needed
Code for outreatchy Wikimedia project.

## Installation 

1. Download run_citation_need_model.py from [this version](https://github.com/mirrys/citation-needed-paper/tree/ef16de6c6165978a55b1bc0a6ba6c9ddc82e0d87).
2. Download section and language dictionaries and models from the same repository and rename as "models/model.h5", "dicts/word_dict.pck" and  "dicts/section_dict.pck".
3. Download requirements.

# Observation
[Miniconda](https://docs.conda.io/en/latest/miniconda.html) enviroment was used install the requirements, but [Tensowflow Custom Build](https://github.com/lakshayg/tensorflow-build) was also used (TensorFlow 1.6.0 Ubuntu 16.04) due to "Your CPU supports instructions that this TensorFlow binary was not compiled to use" error. Perheaps, "outreatchy.yml" won't work in your device.

### System Requirements

* python 2.7
* keras 2.1.5
* tensorflow 1.6.0 or 1.7.0
* sklearn 0.18.1
* pandas
* nltk
* requests
* mwparserfromwell
* h5py

## Usage

1. Run all_action.py and insert a page name (case sensite). 

It will generate in output_folder:

* table.txt - used by run_citation_need_model.py
* need_citation.txt - needs citation sentence list 
