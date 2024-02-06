from flask import Blueprint, jsonify
import requests

stack_exchange = Blueprint('stack_exchange', __name__)

url = "https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"

@stack_exchange.route('/stackexchange')
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
    response = requests.get(url)
    data = response.json()
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
    response = requests.get(url)
    data = response.json()
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
    response = requests.get(url)
    data = response.json()
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
    response = requests.get(url)
    data = response.json()
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
    response = requests.get(url)
    data = response.json()
    oldest = min(data['items'], key=lambda item: item['creation_date'])
    most_recent = max(data['items'], key=lambda item: item['creation_date'])
    return jsonify({
        'oldest': oldest,
        'most_recent': most_recent
    })
