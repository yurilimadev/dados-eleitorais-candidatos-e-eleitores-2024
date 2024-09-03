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


def create_icon_link(icon, link, text, descricao):

    col1, col2 = st.columns([0.1, 1])
    with col1:
        st.image(icon, width=50)
    with col2:
        st.subheader(f"[{text}]({link})")
        st.markdown(descricao)


# Título do rodapé
st.markdown("<h3 style='text-align: left;'>Veja meu portfólio ou se quiser bater um papo 😉</h3>",
            unsafe_allow_html=True)
col1, col2 = st.columns(2, gap='small')

with col1:

    create_icon_link("images/github-mark-white.svg",
                     "https://github.com/streamlit", "GitHub", "Você vai ver os últimos projetos que tenho trabalhado para construir minha carreira na tecnologia.")
    create_icon_link("images/instagram-round-white.svg",
                     "https://streamlit.io/newsletter", "Instagram", "Você pode ver minha rotina e o que venho aprendendo na faculdade e aplicando nos stories.")

with col2:
    create_icon_link("images/Youtube_white.svg",
                     "https://www.youtube.com/@yurilimaexplorandodados", "YouTube", "Você pode acompanhar as apresentações dos meus projetos em vídeo e discussões sobre futuros temas sobre tecnologia e sociedade.")
    create_icon_link("images/linkedin-round-white.svg",
                     "https://www.linkedin.com/in/yuri-lima-dev/", "LinkedIn", "Aqui podemos nos comunicar sobre possíveis colaborações e discussões sobre meus últimos projetos.")

# Customização CSS (opcional)
st.markdown("""
<style>
a:link, a:visited {
  color: white;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}

a:hover, a:active {
  color:hotpink;
}
.st-emotion-cache-ocqkz7 {
    display: flex;
    flex-wrap: wrap;
    -webkit-box-flex: 1;
    flex-grow: 1;
    -webkit-box-align: stretch;
    align-items: center;
    gap: 1rem;
}
</style>
""", unsafe_allow_html=True)
