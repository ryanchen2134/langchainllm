from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

#load the environment variables
from dotenv import load_dotenv
load_dotenv()

#langsmith tracks the calling chain of the API
from langsmith import Client
client = Client()

model = ChatOpenAI( #gpt-4o-mini    #-2024-07-18
  model="gpt-4o-mini",
  temperature=0,
  max_retries=2,
  timeout=None)




from langchain_community.agent_toolkits.load_tools import load_tools
from extractor_pending import Movie
tools = load_tools(["wikipedia"], llm=model)
model.bind_functions()



from langgraph.prebuilt import create_react_agent

#tools need to have this
from langgraph.prebuilt.chat_agent_executor import AgentState

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
        ("placeholder", "{messages}"),
    ]
)
def _modify_state_messages(state: AgentState):
    return prompt.invoke({"messages": state["messages"]}).to_messages()

app = create_react_agent(model, tools, state_modifier=_modify_state_messages)

def prior_films(year, film):
#   messages = app.invoke({"messages": [("human", query)]})
    messages = app.invoke({"year": year, "name": film})
    print(
        {
            "input": "prior_films(2007, 'Death Proof')",
            "output": messages["messages"][-1].content,
        }
    )


prior_films(2007, "Death Proof")


