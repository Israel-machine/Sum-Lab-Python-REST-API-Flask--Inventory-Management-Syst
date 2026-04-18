import json
import os
from models.user_class import User
from models.project_class import Project
from models.task_class import Task

DB_PATH = "data/db.json"

def save_data():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        data = {
            "users": [
                {"id": u.id, "name": u.name, "email": u.email} 
                for u in User.all
            ],
            "projects": [
                {
                    "id": p.id, 
                    "title": p.title, 
                    "description": p.description, 
                    "due_date": p.due_date, 
                    "user_id": p.user.id
                } for p in Project.all
            ],
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "project_id": t.project.id
                } for t in Task.all
            ]
        }
        
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    if not os.path.exists(DB_PATH):
        return

    try:
        with open(DB_PATH, "r") as f:
            data = json.load(f)

        User.all = []
        for u_d in data.get("users", []):
            u = User(name=u_d['name'], email=u_d['email'])
            u.id = u_d['id']
            User.id_counter = max(User.id_counter, u.id + 1)

        Project.all = []
        for p_d in data.get("projects", []):
            owner = next((u for u in User.all if u.id == p_d['user_id']), None)
            if owner:
                p = Project(
                    title=p_d['title'], 
                    description=p_d['description'], 
                    due_date=p_d['due_date'], 
                    user=owner
                )
                p.id = p_d['id']
                Project.id_counter = max(Project.id_counter, p.id + 1)

        Task.all = []
        for t_d in data.get("tasks", []):
            proj = next((p for p in Project.all if p.id == t_d['project_id']), None)
            if proj:
                t = Task(title=t_d['title'], project=proj, status=t_d['status'])
                t.id = t_d['id']
                Task.id_counter = max(Task.id_counter, t.id + 1)

    except Exception as e:
        print(f"Error loading data: {e}")