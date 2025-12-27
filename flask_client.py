import requests
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# API Configuration
BASE_URL = "https://env-tls.henokcodes.com"
API_USERNAME = os.environ.get("API_USERNAME")
API_PASSWORD = os.environ.get("API_PASSWORD")

class APIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def login(self):
        """Obtain JWT tokens from the Django API."""
        if not self.username or not self.password:
            print("Error: API_USERNAME or API_PASSWORD environment variables are not set.")
            return False
            
        url = f"{self.base_url}/api/token/"
        try:
            print(f"Attempting login for user: {self.username}")
            response = requests.post(url, json={
                "username": self.username,
                "password": self.password
            })
            if response.status_code == 400:
                print(f"Bad Request (400): {response.text}")
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get('access')
            self.refresh_token = data.get('refresh')
            print("Successfully authenticated with API.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return False

    def get_work_logs(self, start_date=None, end_date=None, tag=None):
        """Fetch WorkLog data from the secure endpoint."""
        if not self.access_token:
            if not self.login():
                return None

        url = f"{self.base_url}/work-logs/api/logs/"
        params = {}
        if start_date: params['start_date'] = start_date
        if end_date: params['end_date'] = end_date
        if tag: params['tag'] = tag

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            
            # If token expired, try to refresh once (optional implementation)
            if response.status_code == 401:
                print("Token expired, re-authenticating...")
                if self.login():
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = requests.get(url, params=params, headers=headers)
                else:
                    return None

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None

# Initialize Client
client = APIClient(BASE_URL, API_USERNAME, API_PASSWORD)

@app.route('/fetch-logs')
def fetch_logs():
    # Example parameters from request query
    start_date = request.args.get('start_date', '2025-12-01')
    tag = request.args.get('tag', '3')
    
    logs = client.get_work_logs(start_date=start_date, tag=tag)
    
    if logs is not None:
        return jsonify({
            "status": "success",
            "count": len(logs),
            "data": logs
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Could not retrieve data from API"
        }), 500

if __name__ == '__main__':
    # Print a hint for the user
    print("Starting Flask client...")
    print(f"Endpoint available at: http://127.0.0.1:5000/fetch-logs?start_date=2025-12-01&tag=1")
    app.run(debug=True, port=5000)
