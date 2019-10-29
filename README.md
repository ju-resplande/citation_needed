# Citation-Needed

## Installation 

1. Download run_citation_need_model.py from [this version](https://github.com/mirrys/citation-needed-paper/tree/ef16de6c6165978a55b1bc0a6ba6c9ddc82e0d87).
2. Download section and language dictionaries and models  from the same repository and rename as "models/model.h5", "dicts/word_dict.pck" and  "dicts/section_dict.pck".
3.  Use [miniconda](https://docs.conda.io/en/latest/miniconda.html) (or conda but its heavier) enviroment to install the requirements.

```bash
conda env create -f outreatchy.yml
```



### System Requirements

* python 2.7
* keras 2.1.5
* tensorflow 1.7.0
* sklearn 0.18.1
* pandas
* nltk
* requests
* mwparserfromwell
* h5py

## Usage

1. Activate the enviroment

   ```bash
   conda activate outreatchy
   ```

2. Run all_action.py and insert a page name (case sensite). 

It will generate in output_folder:

* table.txt - used by run_citation_need_model.py
* need_citation.txt - needs citation sentence list 