import streamlit as st
from agents import ecobuddy_graph

st.set_page_config(page_title="EcoBuddy", page_icon="🌱", layout="centered")
st.title("🌱 EcoBuddy: AI Sustainability Guide")

item = st.text_input("Enter a product or item (e.g., 'Single-use plastic water bottle'):")

if st.button("Analyze Product"):
    if item.strip():
        with st.spinner("EcoBuddy agents collaborating..."):
            result = ecobuddy_graph.invoke({
                "user_query": item, 
                "impact_data": "", 
                "alternatives": "", 
                "gamification_update": "", 
                "final_output": ""
            })
            st.markdown(result["final_output"])
    else:
        st.warning("Please enter a product to analyze.")