import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
from app.services import initialize_components, generate_answer

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# User database
USERS_DB = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.components_initialized = False

# Initialize components if not already done
if not st.session_state.get('components_initialized', False) and st.session_state.logged_in:
    initialize_components()
    st.session_state.components_initialized = True

st.title("🔐 Role-Based Chatbot")

# Login page
if not st.session_state.logged_in:
    st.subheader("Login to continue")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = USERS_DB.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Chat interface
else:
    st.success(f"Welcome, {st.session_state.username} (Role: {st.session_state.role})")
    
    # Chat input
    query = st.text_area("Ask your question", height=100)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Ask"):
            if not query.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Generating answer..."):
                    try:
                        if not st.session_state.get('components_initialized', False):
                            initialize_components()
                            st.session_state.components_initialized = True
                            
                        answer = generate_answer(query, st.session_state.role)
                        st.markdown("### Answer:")
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.components_initialized = False
            st.rerun()

    # Display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if query and st.session_state.get('last_query') != query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.last_query = query
