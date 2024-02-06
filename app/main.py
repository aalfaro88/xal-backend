from flask import Flask, jsonify
import requests

app = Flask(__name__)

url = "https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"

@app.route('/stackexchange')
def stack_exchange():
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

@app.route('/answered-unanswered')
def answered_unanswered():
    response = requests.get(url)
    data = response.json()
    answered = sum(1 for item in data['items'] if item['is_answered'])
    unanswered = sum(1 for item in data['items'] if not item['is_answered'])
    return jsonify({
        'answered': answered,
        'unanswered': unanswered
    })

@app.route('/highest-reputation')
def highest_reputation():
    response = requests.get(url)
    data = response.json()
    
    highest_rep = max(data['items'], key=lambda item: item['owner'].get('reputation', 0))
    return jsonify(highest_rep)


@app.route('/fewest-views')
def fewest_views():
    response = requests.get(url)
    data = response.json()
    # Assuming all items have a 'view_count' key.
    fewest_views = min(data['items'], key=lambda item: item['view_count'])
    return jsonify(fewest_views)

@app.route('/oldest-recent')
def oldest_recent():
    response = requests.get(url)
    data = response.json()
    oldest = min(data['items'], key=lambda item: item['creation_date'])
    most_recent = max(data['items'], key=lambda item: item['creation_date'])
    return jsonify({
        'oldest': oldest,
        'most_recent': most_recent
    })

def print_console_data():
    response = requests.get(url)
    data = response.json()
    # Here you would process and print data as per requirements 2 to 4.
    # For example:
    print("Data for console:")
    print("Answered and Unanswered:")
    print(sum(1 for item in data['items'] if item['is_answered']),
          sum(1 for item in data['items'] if not item['is_answered']))
    # Continue for other requirements...

if __name__ == '__main__':
    print_console_data()  # Call it before starting the Flask app.
    app.run(host='0.0.0.0', port=5001, debug=True)
