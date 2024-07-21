from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

llm2 = OpenAI(openai_api_key="", temperature=0.7)
output_parser2 = CommaSeparatedListOutputParser()
template2 = """You are a simple functioning robot that determines if a person is being genuine in their response or not
    Question: here is the text {text} 
    Answer: Give out a binary response, EITHER "yes" OR "no" if the person is being genuine or not
    """

prompt_template2 = PromptTemplate(input_variables=["text"], template=template2, output_parser=output_parser2)
answer_chain2 = LLMChain(llm=llm2, prompt=prompt_template2)

print(answer_chain2.run("I learned Python a lot, it was very fun! I learned about for-loops, while-loops, print statements, if-else statements, and more! I learnt so much from this experience! Thank you SkillMap for the beautifully generated roadmap you ever-so mindfully provided to me! My experience with this application was truly remarkable! Twas was something to behold!"))