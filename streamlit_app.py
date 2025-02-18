"""Streamlit app example."""
import os
import json
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()

URL = "https://gavinzli-news.hf.space/stream"
def get_answer(query):
    """
    Sends a query to a specified URL and retrieves the answer from the response.

    Args:
        query (str): The query string to be sent.

    Returns:
        str: The answer extracted from the response.
    """
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ.get("token")}'
    }
    payload = json.dumps({
            "query": query,
            "chat_id": "string",
            "user_id": "string",
            "web": False
            })
    # contexts = []
    response_answer = ""
    api_response = requests.request("POST", URL, headers=headers,
                                    data=payload, stream=True, timeout=60)
    for response_str in api_response.text.strip().split('\n\n'):
        response_list = response_str.split('\n')
        response_str = response_list[1]
        json_object = json.loads(response_str.replace("data: ", ""))
        # if "context" in json_object:
        #     contexts.append(json_object['context'])
        if "answer" in json_object:
            response_answer = response_answer + json_object['answer']
        # elif "questions" in json_object:
        #     questions = json_object['questions']
    return response_answer

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = get_answer(prompt)
    with st.chat_message("assistant"):
        response_content = st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
