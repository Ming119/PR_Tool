# PR_Tool
This is a PR tool for sunbirddcim/test_automation.

### Enviornment Setup
1. Install Python dependcies.
```bash
pip3 install -r requirements.txt 
```

2. Setup `config.py` (please ref to `config_temp.py`)
```py
import os
from datetime import timedelta

SECRET_KEY = os.urandom(256)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/test.db') 
SQLALCHEMY_TRACK_MODIFICATIONS = True

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""

OWNER = "sunbirddcim"
REPO  = "test_automation"
BRANCH = "9.0.0-branch"
```

### Usage
Run the server
```bash
python3 app.py 
```

Run the server with development mode
```bash
python3 app.py -d True
```

Customize the host and port
```bash
python3 app.py --host 192.168.0.2 -p 8080
```
