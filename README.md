# Sequence Pattern Search
**Takes as input a regular expression pattern and shows the search results.**

---

## Description
This project is to use a regular expression pattern to search in a large XML file that might not fit in the memory.

---

## Installation
Step-by-step instructions to get the project running locally:

1. Clone the repository:
   ```
   git clone https://github.com/jyu2100/regex_seq_search.git
2. Navigate to the project folder:
   ```
   cd regex_seq_search
3. Set up a python virtual environment
   ```
   python -m venv .venv
   venv\Scripts\activate          # On Windows
   source venv/bin/activate       # On Mac/Linux
4. Install dependencies:
   ```
   pip install -r requirements.txt
---

## Datasets
Download the nucleotide from 30271926 NIH’s nucleotide database
- Navigate to https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=30271926&rettype=fasta&retmode=xml from your browser, rename the downloaded file to sequence.fasta_30271926.xml and copy it to regex_seq_search/data folder.

Download the nucleotide from 224589800 NIH’s nucleotide database
- Navigate to https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=224589800&rettype=fasta&retmode=xml from your browser, rename the downloaded file to sequence.fasta_224589800.xml and copy it to regex_seq_search/data folder.

sequence.fasta_30271926.xml is already included in the repository, however, sequence.fasta_224589800.xml is over 200MB and could not fit in a GitHub project.

---

## Usage
### Running with browser
- Activate the virtual environment from the project's root folder
```
   venv\Scripts\activate          # On Windows
   source venv/bin/activate       # On Mac/Linux
```

- Start the development server by typing the following command:
```
   python manage.py runserver
```

- Now open http://127.0.0.1:8000/ in your browser
```
   python manage.py runserver
```

### Running with CLI

- Activate the virtual environment from the project's root folder
```
   venv\Scripts\activate          # On Windows
   source venv/bin/activate       # On Mac/Linux
```

- Run the Django management command run_search_cli:
```
   python manage.py run_search_cli <PATTERN> <UID>

   For example

   python manage.py run_search_cli "(AATCGA|GGCAT)" "224589800"
```

---

## Design and Architecture
- 

---

## Technologies
- Python 3.12
- Django 5.2
- Django REST framework 3.16
- JavaScript/HTML



