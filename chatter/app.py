import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(page_title='Chatter', page_icon='🤖')

load_dotenv()

USER_AVATAR = '👤'
BOT_AVATAR = '🤖'
OPENAI_MODEL = 'gpt-4o'
DOCUMENT_STORAGE = Path.home() / 'Documents' / 'chatter'
DB_NAME = 'chat_history.json'
DB_LOCATION = DOCUMENT_STORAGE / DB_NAME
CUSTOM_STYLESHEET = 'styles.css'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Ensure openai_model is initialized in session state
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = OPENAI_MODEL


# Load chat history from JSON file
def load_chat_sessions():
    if DB_LOCATION.exists():
        with DB_LOCATION.open() as file:
            return json.load(file)
    return []


# Save chat history to JSON file
def save_chat_sessions(chat_sessions):
    with DB_LOCATION.open('w') as file:
        json.dump(chat_sessions, file)


# Load chat sessions on app start
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = load_chat_sessions()
    st.session_state.current_session = None


with open(CUSTOM_STYLESHEET) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar with chat sessions and a button to create a new session
with st.sidebar:
    st.write("<h1 class='sidebar-title'>Chat Sessions</h1>", unsafe_allow_html=True)
    for i, session in enumerate(st.session_state.chat_sessions):
        session_name = session.get('name', f'Session {i+1}')
        if st.button(session_name):
            st.session_state.current_session = i

    if st.button('New Chat Session'):
        new_session = {'name': '', 'messages': []}
        st.session_state.chat_sessions.append(new_session)
        st.session_state.current_session = len(st.session_state.chat_sessions) - 1

# Ensure a session is selected
if st.session_state.current_session is None and st.session_state.chat_sessions:
    st.session_state.current_session = 0

# Display chat messages for the current session
if st.session_state.current_session is not None:
    current_session = st.session_state.chat_sessions[st.session_state.current_session]
    for message in current_session['messages']:
        avatar = USER_AVATAR if message['role'] == 'user' else BOT_AVATAR
        with st.chat_message(message['role'], avatar=avatar):
            st.markdown(message['content'])

    # Main chat interface
    if prompt := st.chat_input('How can I help?'):
        current_session['messages'].append({'role': 'user', 'content': prompt})

        # Set session name if it's the first question
        if not current_session['name']:
            summary_response = client.chat.completions.create(
                model=st.session_state['openai_model'],
                messages=[
                    {
                        'role': 'system',
                        'content': 'Summarize the following prompt in a few words.',
                    },
                    {'role': 'user', 'content': prompt},
                ],
                max_tokens=10,
            )
            if summary := summary_response.choices[0].message.content:
                current_session['name'] = summary.strip()

        with st.chat_message('user', avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message('assistant', avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ''
            for response in client.chat.completions.create(
                model=st.session_state['openai_model'],
                messages=current_session['messages'],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ''
                message_placeholder.markdown(full_response + '|')
            message_placeholder.markdown(full_response)
        current_session['messages'].append(
            {'role': 'assistant', 'content': full_response}
        )

    # Save chat sessions after each interaction
    save_chat_sessions(st.session_state.chat_sessions)
