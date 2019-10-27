# Citation-Needed

## Installation 

 Use [miniconda](https://docs.conda.io/en/latest/miniconda.html) (or conda but its heavier) enviroment to install the requirements.

```bash
conda env create -f outreatchy.yml
```

Download section and language dictionaries and models and rename as "models/model.h5", "dicts/word_dict.pck" and  "dicts/section_dict.pck".

### System Requirements

* Python 2.7
* Keras 2.1.5
* Tensorflow 1.7.0
* sklearn 0.18.1
* pandas
* nltk
* requests
* mwparserfromwell
* h5py

## Usage

Activate the enviroment

```bash
conda activate outreatchy
```

Run all_action.py and insert a page name.