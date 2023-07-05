from pydantic import BaseModel, Field, validator
from typing import List, Optional, Type
from langchain.tools import tool
from langchain.tools import BaseTool, Tool, StructuredTool
from memory import entities


def update_human_profile(entities, key, content):
    if key == 'goals':
        name = content.get('name', '')
        description = content.get('description', '')
        achieved = content.get('achieved', False)
        entities[key]['content'].append(
            {'name': name, 'description': description, 'achieved': achieved})
    else:
        entities[key]['content'].extend(content)
        print("\n" + key + " has been updated.")


class UpdateProfile(BaseModel):
    key: str = Field(
        description="the key of the data to be updated.")
    value: List[str] = Field(
        description="the new data to be added to the human's profile.")


@tool("update_profile", return_direct=True, args_schema=UpdateProfile)
def update_profile(key: str, value: List[str]):
    """If the human's message presents a new piece of information about their profile, then update their profile."""
    update_human_profile(entities, key, value)

    print(entities)

    return "the human's profile has been updated"


agent_tools = [
    update_profile
]
