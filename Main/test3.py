import requests

def test_check_genuineness():
    url = "http://127.0.0.1:8080/check_genuineness"
    params = {
        "text": "I finished the track, hahaha i am just kiddding heheehehe i dont like python."
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        print("Response from server:", response.text)
    else:
        print(f"Failed to get a response from the server. Status code: {response.status_code}")
        print("Response text:", response.text)

if __name__ == "__main__":
    test_check_genuineness()