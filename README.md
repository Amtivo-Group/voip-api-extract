# VOIP Data Extract

## Introduction
This python project aims to extract data from BaB's voip database and push it into Qlik sense so we can report key 
KPI's.

## Project Owners
- Antony Thornton <antony.thornton@amtivo.com>
- David English <david.english@british-assessment.co.uk>


## How to use
Note: I initially had trouble connecting the local repo to GitHub so some files may not have been pushed correctly. 
1. Clone the repository to your IDE
2. Install requirements using the terminal command

        pip install -r requirements.txt
3. Create a config.py file and populate the public and private keys
   - You will need an admin login to the VOIP page
   - This is also where the API documentation can be found
4. Update the list of tables you want to add

### Updating selections
Initially the list was called records because I wanted to pass in another variable, but I ended up not needing this. 
Copy the first line found under records and populate the '' with the name of the table, from the tables list in the API
documentation.

    records = [
    # {'url': ''}
    # {'url': 'eventlog'},
    {'url': 'users'},
    {'url': 'cl_calls'},
    {'url': 'cl_participants'},
    # {'url': 'add table name here'}
    # {'url': 'add table name here'}
    # {'url': 'add table name here'}
    # {'url': 'add table name here'}
    # {'url': 'add table name here'}
    ]

### Future Features
- Push data extracted directly into Qlik Sense via hosting
- Potentially manipulate the dataframes
  - Renaming of fields so that they connect automatically in Qlik sense
- Remove code that manually exports files to FP&A location