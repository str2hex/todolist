- todolist создание календаря с планированием 

# TODOLIST

## Stack

* ![version](https://img.shields.io/badge/pip-v22.3.1-informational/?style=for-the-badge&logo=pypi)
* ![version](https://img.shields.io/badge/Python-v3.10.6-informational/?style=for-the-badge&logo=Python)
* ![version](https://img.shields.io/badge/Django-v4.1.3-informational/?style=for-the-badge&logo=Django)
* ![version](https://img.shields.io/badge/Postgresql-v12.0-informational/?style=for-the-badge&logo=Postgresql)

## Install

### Clone the repo

```sh
git clone https://github.com/str2hex/todolist.git
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### config
```sh
.enc_ci
```

### Start DB

```sh
docker-compose up --build -d
```

### Roll up migrations

```sh
python manage.py migrate
```

### Create superuser


```sh
python manage.py createsuperuser
```

### Run app

```sh
python manage.py runserver
```

### Set Debug

```sh
set DEBUG=False
set DEBUG=True
```
