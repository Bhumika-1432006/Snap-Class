import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# Use this property to access the client in your db.py files
@property
def supabase():
    return get_supabase_client()