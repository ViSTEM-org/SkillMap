import requests
import json

# URL of your FastAPI server
url = "http://localhost:8000/generate_study_plan"

# Data to be sent in the POST request
data = {
    "topics": ["Flutter Fundamentals", "Flutter for app development"],
    "main_topic": "Flutter for Beginners"
}

# Headers
headers = {
    "Content-Type": "application/json"
}

def send_post_request():
    try:
        # Send POST request
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            study_plan = response.json()
            
            print("Study Plan:")
            print(json.dumps(study_plan, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_post_request()