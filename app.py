"""Streamlit app example."""
import os
import uuid
import json
import requests
import streamlit as st

DOMAIN = "https://gavinzli-news.hf.space"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.environ.get("HF_TOKEN")}'
}
STOCK = ["AAPL","ADBE","AMD","AMZN","ARM","ASML","AVGO","BRK.B","BTC","CHAU","COIN","CVNA",
         "DXYZ","GBTC","GOOG","GOOGL","KULR","MARA","META","MRVL","MSFT","MSTR","NBIS",
         "NFLX","NVDA","PDD","PLTR","QCOM","QQQ","QUBT","RDDT","ROKU","RR","SPY","TEM","TSLA"]

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
    st.session_state.user_id = str(uuid.uuid4())

with st.sidebar:
    st.header("Symbols Selection")
    symbols = st.multiselect("Select stocks", STOCK, default=["AAPL"])
    mode = st.selectbox("Mode", ["research", "stream"])
    retrivers = st.multiselect("Retrievers", ["duckduckgo", "google"], default=["duckduckgo"])

def get_research(query):
    """
    Sends a POST request to the research endpoint with the given query.

    Args:
        query (str): The search query to be sent in the request payload.

    Returns:
        str: The response text from the research endpoint.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the request.
    """
    payload = json.dumps({
        "query": query,
        "symbols": symbols,
        "headers": {
            "retrievers": ",".join(retrivers)
        }
    })
    response = requests.request(
        "POST", f"{DOMAIN}/research", headers=HEADERS, data=payload, timeout=100)
    return response.text

def get_answer(query):
    """
    Sends a query to a specified URL and retrieves the answer from the response.

    Args:
        query (str): The query string to be sent.
        symbols (list): The symbols to be sent

    Returns:
        str: The answer extracted from the response.
    """
    payload = json.dumps({
            "query": query,
            "chat_id": st.session_state.chat_id,
            "user_id": st.session_state.user_id,
            "sybols": symbols,
            "web": False
            })
    contexts = []
    response_answer = ""
    api_response = requests.request(
        "POST", f"{DOMAIN}/stream", headers=HEADERS,data=payload, stream=True, timeout=60)
    for response_str in api_response.text.strip().split('\n\n'):
        response_list = response_str.split('\n')
        response_str = response_list[1]
        json_object = json.loads(response_str.replace("data: ", ""))
        if "answer" in json_object:
            response_answer = response_answer + json_object['answer']
        elif "context" in json_object:
            contexts.append(json_object['context'])
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
    if mode == 'stream':
        answer = get_answer(prompt)
    else:
        answer = get_research(prompt)
    with st.chat_message("assistant"):
        response_content = st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
