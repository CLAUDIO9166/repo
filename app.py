import streamlit as st
from streamlit_option_menu import option_menu
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.upload_pdf import render_upload_page
from paginas.post import render_post_page


st.sidebar.image("images/logo.png", use_container_width=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Agentic Platform",  # Título do menu
        options=["Home", "Post Agent", "Summary PDF"],  # Opções do menu
        icons=['house','file-earmark-text','cloud-upload'],
        menu_icon='robot',
        default_index=0,
        orientation="vertical" #teste com "horizontal"
    )

st.sidebar.image("images/powered.png", use_container_width=True)


# Conteúdo baseado na opção selecionada
if selected == "Home":
    render_welcome()

elif selected == "Post Agent":
    render_post_page()

elif selected == "Summary PDF":
    render_upload_page()

