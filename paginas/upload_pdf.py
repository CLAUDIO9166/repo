import os
import time
import streamlit as st
import pandas as pd
import json
from crews.data_analysis_crew import CrewDataAnalyzer  

# Configuração do diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def process_file(file_path, file_type):
    # Função genérica de leitura
    if file_type == 'pdf':
        return {"type": "pdf", "path": file_path}
    elif file_type in ['xlsx', 'xls']:
        df = pd.read_excel(file_path)
        return {"type": "dataframe", "data": df}
    elif file_type == 'csv':
        df = pd.read_csv(file_path)
        return {"type": "dataframe", "data": df}
    elif file_type == 'json':
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"type": "json", "data": data}
    else:
        return {"type": "unknown", "data": None}

def render_upload_page():
    st.title("Central de Análise de Arquivos - Equipe de Agentes")

    st.write("Envie arquivos (PDF, Excel, JSON, CSV) para análise personalizada.")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["pdf", "xlsx", "xls", "csv", "json"])

    if uploaded_file is not None:
        try:
            # Salva o arquivo
            file_path = os.path.join(TEMP_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Upload realizado com sucesso: {uploaded_file.name}")

            # Pergunta ao usuário o que deseja extrair
            user_request = st.text_input("Digite o que você quer saber do arquivo (ex: 'listar crianças de 6 a 10 anos', 'quem não tomou vacina da gripe')")

            if user_request:
                with st.spinner("Analisando com a equipe de agentes..."):
                    time.sleep(1)

                    file_type = uploaded_file.name.split(".")[-1].lower()
                    content = process_file(file_path, file_type)

                    # Chama a "equipe de agentes"
                    crew = CrewDataAnalyzer(content, user_request)
                    resultado = crew.kickoff()

                st.text_area("Resultado da análise:", resultado, height=300)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
