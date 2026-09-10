import streamlit as st
from agents import ecobuddy_graph

st.set_page_config(page_title="EcoBuddy", page_icon="🌱", layout="centered")

if "last_result" not in st.session_state:
    st.session_state["last_result"] = ""

# Main Screen (No more fake coins sidebar)
st.title("🌱 EcoBuddy: AI Sustainability & ROI Guide")
st.caption("Analyze environmental impact and calculate your financial savings.")

item = st.text_input("Enter a product or item (e.g., 'Single-use plastic water bottle'):")

if st.button("Analyze Product"):
    if item.strip():
        with st.spinner("Analyzing footprint and calculating ROI..."):
            result = ecobuddy_graph.invoke({
                "user_query": item,
                "route_decision": "",
                "impact_data": "", 
                "alternatives": "", 
                "gamification_update": "", 
                "final_output": ""
            })
            st.session_state["last_result"] = result["final_output"]
            st.rerun()
    else:
        st.warning("Please enter a product to analyze.")

if st.session_state["last_result"]:
    st.markdown(st.session_state["last_result"])