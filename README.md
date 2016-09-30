# OpenEvals
Implementation of the open evals project using the Django framework.

## Usage (Local Development)
- Copy ```secrets.py.template``` to ```secrets.py``` and fill in the credentials.
- Run ```python manage.py runserver```

## Developers - Installation
- Create virtual environment for the python application, with >= python 3.4
- run `pip install -r requirements.txt`
- run `ln -s -f hooks/pre-commit .git/hooks/pre-commit`

## Workflow - how to push code

In an attempt to ensure some type of quality control, we'll be using a 
pull-request, review and then merge workflow. 


```
$ git branch user-dev-branch        # specify your working branch
// do code
// test personally
$ git add --all                     
$ git commit -m "message"           # commit your work, with a helpful commit message!
$ git push origin user-dev-branch   # will push to a remote branch
```

Using the Github website, you can then make a pull request against 
the current master-working branch. The current master-working branch is `dev`.
A travisCI build will be triggered. 

Once a pull request has been made <b> please wait for two reviews before merging </b> as well
as a successful travis build.

##LOLOLOLOL
