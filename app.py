import requests
import streamlit as st

# ====== Dify API Key ======
dify_api_key = "app-PMf4o3QiTPjrn56QjBpAdQo9"
url = "https://api.dify.ai/v1/chat-messages"

# ====== Streamlit Page Config ======
st.set_page_config(page_title="Recipe Chatbot", page_icon="🥘")

st.title("🍳 Recipe Chatbot")

# ====== Initialize session state ======
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ====== Display previous chat messages ======
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ====== User Input ======
prompt = st.chat_input("Enter your question about recipes")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Placeholder for assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {dify_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "conversation_id": st.session_state.conversation_id,
            "user": "aianytime",
            "files": []
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            full_response = response_data.get('answer', 'No response received.')
            st.session_state.conversation_id = response_data.get("conversation_id", st.session_state.conversation_id)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        # Display assistant response and save in session state
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
