# CN-Lab-Assignment

## Objective

## Technology

### Frontend
Pure html, css, js

### Backend
Django, Python

## Run locally
You need to clone the repository then install all require packages in an environment. We recommend you use anaconda distribution
### Install Anaconda

Download here: https://www.anaconda.com/products/distribution

### Install requirements
```{bash}
conda create -n <env_name> python=3.9
```
```
conda activate <created_env_name>
```

```
pip install django
```
### Create database
You need to go to the folder which contains the **manage.py** file then running the following commands

```
python manage.py makemigrations usr base
```

```
python manage.py migrate
```
Running the application on your local.
```
python manage.py runserver
```

Create account
```
python manage.py createsuperuser
```
Then fill in the in need information