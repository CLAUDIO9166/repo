from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import datetime
import pandas as pd
from io import BytesIO

class IdadeInput(BaseModel):
    planilha: BytesIO = Field(..., description="Arquivo Excel com data de nascimento dos pacientes")

    class Config:
        arbitrary_types_allowed = True

class CalcularIdadePacientes(BaseTool):
    name: str = "calcular_idade_pacientes"
    description: str = "Calcula a idade atual de pacientes com base na data de nascimento."
    args_schema: Type[BaseModel] = IdadeInput

    def _run(self, planilha: BytesIO) -> str:
        try:
            df = pd.read_excel(planilha)
            hoje = datetime.today()
            texto_resultado = ""

            for _, row in df.iterrows():
                nome = row.get("NOME", "Desconhecido")
                data_nasc = row.get("DATA NASC.", None)
                if pd.isna(data_nasc):
                    idade = "Data de nascimento não informada"
                else:
                    try:
                        nascimento = pd.to_datetime(data_nasc)
                        anos = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
                        idade = f"{anos} anos"
                    except Exception:
                        idade = "Data inválida"
                texto_resultado += f"Nome: {nome}, Idade: {idade}\n---\n"

            return texto_resultado.strip()
        except Exception as e:
            return f"Erro ao calcular idades: {str(e)}"
