# OpenEvals
Implementation of the open evals project using the Django framework.

## Usage (Local Development)
- Copy ```secrets.py.template``` to ```secrets.py``` and fill in the credentials.
- Run ```python manage.py runserver```

## Developers - Installation
- Create virtual environment for the python application, with >= python 3.4
- run `pip install -r requirements.txt`
- run `ln -s -f hooks/pre-commit .git/hooks/pre-commit`
