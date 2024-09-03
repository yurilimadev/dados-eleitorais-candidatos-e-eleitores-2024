import streamlit as st

st.set_page_config(page_title="Eleitoral Analysis", layout='wide')

st.title("Analise Eleitorais Municipal 2024")
st.subheader("Escolha a Análise:")

app_options = ["Eleitores", "Candidatos"]
selected_app = st.selectbox("Análise", app_options,
                            index=None, placeholder="Selecione a Análise...")

if selected_app == "Eleitores":
    from my_pages import app_eleitores
    app_eleitores.app_eleitores()
elif selected_app == "Candidatos":
    from my_pages import app_candidatos
    app_candidatos.app_candidatos()
