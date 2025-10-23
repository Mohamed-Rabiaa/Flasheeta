from app import create_app
from flask import redirect, url_for
from flask_cors import CORS
import os

app = create_app()
app_host = os.environ.get('FLASK_RUN_HOST')

#Allowing API requests coming from localhost and PythonAnywhere only
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://127.0.0.1:5000",
            "http://localhost:5000",
            "http://158.180.238.158:5000" # oracle cloud instance public ip address
        ],
        "supports_credentials": True
    }})

# Redirect the user to the login page when he request the home page
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host=app_host, port=5000)
