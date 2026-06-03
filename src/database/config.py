import streamlit as st
from supabase import create_client

# Define the client creation function
@st.cache_resource
def get_supabase_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# Force the creation of the global variable
supabase = get_supabase_client()