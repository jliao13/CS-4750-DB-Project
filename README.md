# CS-4750-DB-Project
Housing Database Implementation Project

## Access the web app
Our web app is pushed to GAE (Google App Engine) at: https://cs-4750-db-292115.ue.r.appspot.com/ 

## To run locally: 
Need to run the cloud proxy to connect to database on your local host. Then, set up your python veritual environment with all the necessary dependencies. Lastly run the Django web app on your local host.

### Connect to GCP MySQL db
Setup to connect mysql gcp to django app: https://medium.com/@tintinve/instructions-to-set-up-django-3-0-4-and-google-cloud-mysql-3-7-instance-on-macos-catalina-10-1-5-d302164ffc3f  

Run on desktop to run sql proxy:
```
./cloud_sql_proxy -instances=cs-4750-db-292115:us-east4:cville-leasing-project-db=tcp:3306
```

### Set up Python Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the django server
```
python manage.py runserver
```