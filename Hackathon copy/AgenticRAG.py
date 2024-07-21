import os
from dotenv import load_dotenv
import serpapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Load environment variables
load_dotenv()
serp_api_key = os.getenv()
openai_api_key = ""

os.environ["OPENAI_API_KEY"] = openai_api_key

client = serpapi.Client(api_key="")

# Function to get search results using SerpAPI
def get_search_results(query, num_results=5):
    result = client.search(
        q= query,
        engine= "google",
        num= str(num_results),
        location= "United States",
        hl= "en",
        gl= "us"
    )
    
    content = []
    for item in result["organic_results"]:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        content.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
    
    return "\n".join(content)


def create_knowledge_base(topics):
    documents = []
    for topic in topics:
        content = get_search_results(topic)
        documents.append(content)
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(texts, embeddings)


# Function to generate a study plan
def generate_study_plan(docsearch, query, openai_api_key):
    docs = docsearch.similarity_search(query)
    
    llm = OpenAI(temperature=0.3, openai_api_key="", max_tokens=1000)
    chain = load_qa_chain(llm, chain_type="stuff")
    
    prompt_template = """
    Based on the following information about {topic}, create a detailed and personalized study plan. Try to be clear and succinct in your language and dont generate too long answers.
    The plan should include:
    1. Clear learning objectives
    2. A very short structured timeline to cover the topic for 1 week
    3. Suggested resources for each week (use the provided links where relevant)

    Context: {context}

    Study Plan:
    """
    
    prompt = PromptTemplate(
        input_variables=["topic", "context"],
        template=prompt_template,
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.run(topic=query, context=docs)

'''# Main function to run the study planner
def run_study_planner(topics, main_topic, openai_api_key):
    print("Creating knowledge base from search results...")
    docsearch = create_knowledge_base(topics)
    
    print(f"Generating personalized study plan for {main_topic}...")
    study_plan = generate_study_plan(docsearch, main_topic, openai_api_key)
    
    print("Your personalized study plan:")
    print(study_plan)

if __name__ == "__main__":

    # Example usage
    topics = [
        "Flutter Fundamentals",
        "Flutter for app development"
    ]
    main_topic = "Flutter for Beginners"

    run_study_planner(topics, main_topic,"")'''


class StudyPlanRequest(BaseModel):
    topics: list[str]
    main_topic: str


@app.post("/generate_study_plan")
async def generate_study_plan_endpoint(request: StudyPlanRequest):
    try:
        #print("Creating knowledge base from search results...")
        docsearch = create_knowledge_base(request.topics)
        #print(f"Generating personalized study plan for {request.main_topic}...")
        study_plan = generate_study_plan(docsearch, request.main_topic, "")
        return {"study_plan": study_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)