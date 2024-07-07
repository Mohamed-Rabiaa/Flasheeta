from app import create_app
from flask import redirect, url_for

app = create_app()

# Redirect the user to the login page when he request the home page
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host='https://flasheeta.pythonanywhere.com', port=5000)
