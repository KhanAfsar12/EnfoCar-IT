1. git clone https://github.com/KhanAfsar12/EnfoCar-IT.git

2. cd pricing_module


3. python -m venv venv

4. source venv/bin/activate  # On Windows: venv\Scripts\activate

5. pip install django djangorestframework


6. python manage.py migrate

7. python manage.py createsuperuser


8. python manage.py runserver

9. Visit http://localhost:8000/admin/

    i. Log in with your superuser credentials
    
    ii. Configure pricing settings in the Pricing Config section

    iii. Send POST requests to http://localhost:8000/api/calculate-price/ with JSON payload:

{

    "distance": 4.5,
    
    "ride_time": 90,
    
    "waiting_time": 5,
    
    "date": "2023-06-04T12:00:00"

}