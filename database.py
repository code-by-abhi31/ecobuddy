import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client and cache it so Streamlit doesn't reconnect on every button click
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

def add_points(username: str, item: str, points: int = 10) -> int:
    # Check if user already exists
    user_res = supabase.table("users").select("*").eq("username", username).execute()
    
    if not user_res.data:
        # Insert new user
        supabase.table("users").insert({
            "username": username, 
            "total_points": points, 
            "items_logged": 1
        }).execute()
        new_total = points
    else:
        # Update existing user
        current_points = user_res.data[0]["total_points"]
        current_items = user_res.data[0]["items_logged"]
        new_total = current_points + points
        
        supabase.table("users").update({
            "total_points": new_total, 
            "items_logged": current_items + 1
        }).eq("username", username).execute()
    
    # Insert audit record into logs
    supabase.table("logs").insert({
        "username": username, 
        "item": item, 
        "points_awarded": points
    }).execute()
    
    return new_total

def get_user_stats(username: str) -> dict:
    res = supabase.table("users").select("total_points, items_logged").eq("username", username).execute()
    if res.data:
        return {
            "total_points": res.data[0]["total_points"], 
            "items_logged": res.data[0]["items_logged"]
        }
    return {"total_points": 0, "items_logged": 0}