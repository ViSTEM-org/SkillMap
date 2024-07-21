from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
import requests
import uuid
import base64
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

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

@app.post("/check_genuineness")
async def check_genuineness(text: str):
    llm2 = OpenAI(openai_api_key="", temperature=0.7)
    output_parser2 = CommaSeparatedListOutputParser()
    template2 = """You are a simple functioning robot that determines if a person is being genuine in their response or not
    Question: here is the text {text}
    Answer: Give out a binary response, EITHER "yes" OR "no" if the person is being genuine or not
    """
    prompt_template2 = PromptTemplate(input_variables=["text"], template=template2, output_parser=output_parser2)
    answer_chain2 = LLMChain(llm=llm2, prompt=prompt_template2)
    
    try:
        result = answer_chain2.run(text)
        return PlainTextResponse(result.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))