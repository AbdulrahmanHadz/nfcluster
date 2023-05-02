## How to run


### Step 1:
#### Create venv
***If on mac/linux:***
```bash
python3.8 -m venv "venv"
source venv/bin/activate
pip install -r requirements.txt
```
***If on windows:***
```bash
python3.8 -m venv "venv"
"venv/Scripts/activate"
pip install -r requirements.txt
```

### Step 2:
#### Start Django Server and run migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 3:
#### Run development server
***If NLTK raises missing packages errors, import NLTK from the CLI and then download the missing packages***
```bash
python3 manage.py runserver
```
