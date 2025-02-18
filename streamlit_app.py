from dotenv import load_dotenv
import os
import json
import requests
import streamlit as st

load_dotenv()

URL = "https://gavinzli-news.hf.space/stream"
def get_answer(query):
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
    answer = ""
    response = requests.request("POST", URL, headers=headers, data=payload, stream=True)
    for response_str in response.text.strip().split('\n\n'):
        response_list = response_str.split('\n')
        response_str = response_list[1]
        json_object = json.loads(response_str.replace("data: ", ""))
        # if "context" in json_object:
        #     contexts.append(json_object['context'])
        if "answer" in json_object:
            answer = answer + json_object['answer']
        # elif "questions" in json_object:
        #     questions = json_object['questions']
    return answer

# Show title and description.
# st.title("💬 Chatbot")
# st.write(
#     "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
#     "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
# )

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# token = st.text_input("Huggingface Space Token", type="password")
# if not token:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

# # Create an OpenAI client.
# client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    # stream = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": m["role"], "content": m["content"]}
    #         for m in st.session_state.messages
    #     ],
    #     stream=True,
    # )

    # Stream the response to the chat using `st.write_stream`, then store it in
    # session state.
    answer = get_answer(prompt)
    with st.chat_message("assistant"):
        response = st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": response})
