# Enhancing Bus Transportation Movement in UK through a Cloud-based Smart Review Platform

SmartBus Buddy Prototype

SmartBus Buddy is an innovative and user-friendly mobile application designed to revolutionize your bus transportation experience. This intelligent companion app is equipped with a range of features aimed at making your bus journey more efficient, enjoyable, and hassle-free.

# Development Environment

Home Page : <https://smartbusbuddy.azurewebsites.net/>

Admin Page : <https://smartbusbuddy.azurewebsites.net/admin/>

# Environment Variables

AZURE_DB_NAME='bus_development'

AZURE_DB_HOST='smartbus.mysql.database.azure.com'

AZURE_DB_PORT='3306'

AZURE_DB_USER='c2063081'

AZURE_DB_PASSWORD='June0620@'

TRANSPORT_API_KEY='b0172443d13086192192fc659ac988ef'

TRANSPORT_APP_ID='b42e95c3'

COORDINATE_API_KEY='AIzaSyBic5uX0v4MzK_HoMYlw03cbUvV7lev1Yk'


# Features

Real-time Bus Tracking

Smart Route Optimization

Personalized User Feedback

Bus Details and Historical Reviews

Integration with Google map


## Installation

1. Open Terminal
2. Check whether Python and Django-admin is installed
    
     ```sh
     python --version
     ```
     ```sh
     django-admin --version
     ```
3. If you don't have them installed, Visit the official Python website at <https://www.python.org/downloads/> to download the latest version of Python. After installing Python, open your treminal and type the below:
     ```sh
     python -m pip install Django
     ```
4. Clone the Repository
    ```sh
     git clone https://github.com/sgbo001/SMARTBUS.git
     ```
5. Create a Virtual Environment
    ```sh
     python -m venv myenv
     ```
6. Activate the virtual environment
   - On Windows
   ```sh
     myenv\Scripts\activate
     ```
   - On Windows
   ```sh
     myenv\Scripts\activate
     ```
8. Install Dependencies
   - cd your_project_directory
   ```sh
     pip install -r requirements.txt
     ```
9. Run Migrations
   ```sh
     python manage.py makemigrations
     ```
   ```sh
     python manage.py migrate
     ```
10. Create Superuser
    ```sh
     python manage.py createsuperuser
     ```
11. Run Development Server
    ```sh
     python manage.py runserver
     ```
12. Open your web browser and navigate to http://127.0.0.1/ to access your Django application. You can also access the admin panel at http://127.0.0.1/admin/.

# Contributors

- [Adetoyese Olaide](https://github.com/sgbo001)

