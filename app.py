"""Streamlit app example."""
import os
import uuid
import json
import requests
import streamlit as st

URL = "https://gavinzli-news.hf.space/stream"
general_category_options = ["suggestion", "compliment", "complain"]

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.user_id = str(uuid.uuid4())

with st.sidebar:
    # st.header("LLM selection")
    # st.selectbox("Select LLM", ["GPT-4o"], key="llm_selection")
    st.header("Data selection")
    with st.form(key='data_selection'):
        selected_general_category = st.pills(
            "Feedback Type",general_category_options, selection_mode="multi")
        submitted = st.form_submit_button(label='Confirm selected data')

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
            "chat_id": st.session_state.chat_id,
            "user_id": st.session_state.user_id,
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
