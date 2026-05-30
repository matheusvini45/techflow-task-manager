"""
Testes automatizados – TaskFlow
Execução: pytest tests/test_task_manager.py -v
"""

import pytest
import os
import sys

# garante que a pasta raiz está no path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.task_manager import (
    Task, TaskRepository, TaskService,
    Status, Priority,
)


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_repo(tmp_path):
    """Repositório usando arquivo temporário (isolado entre testes)."""
    filepath = str(tmp_path / "test_tasks.json")
    return TaskRepository(filepath=filepath)


@pytest.fixture
def service(tmp_repo):
    return TaskService(tmp_repo)


# ── testes de criação (CREATE) ────────────────────────────────────────────────

class TestCreateTask:

    def test_create_basic_task(self, service):
        task = service.create_task("Implementar login")
        assert task.id is not None
        assert task.title == "Implementar login"
        assert task.status == Status.TODO

    def test_create_task_with_all_fields(self, service):
        task = service.create_task("Deploy", "Subir para produção", "Alta")
        assert task.priority == Priority.HIGH
        assert task.description == "Subir para produção"

    def test_create_trims_whitespace(self, service):
        task = service.create_task("  Revisar código  ")
        assert task.title == "Revisar código"

    def test_create_empty_title_raises(self, service):
        with pytest.raises(ValueError, match="vazio"):
            service.create_task("")

    def test_create_whitespace_title_raises(self, service):
        with pytest.raises(ValueError):
            service.create_task("   ")

    def test_create_long_title_raises(self, service):
        with pytest.raises(ValueError, match="100"):
            service.create_task("A" * 101)

    def test_ids_are_sequential(self, service):
        t1 = service.create_task("Tarefa 1")
        t2 = service.create_task("Tarefa 2")
        assert t2.id == t1.id + 1


# ── testes de leitura (READ) ──────────────────────────────────────────────────

class TestReadTask:

    def test_get_all_empty(self, service):
        assert service.repo.get_all() == []

    def test_get_all_returns_created(self, service):
        service.create_task("A")
        service.create_task("B")
        assert len(service.repo.get_all()) == 2

    def test_get_by_id_found(self, service):
        task = service.create_task("Tarefa X")
        found = service.repo.get_by_id(task.id)
        assert found is not None
        assert found.title == "Tarefa X"

    def test_get_by_id_not_found(self, service):
        assert service.repo.get_by_id(999) is None

    def test_get_by_status(self, service):
        service.create_task("T1")
        service.create_task("T2")
        todos = service.repo.get_by_status(Status.TODO)
        assert len(todos) == 2


# ── testes de atualização (UPDATE) ───────────────────────────────────────────

class TestUpdateTask:

    def test_move_task_to_in_progress(self, service):
        task = service.create_task("Tarefa")
        updated = service.move_task(task.id, Status.IN_PROGRESS.value)
        assert updated.status == Status.IN_PROGRESS

    def test_move_task_to_done(self, service):
        task = service.create_task("Tarefa")
        service.move_task(task.id, Status.IN_PROGRESS.value)
        done = service.move_task(task.id, Status.DONE.value)
        assert done.status == Status.DONE

    def test_move_nonexistent_raises(self, service):
        with pytest.raises(LookupError):
            service.move_task(999, Status.DONE.value)

    def test_update_title_and_priority(self, service):
        task = service.create_task("Original")
        service.repo.update(task.id, title="Atualizado", priority="Alta")
        updated = service.repo.get_by_id(task.id)
        assert updated.title == "Atualizado"
        assert updated.priority == Priority.HIGH


# ── testes de exclusão (DELETE) ──────────────────────────────────────────────

class TestDeleteTask:

    def test_delete_existing(self, service):
        task = service.create_task("Para deletar")
        result = service.delete_task(task.id)
        assert result is True
        assert service.repo.get_by_id(task.id) is None

    def test_delete_nonexistent_raises(self, service):
        with pytest.raises(LookupError):
            service.delete_task(999)

    def test_delete_reduces_count(self, service):
        t1 = service.create_task("A")
        service.create_task("B")
        service.delete_task(t1.id)
        assert len(service.repo.get_all()) == 1


# ── testes do quadro Kanban ───────────────────────────────────────────────────

class TestKanbanBoard:

    def test_board_has_three_columns(self, service):
        board = service.get_kanban_board()
        assert Status.TODO.value in board
        assert Status.IN_PROGRESS.value in board
        assert Status.DONE.value in board

    def test_board_reflects_moves(self, service):
        task = service.create_task("Sprint task")
        service.move_task(task.id, Status.IN_PROGRESS.value)
        board = service.get_kanban_board()
        assert len(board[Status.IN_PROGRESS.value]) == 1
        assert len(board[Status.TODO.value]) == 0


# ── testes de persistência ────────────────────────────────────────────────────

class TestPersistence:

    def test_data_persists_across_instances(self, tmp_path):
        filepath = str(tmp_path / "persist.json")
        repo1 = TaskRepository(filepath)
        svc1  = TaskService(repo1)
        task  = svc1.create_task("Persistida")

        # nova instância lê o mesmo arquivo
        repo2 = TaskRepository(filepath)
        found = repo2.get_by_id(task.id)
        assert found is not None
        assert found.title == "Persistida"
