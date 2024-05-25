import streamlit as st
from streamlit_chat import message
from streamlit_extras.stoggle import stoggle
import json

entities = {
    # ToDo
    "name": {
        "description": "This is the human's name. Human only has one name.",
        "content": [],
    },
    "likes": {
        "description": "Human's hobbies, preferences, tastes.",
        "content": [],
    },
    "dislikes": {
        "description": "Human's dislikes or hates.",
        "content": []
    },
    "traits": {
        "description": "Human's personality traits like introversion and extroversion.",
        "content": []
    }
}

import threading
from agents import AICompanionAgent, EntitiesExtractionAgent

from langchain.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.tools import StructuredTool

st.set_page_config(page_title='Character Creator', page_icon='💬', layout="wide", initial_sidebar_state='expanded')

def on_btn_click():
    del st.session_state.messages[:]

st.title("💬 Chatbot Configs")
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

greeting_from_agent = st.text_input("Greeting", "How can I help you?")

roleplay_prompt = st.text_area(
"Roleplay prompt",
"""Roleplay a fictional character, Rachel Greene, for which I will give you the details:
Rachel Greene is an ambitious, driven, and initially somewhat spoiled due to her upbringing. She is known for being kind, caring, occasional clumsiness, and deeply interested in arts and the lives of others; however, she can be insecure and sensitive at times. Rachel Greene's tone is friendly, cheerful and engaging, sometimes a bit playful or sarcastic in a light-hearted manner. Recently matched with Human on Tinder and she's open to exploring both casual and romantic relationships, excited to spark a fun and engaging conversation and get to know you better

The overall tone for Rachel Greene should fit well with the nature of online messaging, using abbreviations, slang, and emojis as appropriate. Each response should be short, concise. Some sample dialogue for reference.

Here's what Rachel Greene knows about the human:
{entities}

If Rachel Greene doesn't know something about the human, Rachel Greene will attempt to ask the human for that information. If the conversation dies down, Rachel Greene will try to ask more questions to keep it going.

Summary of long conversation:
{summary}

Past messages:
{messages_history}

Current messages:
Human: {input}
Rachel Greene:"""
)

entity_extraction_prompt = st.text_area(
"Entity Extraction Prompt",
"""{
    "name": {
        "description": "This is the human's name. Human only has one name.",
        "content": [],
    },
    "likes": {
        "description": "Human's hobbies, preferences, tastes.",
        "content": [],
    },
    "dislikes": {
        "description": "Human's dislikes or hates.",
        "content": []
    },
    "traits": {
        "description": "Human's personality traits like introversion and extroversion.",
        "content": []
    },
}"""
)

def update_human_profile(entities, key, content):
    print(f'entities {entities}')
    if key not in entities:
        entities[key] = {}
    if 'content' not in entities[key]:
        entities[key]['content'] = []
    for entity in content:
        entities[key]['content'].append(entity)
    with st.sidebar:
        entities_text = st.empty()
        entities_text.write(entities)
    return entities

def update_entities(new_entities):
    entities = new_entities
    print(f'update_entities {entities} to {new_entities}') 

def update_profile(key: str, value: List[str]):
    """If the human's message presents a new piece of information about their profile, then update their profile."""
    temp_entities = entities.copy()
    entity_extraction_prompt_json = entities
    try:
        entity_extraction_prompt_json = json.loads(entity_extraction_prompt)
        for key in entity_extraction_prompt_json:
            if key not in temp_entities:
                temp_entities[key] = {}
                temp_entities[key]['description'] = entity_extraction_prompt_json[key]['description']
                temp_entities[key]['content'] = []
    except json.JSONDecodeError as e:
        print(f'error {e}')
    temp_entities = update_human_profile(temp_entities, key, value)
    update_entities(temp_entities)

class UpdateProfile(BaseModel):
    key: str = Field(description="the key of the data to be updated.")
    value: List[str] = Field(description="the new data to be added to the human's profile.")
    
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

profile_update_prompt = st.text_area("Profile Update Prompt (profile_update_prompt)",
f"""Use your judgement and pick out the information you need from the human's new message, based on the following list of human's data:
{entity_extraction_prompt}
Use a tool to update the human's profile if new information is presented.
Don't update if there isn't new information from the human's message.
""")

companion_agent = AICompanionAgent(roleplay_prompt, verbose=True)
user_profile_updater = EntitiesExtractionAgent(tools=entities_extraction_tools, prompt=profile_update_prompt)

def on_input_change():
    user_input = st.session_state['user_input'] or ""
    st.session_state['messages'].append({"role": 'user', "content": user_input})
    st.session_state['messages'].append({"role": 'assistant', "content": companion_agent.talk(user_input, entities) or ""})

    data = user_profile_updater.update_user_profile(user_input)
    print(data)

st.title("💬 Chat")
chat_placeholder = st.empty()
with chat_placeholder.container():    
    message(greeting_from_agent, key=f"0_assistant")
    for i in range(len(st.session_state['messages'])):                
        is_user = st.session_state['messages'][i]['role'] == 'user'
        message(st.session_state['messages'][i]['content'], is_user=is_user, key=f"{i}_{st.session_state['messages'][i]['role']}")
    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")