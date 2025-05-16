from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import pandas as pd
from io import BytesIO

class PlanilhaInput(BaseModel):
    """Entrada da ferramenta de leitura de planilha de vacinação."""
    arquivo: BytesIO = Field(..., description="Arquivo Excel com os dados de vacinação")

    class Config:
        arbitrary_types_allowed = True

class LerPlanilhaVacinacao(BaseTool):
    name: str = "ler_planilha_vacinacao"
    description: str = "Lê uma planilha Excel com dados de vacinação e extrai nome, nascimento e vacinas aplicadas."
    args_schema: Type[BaseModel] = PlanilhaInput

    def _run(self, arquivo: BytesIO) -> str:
        try:
            df = pd.read_excel(arquivo)
            df = df.fillna("Não informado")
            texto_final = ""

            for _, row in df.iterrows():
                paciente = f"Nome: {row['NOME']}, Data Nasc: {row['"DATA NASC.:", None']}, Vacinas Aplicadas:\n"
                for vacina in df.columns[6:]:
                    valor = row[vacina]
                    if valor != "Não informado":
                        paciente += f"- {vacina}: {valor}\n"
                texto_final += paciente + "\n---\n"

            return texto_final.strip()

        except Exception as e:
            return f"❌ Erro ao processar planilha: {str(e)}"
