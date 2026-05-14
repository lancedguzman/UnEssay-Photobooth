# Setup

## Requirements
- PIP
- Python 3.12+
- Django

### Installation
```
git clone https://github.com/lancedguzman/UnEssay-Photobooth.git
cd UnEssay-Photbooth
```

### Start Your Virtual Environment
```
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### Install Your Requirements
```
pip install -r requirements.txt
```

### Make Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Run Your Server
```
# Start the server
python manage.py runserver
```