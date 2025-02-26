from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from datetime import datetime
import os
from fastapi.middleware.cors import CORSMiddleware

# Configurações de ambiente
os.environ["SERPER_API_KEY"] = "858d840548fd3a36161d5f345706e9d77e672e9f"
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("API Key da OpenAI não encontrada! Verifique suas variáveis de ambiente.")

# Configurando o app FastAPI
app = FastAPI()

# 🔹 ADICIONE ESTA CONFIGURAÇÃO PARA PERMITIR CHAMADAS DO GITHUB PAGES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para maior segurança, pode substituir por ["https://seu-usuario.github.io"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Modelo de entrada
class CompanyInput(BaseModel):
    company_name: str

# Ferramentas e agentes
search_tool = SerperDevTool()

company_enricher = Agent(
    role="Enriquecedor de Dados da Empresa",
    goal="Buscar informações estratégicas sobre a empresa do lead.",
    backstory=(
        "Você é um pesquisador corporativo especializado em identificar informações estratégicas sobre empresas para ajudar na tomada de decisões, levando em consideração as informações fornecidas pelo próprio lead"
    ),
    tools=[search_tool]
)

report_generator = Agent(
    role="Gerador de Relatórios",
    goal="Gerar relatórios estruturados e atrativos.",
    backstory=(
        "Você é um especialista em criar relatórios empresariais."
        "Sua principal missão é transformar essas informações em insights estratégicos que ajudem "
        "a {company_name} a crescer e superar desafios. Como parte da equipe da Goshen Land, você entende que o objetivo "
        "final é expandir os negócios das empresas atendidas, fornecendo soluções práticas e inspiradoras."
    ),
    collaboration=True,
)

report_reviewer = Agent(
    role="Revisor de Relatórios",
    goal="Garantir que o relatório gerado seja claro, relevante e estratégico para ajudar o vendedor em uma primeira reunião com o dono da {company_name}.",
    backstory=(
        "Sua função é revisar o relatório gerado e garantir que ele apresente todas as informações estratégicas necessárias para que o vendedor "
        "possa ter o máximo de informações sobre a {company_name}."
    ),
    collaboration=True,
)

# Tarefas
company_task = Task(
    description=(
        "Pesquise informações sobre a empresa '{company_name}', incluindo setor, faturamento estimado, presença digital e notícias relevantes."
    ),
    expected_output="Resumo detalhado da empresa.",
    agent=company_enricher,
)

report_task = Task(
    description=(
        "Com base nas informações fornecidas pelos outros agentes e as informações do input inicial, "
        "crie um relatório completo da {company_name} para a reunião de venda que inclua análises completas. "
        "Inclua a data e hora atuais: {current_datetime}."
    ),
    expected_output="Relatório estratégico e visualmente atrativo, listando todos os dados pesquisados.",
    agent=report_generator,
    async_execution=False,
)

review_task = Task(
    description=(
        "Avalie o relatório gerado pelo Gerador de Relatórios. Verifique se ele está de acordo com as informações necessárias "
        "para que o vendedor possa realizar uma ótima primeira reunião."
        "Se necessário, solicite uma revisão detalhada."
    ),
    expected_output="Apresentação do relatório aprovado.",
    agent=report_reviewer,
)

# Rota de teste para a raiz
@app.get("/")
def root():
    return {"message": "API está funcionando! Use o endpoint /run-crew para executar a Crew."}

# Endpoint para executar a Crew
@app.post("/run-crew")
def run_crew(input_data: CompanyInput):
    # Captura a data e hora atuais
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Crie a Crew
    crew = Crew(
        agents=[company_enricher, report_generator, report_reviewer],
        tasks=[company_task, report_task, review_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute a Crew
    try:
        result = crew.kickoff(inputs={
            "company_name": input_data.company_name,
            "current_datetime": now  # Adiciona a data e hora como entrada
        })
        return {
            "status": "success",
            "data": result,
            "timestamp": now  # Adiciona a data e hora no retorno da API
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar localmente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
