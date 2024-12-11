import streamlit as st
from huggingface_hub import InferenceClient
from utils import *
from streamlit_extras.grid import grid

# ---------set up page config -------------#
st.set_page_config(page_title="Sonic Cosmo",
                   layout="centered",
                   page_icon="🐶",
                   initial_sidebar_state="collapsed")

# ---------set button css-------------#
st.markdown(custom_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
client = InferenceClient(token=st.secrets["huggingfacehub_api_token"])

# ---------set model ------------#
model_option = {"qwen2.5-72b": "Qwen/Qwen2.5-72B-Instruct",
                "qwen2.5-coder": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "llama3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
                "llama3.1-70b": "meta-llama/Meta-Llama-3.1-70B-Instruct",
                "llama3-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
                }

if "model_select" not in st.session_state:
    st.session_state.model_select = model_option.get("qwen2.5-72b")

# ------- Store conversations with session state --------#
if 'msg_history' not in st.session_state:

    st.session_state.msg_history = []

    system_message = """You are Sonic Cosmo, the friendly chatdog that provides helpful information.
    Look back at the chat history to find information if needed"""

    # system_message = """You are an AI assistant that are expert in coding."""

    st.session_state.msg_history.append(
        {"role": "system", "content": f"{system_message}"})

# -------Write chat history to UI --------#
for msg in st.session_state.msg_history:
    if msg['role'] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ------- Set up header --------#
with st.sidebar:
    model_select = st.selectbox(
        label="Choose a model", options=model_option.keys())
    st.session_state.model_select = model_option.get(model_select)
    st.write(f"**Model selected :** {st.session_state.model_select}")
    st.image("cosmo.jpg", width=150)
    st.subheader("Meet Sonic Cosmo")
    st.write(intro)

# ------- Set up buttons --------#
button_pressed = ""

btn_grid = grid(2, gap='small', vertical_align="top")

if btn_grid.button(EXAMPLE_PROMPTS[0]):
    button_pressed = EXAMPLE_PROMPTS[0]

elif btn_grid.button(EXAMPLE_PROMPTS[1]):
    button_pressed = EXAMPLE_PROMPTS[1]

elif btn_grid.button(EXAMPLE_PROMPTS[2]):
    button_pressed = EXAMPLE_PROMPTS[2]

elif btn_grid.button(EXAMPLE_PROMPTS[3]):
    button_pressed = EXAMPLE_PROMPTS[3]

# ---- Input field for users to continue the conversation -----#
if user_input := (st.chat_input("Type your message or click a button...") or button_pressed):

    # Append the user's input to the msg_history
    st.session_state.msg_history.append(
        {"role": "user", "content": user_input})

    # write current chat on UI
    st.chat_message("user").write(user_input)

    # ---- find keys words to activate function and append to chat history ----#
    if contains_any_keyword(user_input, ["video"]):

        video_var = video_search(user_input)
        st.session_state.msg_history.append({"role": "system",
                                             "content": f"Here is the youtube video for {user_input} : {video_var}"})

    if contains_any_keyword(user_input, ["weather", "rain"]):

        st.session_state.msg_history.append(
            {"role": "system", "content": f"Here is the weather forecast for today - {datetime_var}: {weather_var}"})

    if contains_any_keyword(user_input, ["time", "date"]):

        st.session_state.msg_history.append(
            {"role": "system", "content": f"Here are the date and time for today: {datetime_var}"})

    if contains_any_keyword(user_input, ["news", "headlines", "headline"]):

        st.session_state.msg_history.append(
            {"role": "system", "content": f"These are the news headlines for today - {datetime_var} : {news_var}"})

    # ----- Create a placeholder for the streaming response ------- #
    with st.empty():
        # Stream the response

        stream = client.chat_completion(
            model=st.session_state.model_select,
            messages=st.session_state.msg_history,
            temperature=0.6,
            max_tokens=4524,
            top_p=0.7,
            stream=True,)

        # st.write(stream['choices'][0]['message']['content'])

        # Initialize an empty string to collect the streamed content
        collected_response = ""

        # Stream the response and update the placeholder in real-time
        for chunk in stream:
            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                collected_response += chunk.choices[0].delta.content
                st.chat_message("assistant").write(collected_response)

    # Add the assistant's response to the conversation history
    st.session_state.msg_history.append(
        {"role": "assistant", "content": collected_response})

    # Keep history to 10, pop 2 item from the list
    if len(st.session_state.msg_history) >= 5:
        st.session_state.msg_history.pop(1)

    # play video if response contain youtube link but don't re-run script
    if "https://www.youtube.com/watch?" in collected_response and button_pressed != "Translate in Chinese":
        st.video(video_var)

    # rerun scripts for the other responses.
    else:
        st.rerun()
