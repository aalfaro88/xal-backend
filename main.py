import os
from flask import Flask
from flask_cors import CORS
from app.routes.stackexchange import stack_exchange
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your configuration values, including KEY
app.config['CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['KEY'] = os.getenv('KEY')

app.register_blueprint(stack_exchange, url_prefix='/stackexchange')

if __name__ == '__main__':
    port = os.getenv('FLASK_RUN_PORT', 5001)  # Default to 5001 if not set
    app.run(host='0.0.0.0', port=port, debug=True)
