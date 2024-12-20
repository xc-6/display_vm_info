from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# HTML template for the page
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Request History</title>
</head>
<body>
    <h1>Request History</h1>
    <table border="1">
        <tr>
            <th>Client Name</th>
            <th>IP Address</th>
            <th>MAC Address</th>
            <th>Client Time</th>
            <th>Server Time</th>
        </tr>
        {% for req in request_history %}
        <tr>
            <td>{{ req.client_name }}</td>
            <td>{{ req.client_ip_address }}</td>
            <td>{{ req.client_mac_address }}</td>
            <td>{{ req.client_request_time }}</td>
            <td>{{ req.server_record_time }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

# File to store request history
history_file = 'request_history.json'

# Load history of requests from file
def load_request_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

# Save history of requests to file
def save_request_history():
    with open(history_file, 'w') as file:
        json.dump(request_history, file, indent=4)

# Initialize request history
request_history = load_request_history()

@app.route('/post_vm_info', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        client_name = data.get('client_name')
        client_ip_address = data.get('client_ip_address')
        client_mac_address = data.get('client_mac_address')
        client_request_time = data.get('client_request_time')

        exists = False
        # Look for matching MAC address to update.
        for req in request_history:
            if req['client_mac_address'] == client_mac_address:
                req['client_ip_address'] = client_ip_address
                req['client_name'] = client_name
                req['client_request_time'] = client_request_time
                req['server_record_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                exists = True
                break

        if not exists:
            # Add the new request to history
            request_history.append({
                'client_name': client_name,
                'client_ip_address': client_ip_address,
                'client_mac_address': client_mac_address,
                'client_request_time': client_request_time,
                'server_record_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        request_history.sort(key=lambda x: datetime.strptime(x['server_record_time'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        # Save the updated request history to file
        save_request_history()

        return jsonify({"message": "Data received", "data": data}), 200

    return render_template_string(template, request_history=request_history)

if __name__ == '__main__':
    app.run(debug=True)
