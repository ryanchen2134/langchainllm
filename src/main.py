from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import  AgentExecutor, create_openai_tools_agent

from langchain_community.agent_toolkits.load_tools import load_tools
from re import sub

# API Secret Key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Code example used however that version of langchain is deprecated
# langchain is now 0.3.0 and langchain-open is 0.2.0
# As such, the initiator code has a few other requirements
# Not doing this will cause an "insuffient quota" error from OpenAI endpoint despite that not being the case
model = ChatOpenAI( #gpt-4o-mini    #-2024-07-18
  model="gpt-4o-mini", #https://platform.openai.com/docs/models/gpt-3-5-turbo , https://openai.com/api/pricing/
  # this one is 20x cheaper at max than gpt-3.5-turbo and performs better
  temperature=0, 
  api_key=openai_api_key,
  max_retries=2,
  timeout=None,
  
  #debug
#   stream_options={"include_usage": True},
#   include_response_headers=True
)
tools = load_tools(["wikipedia"], llm=model)
prompt = ChatPromptTemplate.from_messages(
  [
    ("system", """You are a helpful research assistant, and your job is to
                  retrieve information about movies and movie directors. Think
                  through the questions you are asked step-by-step."""),
    ("human", """How many FEATURE FILMS did the director of the {year} movie 
                 {name} direct before they made {name}? First, find who
                 directed {name}. Then, look at their filmography. Find all the
                 feature-length movies they directed before {name}. Only 
                 consider movies that were released. Lastly, count up how many 
                 movies this is. Think step-by-step and write them down. When 
                 you have an answer, say, 'The number is: ' and give the
                 answer."""),
    MessagesPlaceholder("agent_scratchpad")
  ]
)
agent = create_openai_tools_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=6)

def prior_films(year, film):
  resp = agent_executor.invoke({"year": year, "name": film})
    # This is an example of a prompt template, which streamline argument passing into the 
    # HumanMessage
  return(resp['output'])


print(prior_films(2007, "Death Proof"))