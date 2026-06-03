import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# This creates the global variable 'supabase' that all your files are looking for
supabase = get_supabase_client()