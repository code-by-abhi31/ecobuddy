import streamlit as st
import uuid
from agents import ecobuddy_graph
from database import add_points, get_user_stats

st.set_page_config(page_title="EcoBuddy", page_icon="🌱", layout="centered")

st.title("🌱 EcoBuddy: AI Sustainability & ROI Guide")
st.caption("Analyze environmental impact, calculate ROI, and track eco-actions.")

# Static demo username (or tie to authentication later)
USER = "abhi_dev"

# Sidebar: Live cloud stats from Supabase
stats = get_user_stats(USER)
with st.sidebar:
    st.header("👤 Eco Profile")
    st.metric(label="Total Points", value=stats["total_points"])
    st.metric(label="Items Analyzed", value=stats["items_logged"])

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Render message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Box
# Chat Input Box
if user_input := st.chat_input("Ask Ecobuddy"):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    
    with st.chat_message("assistant"):
        with st.spinner("EcoBuddy is thinking..."):
            result = ecobuddy_graph.invoke({"user_query": user_input}, config=config)
            output = result["final_output"]
            st.markdown(output)
            
    # 1. SAVE THE MESSAGE FIRST
    st.session_state.messages.append({"role": "assistant", "content": output})
    
    # 2. THEN TRIGGER THE DATABASE AND RERUN
    if result.get("route_decision") == "PRODUCT":
        new_points = add_points(USER, user_input, points=10)
        st.toast(f"🌱 +10 Eco-points recorded to cloud! Total: {new_points}")
        st.rerun()