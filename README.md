# Backend-Assignment

## Overview

The Django Referral API is a user authentication and referral system that allows users to register, log in, and use referral codes for inviting others. The API supports functionalities such as user registration with referrals, password management, and authentication.

## Features

User Registration: Users can register with or without a referral code.

Referral System: Users can invite others using referral codes.

Authentication: Login functionality with case-insensitive username handling.

Password Management: Users can reset passwords using email.

Validation & Edge Cases: Duplicate emails, invalid referral codes, missing fields, and more are handled.

## Technologies Used

Django (Backend Framework)

Django REST Framework (API Development)

SQLite (Database, but can be switched to PostgreSQL/MySQL)

pytest/unittest (Testing)

## Installation & Setup

### Clone the repository

```git clone https://github.com/yourusername/Django-Referral-API.git```

```cd Django-Referral-API```

### Create a virtual environment and activate it

```python -m venv venv```

```source venv/bin/activate```

### Install dependencies

```pip install -r requirements.txt```

### Run migrations

``` python manage.py migrate ```

### Create a superuser (Optional, for admin access)

```python manage.py createsuperuser```

### Run the development server

```python manage.py runserver```

### API Endpoints

#### User Registration

POST /api/register/

```
{
  "username": "newuser",
  "email": "new@example.com",
  "password": "testpass",
  "referral_code": "optional-code"
}
```


#### User Login

POST /api/login/

```
{
  "username": "newuser",
  "password": "testpass"
}
```


#### Forgot Password

POST /api/forgot-password/

```
{
  "email": "new@example.com"
}
```


#### Password Reset (Confirm New Password)

POST /api/reset-password/
```
{
  "token": "reset-token",
  "new_password": "newsecurepassword"
}
```

#### Fetch Referral List

``` GET /api/referrals/ ```

Returns a list of users referred by the logged-in user.

#### Referral Statistics

``` GET /api/referral-stats/ ```

Retrieves statistics on successful referrals.

#### Running Tests

To run unit and integration tests:

``` python manage.py test accounts ```

