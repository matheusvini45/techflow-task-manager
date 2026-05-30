"""
TaskFlow - Sistema de Gerenciamento de Tarefas
TechFlow Solutions | Engenharia de Software
"""

import json
import os
from datetime import datetime
from enum import Enum


# ──────────────────────────────────────────────
# Enums de status e prioridade (inspirados no Kanban)
# ──────────────────────────────────────────────

class Status(str, Enum):
    TODO        = "A Fazer"
    IN_PROGRESS = "Em Progresso"
    DONE        = "Concluído"


class Priority(str, Enum):
    LOW    = "Baixa"
    MEDIUM = "Média"
    HIGH   = "Alta"


# ──────────────────────────────────────────────
# Modelo de Tarefa
# ──────────────────────────────────────────────

class Task:
    """Representa uma tarefa no sistema."""

    def __init__(self, title: str, description: str = "",
                 priority: Priority = Priority.MEDIUM):
        self.id          = None                        # definido pelo repositório
        self.title       = title
        self.description = description
        self.priority    = priority
        self.status      = Status.TODO
        self.created_at  = datetime.now().isoformat()
        self.updated_at  = self.created_at

    # Serialização ↔ JSON
    def to_dict(self) -> dict:
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "priority":    self.priority.value,
            "status":      self.status.value,
            "created_at":  self.created_at,
            "updated_at":  self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        task             = Task(data["title"], data["description"],
                                Priority(data["priority"]))
        task.id          = data["id"]
        task.status      = Status(data["status"])
        task.created_at  = data["created_at"]
        task.updated_at  = data["updated_at"]
        return task

    def __repr__(self):
        return (f"Task(id={self.id}, title='{self.title}', "
                f"status='{self.status.value}', priority='{self.priority.value}')")


# ──────────────────────────────────────────────
# Repositório (persistência em JSON)
# ──────────────────────────────────────────────

class TaskRepository:
    """Gerencia leitura e escrita de tarefas em arquivo JSON."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        self._load()

    # ── persistência ──

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for item in raw:
                task = Task.from_dict(item)
                self._tasks[task.id] = task
                if task.id >= self._next_id:
                    self._next_id = task.id + 1

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._tasks.values()],
                      f, ensure_ascii=False, indent=2)

    # ── CRUD ──

    def create(self, task: Task) -> Task:
        """CREATE – adiciona nova tarefa."""
        task.id = self._next_id
        self._next_id += 1
        self._tasks[task.id] = task
        self._save()
        return task

    def get_all(self) -> list[Task]:
        """READ – retorna todas as tarefas."""
        return list(self._tasks.values())

    def get_by_id(self, task_id: int) -> Task | None:
        """READ – retorna tarefa pelo ID."""
        return self._tasks.get(task_id)

    def get_by_status(self, status: Status) -> list[Task]:
        """READ – filtra por coluna do Kanban."""
        return [t for t in self._tasks.values() if t.status == status]

    def update(self, task_id: int, **kwargs) -> Task | None:
        """UPDATE – atualiza campos de uma tarefa."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        allowed = {"title", "description", "priority", "status"}
        for key, value in kwargs.items():
            if key in allowed:
                # converte string → enum quando necessário
                if key == "status" and isinstance(value, str):
                    value = Status(value)
                if key == "priority" and isinstance(value, str):
                    value = Priority(value)
                setattr(task, key, value)

        task.updated_at = datetime.now().isoformat()
        self._save()
        return task

    def delete(self, task_id: int) -> bool:
        """DELETE – remove tarefa pelo ID."""
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        self._save()
        return True


# ──────────────────────────────────────────────
# Serviço (regras de negócio)
# ──────────────────────────────────────────────

class TaskService:
    """Camada de serviço com validações e regras de negócio."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, title: str, description: str = "",
                    priority: str = "Média") -> Task:
        if not title or not title.strip():
            raise ValueError("O título da tarefa não pode ser vazio.")
        if len(title) > 100:
            raise ValueError("O título não pode ter mais de 100 caracteres.")

        task = Task(title.strip(), description.strip(), Priority(priority))
        return self.repo.create(task)

    def move_task(self, task_id: int, new_status: str) -> Task:
        """Move tarefa entre colunas do Kanban."""
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise LookupError(f"Tarefa #{task_id} não encontrada.")
        return self.repo.update(task_id, status=new_status)

    def get_kanban_board(self) -> dict[str, list[Task]]:
        """Retorna tarefas agrupadas por coluna (quadro Kanban)."""
        return {
            Status.TODO.value:        self.repo.get_by_status(Status.TODO),
            Status.IN_PROGRESS.value: self.repo.get_by_status(Status.IN_PROGRESS),
            Status.DONE.value:        self.repo.get_by_status(Status.DONE),
        }

    def delete_task(self, task_id: int) -> bool:
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise LookupError(f"Tarefa #{task_id} não encontrada.")
        return self.repo.delete(task_id)
