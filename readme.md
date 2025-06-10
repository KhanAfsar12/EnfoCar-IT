git clone https://github.com/KhanAfsar12/EnfoCar-IT.git \n
cd pricing_module

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django djangorestframework

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
Visit http://localhost:8000/admin/
Log in with your superuser credentials
Configure pricing settings in the Pricing Config section

Send POST requests to http://localhost:8000/api/calculate-price/ with JSON payload:
{
    "distance": 4.5,
    "ride_time": 90,
    "waiting_time": 5,
    "date": "2023-06-04T12:00:00"
}