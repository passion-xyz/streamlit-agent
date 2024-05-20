from langchain.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.tools import StructuredTool
from memory import entities
import json

class UpdateProfile(BaseModel):
    key: str = Field(description="the key of the data to be updated.")
    value: List[str] = Field(description="the new data to be added to the human's profile.")

def update_human_profile(entities, key, content):
    entities[key]['content'].extend(content)
    print("\n\n" + key + " has been updated.")
    print("-------")
    print(entities)
    print("-------")
    #print(json.dumps(entities, indent=4))

def update_profile(key: str, value: List[str]):
    """If the human's message presents a new piece of information about their profile, then update their profile."""
    update_human_profile(entities, key, value)
    return "\n\nThe human's profile has been updated"

# Create the StructuredTool directly
update_profile_tool = StructuredTool.from_function(
    func=update_profile,
    args_schema=UpdateProfile,
    name="update_profile",
    description="Updates the profile with given key and value."
)

entities_extraction_tools = [
    update_profile_tool
]
