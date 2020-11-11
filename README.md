# CS-4750-DB-Project
Housing Database Implementation Project


Shouldn't have to edit anything except for the html files in templates folder. 

## How to run Heroku app locally:

```
source venv/bin/activate
heroku local
```

## How to push Heroku app
```
git add .
git commit -m <commit-message>
git push heroku <branch-name>
git push 
```

Make sure to verify that all your commits got pushed with 'git push' at the end. 

## Connect to GCP MySQL db
Setup to connect mysql gcp to django app: https://medium.com/@tintinve/instructions-to-set-up-django-3-0-4-and-google-cloud-mysql-3-7-instance-on-macos-catalina-10-1-5-d302164ffc3f  

Run on desktop to run sql proxy:
```
./cloud_sql_proxy -instances=cs-4750-db-292115:us-east4:cville-leasing-project-db=tcp:3306
```

## Set up Python Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```