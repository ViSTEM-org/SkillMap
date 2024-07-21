import requests

def test_fastapi_endpoint():
    # URL of your FastAPI endpoint
    endpoint_url = "http://localhost:8000/get_nft_and_image"

    # Make the request to the FastAPI endpoint
    response = requests.get(endpoint_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the image
        with open("response_image.png", "wb") as image_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    image_file.write(chunk)

        # Extract and print NFT information from headers
        nft_info = response.headers.get("X-NFT-Info", "No NFT info found")
        print("NFT Information or UUID:", nft_info)

        print("Image saved as 'response_image.png'")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    test_fastapi_endpoint()
