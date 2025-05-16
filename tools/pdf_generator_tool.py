from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from fpdf import FPDF
import os

class TextoRelatorio(BaseModel):
    conteudo: str = Field(..., description="Texto com os dados que serão convertidos em PDF")

    class Config:
        arbitrary_types_allowed = True

class GerarRelatorioPDF(BaseTool):
    name: str = "gerar_relatorio_pdf"
    description: str = "Gera um relatório em PDF com base no conteúdo analisado."
    args_schema: Type[BaseModel] = TextoRelatorio

    def _run(self, conteudo: str) -> str:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Use uma fonte Unicode TrueType compatível
            font_path = os.path.join("fonts", "DejaVuSans.ttf")
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.set_font("DejaVu", size=12)

            for linha in conteudo.split("\n"):
                pdf.multi_cell(0, 10, linha)

            caminho = "relatorio_vacinal.pdf"
            pdf.output(caminho)
            return caminho
        except Exception as e:
            return f"❌ Erro ao gerar PDF: {str(e)}"
