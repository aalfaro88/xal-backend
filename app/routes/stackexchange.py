from flask import Blueprint, jsonify, current_app
import requests
import time

stack_exchange = Blueprint('stack_exchange', __name__)

# Define the base URL for Stack Exchange API
API_BASE_URL = "https://api.stackexchange.com/2.2/"

@stack_exchange.route('/')
def stack_exchange_route():
    """
    Stack Exchange Data
    ---
    get:
      description: Get data from Stack Exchange API
      responses:
        200:
          description: A list of data from Stack Exchange API
    """
    # Create headers with your client ID and key
    headers = {
        'User-Agent': 'YourApp/1.0',  # Replace with your app name and version
        'X-API-Key': current_app.config['KEY']
    }

    # Make the API request
    response = requests.get(API_BASE_URL + "search",
                            params={'order': 'desc', 'sort': 'activity', 'intitle': 'perl', 'site': 'stackoverflow'},
                            headers=headers)
    
    data = response.json()

    # Check for backoff and handle rate limiting
    if 'backoff' in data:
        backoff_seconds = data['backoff']
        time.sleep(backoff_seconds)

    return jsonify(data)

@stack_exchange.route('/answered-unanswered')
def answered_unanswered_route():
    """
    Answered and Unanswered Questions
    ---
    get:
      description: Get the number of answered and unanswered questions
      responses:
        200:
          description: A JSON object with the count of answered and unanswered questions
    """
    # Create headers with your client ID and key
    headers = {
        'User-Agent': 'YourApp/1.0',  # Replace with your app name and version
        'X-API-Key': current_app.config['KEY']
    }

    # Make the API request
    response = requests.get(API_BASE_URL + "search",
                            params={'order': 'desc', 'sort': 'activity', 'intitle': 'perl', 'site': 'stackoverflow'},
                            headers=headers)
    
    data = response.json()

    # Calculate answered and unanswered counts
    answered = sum(1 for item in data['items'] if item['is_answered'])
    unanswered = sum(1 for item in data['items'] if not item['is_answered'])

    return jsonify({
        'answered': answered,
        'unanswered': unanswered
    })

@stack_exchange.route('/highest-reputation')
def highest_reputation_route():
    """
    Question with Highest Reputation
    ---
    get:
      description: Find and return the question with the highest owner reputation
      responses:
        200:
          description: A JSON object of the question with the highest owner reputation
    """
    # Create headers with your client ID and key
    headers = {
        'User-Agent': 'YourApp/1.0',  # Replace with your app name and version
        'X-API-Key': current_app.config['KEY']
    }

    # Make the API request
    response = requests.get(API_BASE_URL + "search",
                            params={'order': 'desc', 'sort': 'activity', 'intitle': 'perl', 'site': 'stackoverflow'},
                            headers=headers)
    
    data = response.json()

    # Find the question with the highest owner reputation
    highest_rep = max(data['items'], key=lambda item: item['owner'].get('reputation', 0))

    return jsonify(highest_rep)

@stack_exchange.route('/fewest-views')
def fewest_views_route():
    """
    Question with Fewest Views
    ---
    get:
      description: Find and return the question with the fewest views
      responses:
        200:
          description: A JSON object of the question with the fewest views
    """
    # Create headers with your client ID and key
    headers = {
        'User-Agent': 'YourApp/1.0',  # Replace with your app name and version
        'X-API-Key': current_app.config['KEY']
    }

    # Make the API request
    response = requests.get(API_BASE_URL + "search",
                            params={'order': 'desc', 'sort': 'activity', 'intitle': 'perl', 'site': 'stackoverflow'},
                            headers=headers)
    
    data = response.json()

    # Find the question with the fewest views
    fewest_views = min(data['items'], key=lambda item: item.get('view_count', float('inf')))

    return jsonify(fewest_views)

@stack_exchange.route('/oldest-recent')
def oldest_recent_route():
    """
    Oldest and Most Recent Question
    ---
    get:
      description: Find and return the oldest and most recent questions based on the creation date
      responses:
        200:
          description: A JSON object containing the oldest and most recent questions
    """
    # Create headers with your client ID and key
    headers = {
        'User-Agent': 'YourApp/1.0',  # Replace with your app name and version
        'X-API-Key': current_app.config['KEY']
    }

    # Make the API request
    response = requests.get(API_BASE_URL + "search",
                            params={'order': 'desc', 'sort': 'activity', 'intitle': 'perl', 'site': 'stackoverflow'},
                            headers=headers)
    
    data = response.json()

    # Find the oldest and most recent questions
    oldest = min(data['items'], key=lambda item: item['creation_date'])
    most_recent = max(data['items'], key=lambda item: item['creation_date'])

    return jsonify({
        'oldest': oldest,
        'most_recent': most_recent
    })
