from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import uuid
import base64
import json

app = FastAPI()

# Allow CORS for all origins (adjust this as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/get_nft_and_image")
def get_nft_and_image():
    url = "https://api.verbwire.com/v1/nft/mint/quickMintFromFile"
    files = {"filePath": ("certificate.png", open("certificate.png", "rb"), "image/png")}
    payload = {
        "allowPlatformToOperateToken": "true",
        "chain": "sepolia",
        "name": "certificate",
        "description": "certified track completion"
    }
    headers = {
        "accept": "application/json",
        "X-API-Key": ""
    }
    response = requests.post(url, data=payload, files=files, headers=headers)

    # Determine if response status is 400 or 401, and handle accordingly
    if response.status_code in [400, 401]:
        unique_id = str(uuid.uuid4())
        nft_info = {"uuid": unique_id}
    else:
        nft_info = response.json()

    # Convert NFT info to a string
    nft_info_str = json.dumps(nft_info)

    # Read and encode the image file
    with open("certificate.png", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Create a JSON response with both the image data and NFT info
    response_data = {
        "image": image_data,
        "nft_info": nft_info_str
    }

    return JSONResponse(content=response_data)