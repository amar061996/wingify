# Wingify
Wingify API test created using Django Rest Framework.

## Usuage
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Clone the project to your local computer. You can either download the .zip file or use the command: 

```
git clone https://github.com/amar061996/wingify.git
```
### Installing

Once the project is cloned, in order to run the application first the dependencies have to be installed. To install the dependencies open cmd and execute
```
pip install -r requirements.txt
```

Once the dependencies are installed, migrate and create database
```
python manage.py makemigrations
```
```
python manage.py migrate
```
To create superuser:

```
python manage.py createsuperuser
```
To run the app locally
```
python manage.py runserver
```

### Contributions
Open to all types of contributions
