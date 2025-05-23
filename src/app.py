"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   # Esportivas
   "Futebol": {
      "description": "Participe do time de futebol da escola e jogue campeonatos",
      "schedule": "Terças e quintas, 16h - 17h30",
      "max_participants": 22,
      "participants": ["lucas@mergington.edu", "marcos@mergington.edu"]
   },
   "Vôlei": {
      "description": "Aulas e treinos de vôlei para todos os níveis",
      "schedule": "Quartas e sextas, 15h - 16h30",
      "max_participants": 18,
      "participants": ["ana@mergington.edu", "carla@mergington.edu"]
   },
   # Artísticas
   "Teatro": {
      "description": "Oficina de teatro e expressão corporal",
      "schedule": "Segundas, 16h - 17h30",
      "max_participants": 15,
      "participants": ["paulo@mergington.edu", "juliana@mergington.edu"]
   },
   "Clube de Artes": {
      "description": "Desenho, pintura e outras atividades artísticas",
      "schedule": "Sábados, 10h - 12h",
      "max_participants": 20,
      "participants": ["lara@mergington.edu", "bruno@mergington.edu"]
   },
   # Intelectuais
   "Olimpíada de Matemática": {
      "description": "Prepare-se para olimpíadas de matemática com aulas e desafios",
      "schedule": "Quartas, 17h - 18h",
      "max_participants": 25,
      "participants": ["rafael@mergington.edu", "aline@mergington.edu"]
   },
   "Clube de Leitura": {
      "description": "Leitura e discussão de livros clássicos e contemporâneos",
      "schedule": "Sextas, 14h - 15h",
      "max_participants": 16,
      "participants": ["camila@mergington.edu", "pedro@mergington.edu"]
   }
}


@app.get("/")
def root():
    """Redireciona para a interface web."""
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Retorna todas as atividades e seus detalhes."""
    return activities


@app.post("/activities/{activity_name}/remove")
def remove_participant(activity_name: str, email: str):
    """Remove um participante de uma atividade."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participante não encontrado nesta atividade")
    activity["participants"].remove(email)
    return {"message": f"{email} removido da atividade {activity_name}"}


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Inscreve um participante em uma atividade."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Já inscrito nesta atividade")
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Limite de participantes atingido")
    activity["participants"].append(email)
    return {"message": "Inscrição realizada com sucesso"}
