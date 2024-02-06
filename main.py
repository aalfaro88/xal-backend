from flask import Flask
from flask_cors import CORS 
from app.routes.stackexchange import stack_exchange

app = Flask(__name__)

CORS(app)

app.register_blueprint(stack_exchange, url_prefix='/stackexchange')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
