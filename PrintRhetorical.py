import streamlit as st

def write_rhetorical_functions():
    functions_file_path = "./rhetorical_functions.txt"

    with st.expander("Rhetorical Function", expanded=True):
        functions_file = open(functions_file_path, 'r')
        for sentence in functions_file:
            st.write(sentence)
