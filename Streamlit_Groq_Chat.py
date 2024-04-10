import streamlit as st
from groq import Groq

client = Groq(api_key = os.environ.get("GROQ_API_KEY"),)
st.title('Groq Chat')

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_prompt: str = st.text_area('System Prompt', value = 'You are a helpful assistant.')
    temperature: float = st.slider('Temperature', 0.00, 2.00, 0.70, step = 0.01)
    max_tokens: int = st.slider('Max Tokens', 1, 32768, 32768, step = 1)
    top_p: float = st.slider('Top_P', 0.00, 1.00, 1.00, step = 0.01)

    if st.button('New Chat'):
        st.session_state.messages = []
        st.experimental_rerun()

user_msg: str = st.chat_input('Say something...')

if user_msg:
    st.session_state.messages.append(
        {
            'role': 'user',
            'content': user_msg
        }
    )

    messages = [{'role': 'system', 'content': system_prompt}] + st.session_state.messages

    chat_completion = client.chat.completions.create(
        messages = messages,
        model = 'mixtral-8x7b-32768',
        temperature = temperature,
        max_tokens = max_tokens,
        top_p = top_p,
        stop = None,
        stream = False
    )
    response = chat_completion.choices[0].message.content

    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content': response
        }
    )

    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'], unsafe_allow_html = True)






