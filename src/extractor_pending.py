from typing import Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field


class Movie(BaseModel):
    """Information about the movie"""
    #Sent to the LLM
    
    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    number: int = Field(description="The number of feature films directed by the director of a specified movie before the specified movie's release date. If not found, return -1")
