import streamlit as st
from crews.data_analysis_crew import CrewDataAnalyzer




def CrewDataAnalyzer() -> str:
    ...

# ===== Streamlit App =====
def render_post_page():
    st.title("👩‍⚕️ Assistente de Saúde - Análise Vacinal com IA")

    uploaded_file = st.file_uploader("📎 Envie a planilha Excel de vacinação", type=["xlsx", "xls"])
    user_request = st.text_area("❓ O que deseja saber?", placeholder="Ex: Quais vacinas Cláudio Lucas está faltando?")

    if uploaded_file and user_request:
        with st.spinner("🧠 Analisando dados com inteligência artificial..."):
            file_bytes = uploaded_file.read()
            contexto = CrewDataAnalyzer(file_bytes)

            if contexto.startswith("❌"):
                st.error(contexto)
                return

            resposta = DataAnalysisCrew()

            st.success("✅ Análise concluída!")
            st.markdown("### 🤖 Resposta do assistente:")
            st.write(resposta)
