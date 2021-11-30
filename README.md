![python logo](images/Python_logo.jpg)

# Support API

---
# Author
- Vadim Gulakov

---
# Description
API for the support service.


---
# Requirements
- Python>=3.9

- Docker to run a container

---
# Installation

- Add your **.env** file in the root directory with a similar structure:

        DEBUG = 1
        SECRET_KEY = your_key
        SQL_ENGINE = your_DBMS_engine
        SQL_DATABASE = your_db
        SQL_USER = your_user
        SQL_PASSWORD = your_password
        SQL_HOST = your_host
        SQL_PORT = your_port
        DATABASE = your_DBMS

# Docker:
- Clone the repo
>git clone https://github.com/vdmglkv/Support.git -b develop
- In the directory **with docker-compose.yaml**
>docker-compose up --build

And now you can run the API server from the docker container

# Without docker:
- Clone the repo
>git clone https://github.com/vdmglkv/Support.git -b develop
- In the directory **with settings.py** add **your** database configuration
- Add migrations in your db:

[Windows]
>python manage.py makemigrations && python manage.py migrate

[Linux/Mac OS]
>python3 manage.py makemigrations && python3 manage.py migrate


---
# Usage
# Register new user:

    [api-url]: http://localhost:8000/api/register/
    You should send a post request with a data in json format.
        Example:
        [WARNING]: The email should be similar to the real one!
        {
            "email": "Vadim@gmail.com",
            "password": "12345"
        }
    This request will return your id and email.
        Example:
        {
            "id": "1",
            "email": "Vadim@gmail.com"
        }

# Register new superuser:

    In repo in the directory with manage.py:
    [Windows]:          - $ python manage.py createsuperuser
                        - Enter your information

    [Linux/Mac OS]:     - $ python3 manage.py createsuperuser
                        - Enter your information
                   
                     


# Login in registered user account:

    [api-url]: http://localhost:8000/api/login/
    You should send a post request with a data in json format.
        Example:
        {
            "email": "Vadim@gmail.com",
            "password": "12345"
        }
    This request will save your JWT in the cookies and return a message.
        Example:
        {
            "message": "Successfully login"
        }

# Check user information:

    [api-url]: http://localhost:8000/api/user/
    You should send a get request without data because your JWT saved into cookies.
    This request return your id and email.
        Example:
        {
            "id": "1",
            "email": "Vadim@gmail.com"
        }

# Logout:

    [api-url]: http://localhost:8000/api/logout/
    You should send a post request without data because your JWT saved into cookies.
    This request delete all cookies and return a message.
        Example:
        {
            "message": "success"
        }

# Add ticket:

    [api-url]: http://localhost:8000/api/ticket/
    [WARNING]: You should to be authorized!
    You should send a post request with data in json format.
    This request save a ticket in database and return him to you.
        Example:
        {
            "title": "TestTitle",
            "description": "TestDesc"
        }

    And it return:
        Example:
        {
            "id": 1,
            "title": "TestTitle",
            "description": "TestDesc",
            "date": "2021-11-21T14:26:12.618302+03:00",
            "from_user": "Vadim@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        }


# Get tickets:
    [api-url]: http://localhost:8000/api/ticket/
    [WARNING]: You should to be authorized!
    You should send a get request without data.

    If you are an admin, this request will return to you all ticket.
    Else if you are a user, this request will return to you only your ticket.

        Example if you are a user:
    [
        {
            "id": 1,
            "title": "TestTitle",
            "description": "TestDesc",
            "date": "2021-11-21T14:26:12.618302+03:00",
            "from_user": "Vadim@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        }
    ]
    
    Example if you are an admin:
    [
        {
            "id": 1,
            "title": "TestTitle",
            "description": "TestDesc",
            "date": "2021-11-21T14:26:12.618302+03:00",
            "from_user": "Vadim@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        },

        {
            "id": 2,
            "title": "Test",
            "description": "test",
            "date": "2021-11-20T20:56:30.015249+03:00",
            "from_user": "Vadimka@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        },

        {
            "id": 3,
            "title": "Test1",
            "description": "test1",
            "date": "2021-11-20T21:00:22.816048+03:00",
            "from_user": "test@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        },

        {
            "id": 4,
            "title": "Test1",
            "description": "test1",
            "date": "2021-11-20T20:59:57.325752+03:00",
            "from_user": "test@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        }
    ]

# Retrieve a single ticket:

    [api-url]: http://localhost:8000/api/ticket/{id}
    [WARNING]: You should to be authorized!
    You should send a get request without data.

    If you are an admin, you can retrive any ticket.
        Example :
        [api-url]: http://localhost:8000/api/ticket/1/

    It will return:
        Example:
            [
        {
            "id": 1,
            "title": "TestTitle",
            "description": "TestDesc",
            "date": "2021-11-21T14:26:12.618302+03:00",
            "from_user": "Vadim@gmail.com",
            "support_answer": "None",
            "user_answer": "None",
            "status": "Unresolved"
        }
    ]

    Else if you are a user, you can retrive only your ticket.
    
    If you try to retrive a non - existent ticket id, request will 
    return to you an error:
    
      Example:
      [api-url]: http://localhost:8000/api/ticket/3243728943289
      
      It will return:
      {
          "detail": "Not found."
      }
      




# Update ticket:

    [api-url]: http://localhost:8000/api/ticket/{id}
    [WARNING]: You should to be authorized!
    You should send a put/patch request with data in json format.

    If you are an admin, you can add answer to any ticket and update their status.
        Example:
            {
                "support_answer": "Just reboot",
                "status": "Resolved"
            }
    It will return a message:
        Example:
            {
                "message": "success"
            }

    Else if you are a user, you can add only your answer and update
    your ticket's title or description.
        Example:
            {
                "title": "Test",
                "description": "TestDesc",
                "user_answer": "Thanks a lot"
            }
    It will return:
        Example:
            {
                "message": "success"
            }


# Delete ticket:

    [api-url]: http://localhost:8000/api/ticket/{id}
    [WARNING]: You should to be authorized!
    You should send a delete request without data.

    Only admin can delete a ticket
        Example:
        http://localhost:8000/api/ticket/1/

    It will return a message:
        Example:
            {
                "message": "Item has been deleted"
            }

    If you are a user, request will return:.
        Example:
            {
                "message": "Not Allowed"
            }

# Testing

- Django tests
> python manage.py test

- Manual testing

I will recommend using a [postman](https://www.postman.com/)  application.
