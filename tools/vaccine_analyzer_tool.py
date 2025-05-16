from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import unicodedata

class TextoPacientes(BaseModel):
    dados_texto: str = Field(..., description="Texto com nome, idade e vacinas aplicadas dos pacientes")

    class Config:
        arbitrary_types_allowed = True

class AnalisarVacinacao(BaseTool):
    name: str = "analisar_vacinacao"
    description: str = "Analisa vacinas faltantes de pacientes conforme o calendário PNI 2025."
    args_schema: Type[BaseModel] = TextoPacientes

    def _run(self, dados_texto: str) -> str:
        calendario_pni = {
            "bcg": {"descricao": "Ao nascer"},
            "hepatite b": {"descricao": "Ao nascer"},
            "penta": {"descricao": "Doses aos 2, 4 e 6 meses"},
            "vip": {"descricao": "Doses aos 2, 4 e 6 meses"},
            "pneumo 10": {"descricao": "Doses aos 2, 4 e reforço aos 12 meses"},
            "meningo c": {"descricao": "Doses aos 3, 5 e reforço aos 12 meses"},
            "rotavirus": {"descricao": "Doses aos 2 e 4 meses"},
            "tríplice viral": {"descricao": "Doses aos 12 e 15 meses"},
            "febre amarela": {"descricao": "1ª dose aos 9 meses e reforço aos 4 anos"},
            "varicela": {"descricao": "1ª dose aos 15 meses e reforço aos 4 anos"},
            "hepatite a": {"descricao": "Dose única aos 15 meses"},
            "dtp": {"descricao": "1ª dose aos 15 meses e reforço aos 4 anos"},
            "gripe": {"descricao": "Anual, conforme campanhas"}
        }

        def normalizar(texto):
            return unicodedata.normalize('NFKD', texto.lower()).encode('ASCII', 'ignore').decode()

        relatorio = {}
        pacientes = dados_texto.strip().split("---")

        for paciente in pacientes:
            linhas = [l.strip() for l in paciente.strip().split("\n") if l.strip()]
            nome = next((l.replace("Nome: ", "").strip() for l in linhas if l.lower().startswith("nome:")), "Desconhecido")
            idade = next((int(l.replace("Idade: ", "").strip().split()[0]) for l in linhas if l.lower().startswith("idade:")), None)

            vacinas_aplicadas = [
                normalizar(l.split(":")[0].replace("-", "").strip())
                for l in linhas[2:] if ":" in l
            ]

            pendentes = []
            for vacina, info in calendario_pni.items():
                if normalizar(vacina) not in vacinas_aplicadas:
                    pendentes.append(f"{vacina.title()} - {info['descricao']}")

            relatorio[nome] = {
                "idade": idade,
                "pendentes": pendentes
            }

        saida = ""
        for nome, dados in relatorio.items():
            saida += f"👤 {nome} ({dados['idade']} anos):\n"
            if dados["pendentes"]:
                for pend in dados["pendentes"]:
                    saida += f"  - {pend}\n"
            else:
                saida += "  ✅ Vacinação em dia\n"
            saida += "\n"

        return saida.strip() if saida else "✅ Todos os pacientes estão com vacinação em dia."
