Instahyre Coding Task
A Django backend for a spam detection application

================================================
*List Of Contents*:                             |
- Prerequisites                                 |
- Project Setup                                 |
- API Endpoints                                 |
- Architecture(i.e Code Structure) detail       |
================================================

===================================================================================
*Prerequisites* |
---------------

- Python 3.x installed
- pip (comes with Python)
- Django and other dependencies listed in requirements.txt

===================================================================================
*Project Setup* |
---------------

Note: BE IN THE "assignment" DIRECTORY

1. Install Dependencies
************************

Run the following command to install all required packages from requirements.txt:

pip install -r requirements.txt

2. Configure Environment Variables
***********************************

Create a .env file in the root directory of your project to store your environment variables. The .env file should look like this:

JWT_SECRET=your_jwt_secret_key
Replace "your_jwt_secret_key" with your actual secret key for JWT. This key is used to encode and decode JWT tokens, so keep it secure.

3. Apply Migrations
********************
Run the following command to set up the database tables:


python manage.py migrate

4. Populate Initial Data (for Testing)
***************************************
Run the following custom command to populate initial data for testing:


python manage.py populate_data

Note: This will add sample users, contacts, and other data to the database. The password for all sample users is set to "test"(can use this password for testing apis using those random data), hashed using bcrypt.

5. Run the Development Server
******************************
Start the server using:


python manage.py runserver

Your project will now be accessible at http://127.0.0.1:8000.

6. Testing JWT Authentication
******************************
Use an API client like Postman to test login and other API endpoints.
Set the authorization header in your requests to pass the JWT token:
Key: Authorization
Value: Bearer <your-jwt-token>
Replace <your-jwt-token> with the token you received during login.

============================================================================================================================================================================

*API Endpoints*: |
----------------
1. register/
****************
    Method: POST

    Usecase: Register a new user

    Sample Request Object:{
        name: str(required),
        country_code: int(required),
        phone_number: int(required),
        password: str(required),
        email: str(optional, default=None),
    }

2. login/
***********
    Method: POST

    Usecase: Login a user

    Sample Request Object:{
        country_code: int(required),
        phone_number: int(required),
        password: str(required),
    }

    Returns a JWT Access Token

3. mark_spam/
***************
    Method: POST

    Usecase: Mark a contact as spam

    Headers: Authorization: Bearer <jwt_access_token> (required)

    Sample Request Object:{
        country_code: int(required),
        phone_number: int(required),
    }

4. search_by_name/
*******************
    Method: GET

    Usecase: Search global database with contact having names starting with or containing a given search_query where the contacts which start with name are returned first

    Headers: Authorization: Bearer <jwt_access_token> (required)

    Sample Query Parameters:{
        http://127.0.0.1:8000/register/?search_query=<your_search_query_name>
    }

    Returns data, and returns email for corresponding users matching the search_query if and only if the authenticated user is in the contact list of the users being searched

5. search_by_contact/
**********************
    Method: GET

    Usecase: Search global database with contact having the queried phone number and country code

    Headers: Authorization: Bearer <jwt_access_token> (required)

    Sample Query Parameters:{
        http://127.0.0.1:8000/register/?country_code=<your_country_code_without_+_sign>&phone_number=<your_phone_number_without_country_code>
    }

    Returns data, and returns email for corresponding users matching the search_query if and only if the authenticated user is in the contact list of the users being searched

==============================================================================================================================================================================================

*Architecture* |
----------------

Architecture Used: Clean Architecture

Architectural Components(See app):
1. models.py 
    -> contains all Models using Django ORM tools for SQL
2. storages directory
    -> Contains interface and implementations(impl) file for all tables
    -> Contain the database calls logics

3. presenters diretory
    -> Contains interface and implementations(impl) file for presenting(i.e. generating json response for api calls)
    -> Contain presentation logic for apis

4. interactors directory
    -> Contains the heart of every API
    -> Every Interactor has a wrapper to handle exceptions and call respected presenters
    -> Every Interactor has a private _interact method containg the logic and flow all operations such as getting query params, getting request body params, raising exceptions for wrapper, calling storage, generating dtos and various other login
    -> wrapper is called by the api view

5. views direcory
    -> Contains the entry point of every api
    -> Calls the respective interactor for the corresponding API and returns the corresponding presenter response returned by the interactor

6. urls.py
    -> Contains the paths for apis

7. dtos.py
    -> Contains dataclasses for clean flow of data throughout various components

8. exceptions.py
    -> Contains custom exceptions

9. middlewares directory
    -> Contains middlewares like verify_jwt.py to secure apis by authorization

10. management/commands directory
    -> Contains commands such as populate_data to populate database with random values for testing

==============================================================================================================================================================================================