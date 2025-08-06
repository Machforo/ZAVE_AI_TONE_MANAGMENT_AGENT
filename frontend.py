import streamlit as st
import requests

# --- API Base URL ---
API_BASE = "http://127.0.0.1:5000/api"

# --- Page Setup ---
st.set_page_config(page_title="Tone Adaptive Chatbot", layout="centered")
st.title("🧠 Tone-Adaptive Chatbot")

# --- Session State Initialization ---
for key, default in {
    "user_id": None,
    "chat_history": [],
    "chat_active": False,
    "chat_ended": False,
    "tone_feedback": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- User Profile Form ---
with st.expander("👤 Setup / Update Your Profile", expanded=not st.session_state["user_id"]):
    with st.form("user_form"):
        user_id = st.text_input("User ID", value=st.session_state.user_id or "")
        name = st.text_input("Name")
        email = st.text_input("Email")
        avatar_url = st.text_input("Avatar URL")
        location = st.text_input("Location")
        verbose = st.checkbox("Verbose Communication Style", value=True)
        submit_profile = st.form_submit_button("Submit / Update User")

    if submit_profile:
        payload = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "avatar_url": avatar_url,
            "location": location,
            "communication_style": {"verbose": verbose},
            "interaction_history": {}
        }
        try:
            res = requests.post(f"{API_BASE}/users", json=payload)
            if res.status_code == 200:
                st.success("✅ User profile updated.")
                st.session_state.user_id = user_id
                st.session_state.chat_active = True
                st.session_state.chat_ended = False
                st.session_state.chat_history.clear()
            else:
                st.error(f"❌ Failed to update user: {res.text}")
        except Exception as e:
            st.error(f"🚨 Exception: {e}")

# --- View User Info ---
if st.session_state.user_id:
    with st.expander("📄 View User Info"):
        try:
            res = requests.get(f"{API_BASE}/users/{st.session_state.user_id}")
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.warning("⚠️ Could not fetch user profile.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Sidebar Tone Feedback ---
if st.session_state.user_id and not st.session_state.chat_ended:
    with st.sidebar:
        st.markdown("🎯 **Tone Feedback**")
        st.session_state.tone_feedback = st.selectbox(
            "Choose tone for next message",
            ["", "friendly", "formal", "humorous", "professional"]
        )

# --- Chat Interface ---
if st.session_state.user_id and st.session_state.chat_active and not st.session_state.chat_ended:
    st.subheader("💬 Talk to the Bot")

    # Display Chat History
    for i, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"🗣️ {chat['user']}  \n_Tone: {chat.get('tone', 'default')}_")
        with st.chat_message("assistant"):
            st.markdown(f"💡 {chat['bot']}")

        # Optional thumbs up/down feedback
        if "feedback" not in chat:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key=f"thumbs_up_{i}"):
                    st.session_state.chat_history[i]["feedback"] = "positive"
                    st.success("✅ Feedback submitted.")
            with col2:
                if st.button("👎", key=f"thumbs_down_{i}"):
                    st.session_state.chat_history[i]["feedback"] = "negative"
                    st.success("✅ Feedback submitted.")

    # Chat Input
    prompt = st.chat_input("Type your message...")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        if any(word in prompt.lower() for word in {"bye", "exit", "quit", "goodbye"}):
            st.session_state.chat_history.append({
                "user": prompt,
                "bot": "Goodbye! The session has ended.",
                "tone": "neutral"
            })
            st.session_state.chat_active = False
            st.session_state.chat_ended = True
            st.success("👋 Chat session ended.")
        else:
            payload = {
                "user_id": st.session_state.user_id,
                "user_input": prompt,
                "tone_feedback": st.session_state.tone_feedback or None
            }
            try:
                res = requests.post(f"{API_BASE}/chats", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    bot_reply = data.get("response", "...")
                    tone_used = data.get("tone_applied", "default")

                    st.session_state.chat_history.append({
                        "user": prompt,
                        "bot": bot_reply,
                        "tone": tone_used
                    })

                    with st.chat_message("assistant"):
                        st.markdown(bot_reply)
                else:
                    st.error("❌ Bot failed to respond.")
            except Exception as e:
                st.error(f"❌ Exception: {e}")

# --- Chat Summary ---
if st.session_state.chat_ended and st.session_state.chat_history:
    st.subheader("📜 Chat Summary")
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(f"🗣️ {chat['user']}  \n_Tone: {chat.get('tone', 'default')}_")
        with st.chat_message("assistant"):
            st.markdown(f"💡 {chat['bot']}")

    if st.button("🔄 Start New Chat"):
        st.session_state.chat_active = True
        st.session_state.chat_ended = False
        st.session_state.chat_history.clear()
        st.rerun()
