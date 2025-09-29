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

## Initial Setup
The following commands show how the required secret image files were originally generated. These files have already been committed to the repository for demo purposes, so you **do not need to run these commands yourself** unless you want to regenerate them. However, **do not commit secret image files in real world projects**. DNA.png (from an open source repository) in the assets folder is used as the base (input) image.
- **Embed Secrets**
   - Use the **embed_value** management command:
   ```
      python manage.py embed_value <input_image> <output_image> <secret_string>

      For example

      python manage.py embed_value "assets/DNA.png" "assets/env1.png" "django-insecure-bug_v=8eihc6c_917tu9y*qx!ict_etrg)!r1c)$za_!*8(oyr"
      
      python manage.py embed_value "assets/DNA.png" "assets/env2.png" "localhost,127.0.0.1"

      python manage.py embed_value "assets/DNA.png" "assets/env3.png" "4@6k8b9h2c2v9n0d3"

      python manage.py embed_value "assets/DNA.png" "assets/env4.png" "SflKxwRJSMeKKF2QT4fwpMe"   
   ```

- **Verify Secrets**
   - Use the **extract_value** management command:
   ```
      python manage.py extract_value <secret_image>

      For example

      python manage.py extract_value "assets/env1.png"
      
      python manage.py extract_value "assets/env2.png"

      python manage.py extract_value "assets/env3.png"

      python manage.py extract_value "assets/env4.png"  
   ```
---

## Usage
🔴 The regular expression pattern is limited to **256** characters in this project

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

### Running with CLI (Django management command version)

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

### Running with CLI (standalone Python script version)

- Make sure your Django server is running:
```
   python manage.py runserver
```

- Then, on the same computer, run:
```
   python scripts/run_search_api_cli.py <PATTERN> <UID>

   For example

   python scripts/run_search_api_cli.py "(AATCGA|GGCAT)" "224589800"
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

- **Command Line Utility (Django management command version)**
  - Implemented as a custom Django management command.
  - Provides a non-graphical interface for running the same operations as the web app.
  - Reuses the same backend logic as the web app to avoid duplication.

- **Command Line Utility (standalone Python script version)**
  - Implemented as a standalone Python scipt.
  - Provides a non-graphical interface for running the same operations as the web app.
  - Calls Django API endpoint via HTTP GET request with query parameters.

### Data Flow

1. A user interacts with the application in the browser.
2. The frontend JavaScript sends an HTTP request to the Django backend API.
3. The Django backend processes the request and executes the logic to search for patterns inside XML files.
4. Django returns a JSON response.
5. The frontend receives the response and updates the user interface.

---

## Design
The design of this project emphasizes **code reusability**, ensuring both the web app and the command line utility share the same backend code. The core backend logic focuses on reading large files that might not fit in the memory and finding patterns within the data.

### Overview

1. **Memory Usage**
    - Since the data file for part 2 exceeds 200 MB, loading it entirely into memory may cause performance issues.
    - **Design**
        - ~~Scan the xml file line by line~~ (A very long line may still cause performance issues).
        - Read the xml file in chunks (default to 1MB).
        - Only handle the data within the opening and closing tags of TSeq_sequence.
        - Stream data (levelaging Python generator) one chunk (default to 1MB) at a time for pattern matching.
2. **Searching for <TSeq_sequence> tag split across two file chunks**
    - <TSeq_sequence> tag may be split across chunks when reading file in chunks.
    - **Design**
        - Have each file chunk overlaps with the previous chunk by a fixed size (the length of "<TSeq_sequence>").
3. **Finding patterns across chunk boundaries**
    - Regex can only find patterns within the current chunk.
    - **Design**
        - Have each chunk overlaps with the previous chunk by a fixed size (default to 256 chars, the maximum regular expression pattern length in this project). Without overlap, matched patterns across chunks would be missed.
4. **Handling duplicate matches**
    - Matches found entirely inside the overlap would appear twice.
    - **Design**
        - Ignore matches that end before the “new” part of the chunk. Except for the first chunk, matches found within the first OVERLAP_SIZE area of a chunk are duplicates.
        - Matches spanning across chunk boundaries are included.
5. **Returning absolute positions**
    - Regex matches return the relative positions within the current chunk, not the absolute positions within the searched data.
    - **Design**
        - Keep track of an absolute offset for the current chunk.
        - Convert relative positions to absolute positions inside TSeq_sequence.
6. **API Rate limiting**
    - Use Regex to search in a large file can be a time-intensive task and the web server could be overloaded if there were excessive requests.
    - **Design**
        - Django REST Framework’s throttling system is used to protect the API from abuse and denial-of-service attempts.
        - This project uses DEFAULT_THROTTLE_CLASSES, which apply the throttling rules globally across all API endpoints. If needed, throttling can be adjusted to a per-view configuration.
        - In a production environment, it is a good idea to combine Django REST Framework’s throttling with rate limiting at the web server level (e.g., NGINX). NGINX can apply IP-based rules before the requests reach the application. NGINX rate limiting also applies to any HTTP traffic, not just APIs.
7. **Using image-based Steganography for secret management**
    - Sensitive configuration values were stored in plaintext settings.py within the repository or .env file.
    - **Design**
        - Use the Stegano Python library to hide sensitive configuration values inside PNG images.
        - Critical settings (e.g., SECRET_KEY, database passwords, API tokens) are embedded into image files during setup.
        - Secrets are extracted from images and then injected into Django’s settings at startup.
---

## Notes
- At first, I tried reading the file line by line, thinking that would keep memory usage low since the whole file wouldn’t be loaded at once. But when I tested with a large XML file, I noticed memory usage was still pretty high. During debugging, I found that the value of the TSeq_sequence element was stored on a single line rather than being split across multiple lines. To address this, I switched to reading the file in fixed-size chunks using file.read(chunk_size), which lowered memory usage and improved processing speed.
- It is assumed that both the input pattern and the data being searched are in uppercase. If they aren’t, then the search needs to be case‑insensitive.
- **The .env file, and secret images have been committed to the repository for demo purposes only. This should not be done for production environments.**
- The web application and command line utilities can handle any valid UID as long as the corresponding xml file has been downloaded to the data folder and named properly beforehand.

---

## Possible Improvements
- Expose chunk size and overlap size as configurable parameters.
- Handle longer input pattern length.
- Secure the API with JWT (JSON Web Token) authentication.
- Write unit tests

---

## Technologies
- Python 3.12
- Django 5.2
- Django REST framework 3.16
- JavaScript/HTML



