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

- Now open http://127.0.0.1:8000/ in your browser.
- Enter the regular expression pattern (e.g. "(AATCGA|GGCAT)") and hit the Submit button to see the result.


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
## Sample Output

The following is a partial output from part 1 (see the full outputs for both parts in the outputs folder). Each range (e.g., 543-547, 672-676, 1572-1576) represents the location of a found sequence within the searched data, where the first number is the start index and the second number is the end index. **Indexing is zero-based**.
```
GGCAT
  543-547
  672-676
  1572-1576
  1694-1698
  2057-2061
  3651-3655
  4431-4435
  6834-6838
  ...
  29381-29385

AATCGA
  26007-26012

```

---
## Architecture

This project is implemented as a web application and a command line utility using **Django** and **Python** for the backend and **JavaScript** for the frontend. It follows a client-server model where the browser interacts with the server through HTTP requests.

### Components

- **Frontend**
  - Implemented with JavaScript and HTML.
  - Displays the UI and handles user interactions.
  - Send requests to the backend using asynchronous HTTP requests (Fetch).
  - Updates the UI dynamically based on server responses.

- **Backend**
  - Built with Django and Python.
  - Provides API endpoint and Django HTML template.
  - Search XML files and returns responses.

- **Command Line Utility**
  - Implemented as a custom Django management command.
  - Provides a non-graphical interface for running the same operations as the web app.
  - Reuses the same backend logic as the web app to avoid duplication.

### Data Flow

1. A user interacts with the application in the browser.
2. The frontend JavaScript sends an HTTP request to the Django backend API.
3. The Django backend processes the request and executes the logic to search for patterns inside XML files.
4. Django returns a JSON response.
5. The frontend receives the response and updates the user interface.

---

## Design


- 

---

## Technologies
- Python 3.12
- Django 5.2
- Django REST framework 3.16
- JavaScript/HTML



