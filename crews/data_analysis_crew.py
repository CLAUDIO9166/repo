import os
import tempfile
from langchain_ollama import ChatOllama
from crewai import Agent, Task, Crew, Process
from tools.read_excel_tool import LerPlanilhaVacinacao
from tools.calculate_age_tool import CalcularIdadePacientes
from tools.pdf_generator_tool import GerarRelatorioPDF
from tools.vaccine_analyzer_tool import AnalisarVacinacao
from crewai_tools import FileReadTool

file_read_tool = FileReadTool()



class CrewDataAnalyzer:
    def __init__(self, file_info, user_request):
        self.file_info = file_info
        self.user_request = user_request
        self.model = ChatOllama(
            model="ollama/llama3",
            base_url="http://localhost:11434",
            provider="huggingface"
        )

    def kickoff(self):
        # 1. Leitor de Dados
        leitor = Agent(
        role='ACS Leitor de Dados',
        goal='Ler os dados {self.file_info} fornecidos e organizar as informações dos pacientes',
        tools=[LerPlanilhaVacinacao(),CalcularIdadePacientes(), file_read_tool],
        llm=self.model,
        backstory='Especialista em extração de dados de planilhas e organização de informações de saúde.'
    )


        tarefa_leitura = Task(
            description='Extraia nome, data de nascimento, vacinas aplicadas e datas do arquivo fornecido.',
            expected_output='Lista estruturada: Nome, Data de nascimento, Vacinas aplicadas com datas.',
            agent=leitor
        )

        # 2. Analista de Vacinação
        analista = Agent(
            role='ACS Analista PNI',
            goal='Comparar os dados com o Calendário Nacional de Vacinação 2025',
            tools=[AnalisarVacinacao()],
            llm=self.model,
            backstory='Profissional que conhece a fundo o calendário vacinal e identifica pendências.'
        )

        tarefa_analise = Task(
            description='Avalie os pacientes com vacinação em atraso com base nos dados extraídos.',
            expected_output='Lista com Nome, Idade, Vacinas faltantes, Datas recomendadas.',
            agent=analista
        )

        # 3. Gerador de Relatório
        gerador = Agent(
            role='ACS Gerador de Relatórios',
            goal='Gerar relatório estruturado com base nas análises',
            tools=[GerarRelatorioPDF()],
            llm=self.model,
            backstory='Especialista em criar relatórios claros e formais prontos para uso institucional.'
        )

        tarefa_relatorio = Task(
            description=f'Crie um relatório baseado na solicitação: "{self.user_request}"',
            expected_output='Texto ou relatório com informações solicitadas.',
            agent=gerador
        )

        # Equipe unificada
        equipe = Crew(
            agents=[leitor, analista, gerador],
            tasks=[tarefa_leitura, tarefa_analise, tarefa_relatorio],
            process=Process.sequential
        )

        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(self.file_info)
            caminho_arquivo = tmp.name
        
        resultados = equipe.kickoff(inputs={"arquivo": caminho_arquivo})
        return resultados