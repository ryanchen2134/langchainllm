from langchain_openai import ChatOpenAI

from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents import  AgentExecutor, create_openai_tools_agent
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_community.agent_toolkits.load_tools import load_tools
from re import sub

import json
from langchain_core.agents import AgentActionMessageLog, AgentFinish

from extractor_pending import Movie


from dotenv import load_dotenv
load_dotenv()

#langsmith tracks the calling chain of the API
from langsmith import Client
client = Client()


# Code example used however that version of langchain is deprecated
# langchain is now 0.3.0 and langchain-open is 0.2.0
# As such, the initiator code has a few other requirements
# Not doing this will cause an "insuffient quota" error from OpenAI endpoint despite that not being the case
model = ChatOpenAI( #gpt-4o-mini    #-2024-07-18
  model="gpt-4o-mini", #https://platform.openai.com/docs/models/gpt-3-5-turbo , https://openai.com/api/pricing/
  # this one is 20x cheaper at max than gpt-3.5-turbo and performs better
  temperature=0, 
#   api_key=openai_api_key, will find in environment
  max_retries=2,
  timeout=None,
  

  #debug
#   stream_options={"include_usage": True},
#   include_response_headers=True
)




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


tools = load_tools(["wikipedia"], llm=model)
agent = create_openai_tools_agent(model, tools, prompt)

# agent = create_openai_tools_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=24)

def prior_films(year, film):
  resp = agent_executor.invoke({"year": year, "name": film})
  return(resp['output'])

print(prior_films(2000, "The Matrix"))