import streamlit as st
from google import genai
from google.genai import types
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="My Voice AI App", page_icon="🎙️")

st.title("🤖 Voice & Text AI සහයකයා")

# 1. API Key සකස් කිරීම
client = genai.Client(api_key="AQ.Ab8RN6LqhdAmULbLwIyVTkGjQh56SJtLoB-hp7nM-oW404xcjA")

# 2. Sidebar Settings
st.sidebar.title("⚙️ AI සැකසුම්")
role = st.sidebar.selectbox(
    "AI එකේ චරිතය තෝරන්න:",
    ["සාමාන්‍ය සහයකයා", "Coding උපදේශකයා", "ව්‍යාපාරික උපදේශකයා"]
)

instructions = {
    "සාමාන්‍ය සහයකයා": "You are a helpful AI assistant. Respond clearly.",
    "Coding උපදේශකයා": "You are an expert software developer.",
    "ව්‍යාපාරික උපදේශකයා": "You are a business consultant."
}

# 3. Session State සකස් කිරීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Voice Input කොටස (Mic Icon)
st.write("🎙️ **කතා කර ප්‍රශ්න ඇසීමට පහත මයික්‍රෆෝන් ලකුණ ඔබන්න:**")
audio_bytes = audio_recorder(text="", recording_color="#e84c3d", neutral_color="#6aa84f", icon_size="2x")

# Chat History පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = None
ai_response = None

# Voice Audio එකක් ලැබුණි නම් Gemini වෙත යැවීම
if audio_bytes:
    with st.spinner("ඔබේ හඬ සෙවීම් සිදුකරයි..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/wav",
                ),
                "Listen to this audio prompt and respond accurately."
            ],
            config={"system_instruction": instructions[role]}
        )
        prompt = "🎙️ [Voice Message]"
        ai_response = response.text

# Text Input එකක් ලැබුණි නම්
text_input = st.chat_input("නැතහොත් මෙතැන ටයිප් කරන්න...")
if text_input:
    prompt = text_input
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"system_instruction": instructions[role]}
    )
    ai_response = response.text

# Process and Display Results
if prompt and ai_response:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})