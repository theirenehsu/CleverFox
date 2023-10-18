import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = 'Home'


def set_page():
    st.session_state.page = st.session_state.nav


def home():
    st.session_state.page = 'Home'


if st.session_state.page == 'Home':
    st.sidebar.radio("Navigation", ['Home', 'Summary', 'Twitter', 'Facebook'], key='nav', on_change=set_page)
else:
    st.sidebar.button('Back to Home', on_click=home)

if st.session_state.page == 'Home':
    st.title('Home')
elif st.session_state.page == 'Summary':
    st.title('Summary')
elif st.session_state.page == 'Twitter':
    st.title('Twitter')
else:
    st.title('Facebook')
