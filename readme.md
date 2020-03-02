# Transactions
Digital Hub - Backend
Assignment - CP

## Installation
> made with love & python 3.6

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the libraries

- First, install all dependencies:

```bash
pip3 install -r requirements.txt
```

- Create the database "assignment_django" in your localhost (or your database server)

- Change database settings in assignment_django/settings.py (line 78)

> DATABASES = {
>     'default': { ...

- Run the django migrations

```bash
python3.6 manage.py migrate
```
- Create a superuser! (follow the wizard)

```bash
python3.6 manage.py createsuperuser
```

- Run the account fixtures! (many as you want, ten per hit)

```bash
python3.6 manage.py fixtures
```

- Run the django development server

```bash
python3.6 manage.py runserver
```

- Open your browser in localhost:8000/


## Usage

- Please visit the swagger docs: http://localhost:8000/api

### add transaction
POST /transactions/

### get all transactions by account
GET /transactions/{account_number}

### get all sent transactions by account
GET /transactions/{account_number}/?sent

### get all received transactions by account
GET /transactions/{account_number}/?received

### get account balance
GET /balance/{account_number}/

# Important, use a basic auth with the user/pwd has been created as superuser

## License
[MIT](https://choosealicense.com/licenses/mit/)
