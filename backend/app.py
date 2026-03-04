from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.activities import activities_bp

app = Flask(__name__)
CORS(app)

# rejestracja blueprintow
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(activities_bp, url_prefix='/activity')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
