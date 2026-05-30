"""
TaskFlow CLI – Interface de linha de comando
Navegue pelo menu para gerenciar suas tarefas de forma ágil.
"""

from src.task_manager import TaskRepository, TaskService, Status, Priority


# ── helpers de exibição ──────────────────────────────────────────────────────

PRIORITY_ICON = {
    Priority.LOW.value:    "🟢",
    Priority.MEDIUM.value: "🟡",
    Priority.HIGH.value:   "🔴",
}

SEPARATOR = "─" * 60


def print_header():
    print("\n" + "═" * 60)
    print("      📋  TASKFLOW – Gerenciamento de Tarefas Ágil")
    print("             TechFlow Solutions  |  v1.0")
    print("═" * 60)


def print_task(task):
    icon = PRIORITY_ICON.get(task.priority.value, "⚪")
    print(f"  [{task.id:>3}] {icon} {task.title}")
    if task.description:
        print(f"        {task.description}")
    print(f"        Status: {task.status.value}  |  Prioridade: {task.priority.value}")
    print(f"        Criado em: {task.created_at[:10]}")


def print_kanban(board: dict):
    print("\n" + SEPARATOR)
    for column, tasks in board.items():
        count = len(tasks)
        print(f"\n  🗂  {column.upper()}  ({count})")
        print("  " + "·" * 40)
        if tasks:
            for t in tasks:
                print_task(t)
        else:
            print("  (vazio)")
    print("\n" + SEPARATOR)


def ask(prompt: str, default: str = "") -> str:
    value = input(prompt).strip()
    return value if value else default


def ask_priority() -> str:
    options = [p.value for p in Priority]
    print("  Prioridades: " + " | ".join(f"[{i+1}] {v}" for i, v in enumerate(options)))
    choice = ask("  Escolha [1-3] (padrão: 2): ", "2")
    try:
        return options[int(choice) - 1]
    except (ValueError, IndexError):
        return Priority.MEDIUM.value


def ask_status() -> str:
    options = [s.value for s in Status]
    print("  Status: " + " | ".join(f"[{i+1}] {v}" for i, v in enumerate(options)))
    choice = ask("  Escolha [1-3]: ")
    try:
        return options[int(choice) - 1]
    except (ValueError, IndexError):
        return None


# ── ações do menu ────────────────────────────────────────────────────────────

def menu_create(service: TaskService):
    print(f"\n{SEPARATOR}\n  ➕  Nova Tarefa\n{SEPARATOR}")
    title = ask("  Título: ")
    if not title:
        print("  ⚠️  Título obrigatório. Operação cancelada.")
        return
    desc     = ask("  Descrição (opcional): ")
    priority = ask_priority()
    try:
        task = service.create_task(title, desc, priority)
        print(f"\n  ✅  Tarefa #{task.id} criada com sucesso!")
    except ValueError as e:
        print(f"\n  ❌  Erro: {e}")


def menu_list(service: TaskService):
    tasks = service.repo.get_all()
    if not tasks:
        print("\n  ℹ️  Nenhuma tarefa cadastrada ainda.")
        return
    print(f"\n{SEPARATOR}\n  📄  Todas as Tarefas ({len(tasks)})\n{SEPARATOR}")
    for t in tasks:
        print_task(t)


def menu_kanban(service: TaskService):
    print_kanban(service.get_kanban_board())


def menu_move(service: TaskService):
    print(f"\n{SEPARATOR}\n  🔀  Mover Tarefa\n{SEPARATOR}")
    try:
        task_id = int(ask("  ID da tarefa: "))
    except ValueError:
        print("  ❌  ID inválido.")
        return
    new_status = ask_status()
    if new_status is None:
        print("  ❌  Status inválido. Operação cancelada.")
        return
    try:
        task = service.move_task(task_id, new_status)
        print(f"\n  ✅  Tarefa #{task.id} movida para '{task.status.value}'!")
    except LookupError as e:
        print(f"\n  ❌  {e}")


def menu_update(service: TaskService):
    print(f"\n{SEPARATOR}\n  ✏️  Editar Tarefa\n{SEPARATOR}")
    try:
        task_id = int(ask("  ID da tarefa: "))
    except ValueError:
        print("  ❌  ID inválido.")
        return

    task = service.repo.get_by_id(task_id)
    if task is None:
        print(f"  ❌  Tarefa #{task_id} não encontrada.")
        return

    print(f"  Tarefa atual: {task.title}")
    new_title = ask(f"  Novo título (Enter para manter): ", task.title)
    new_desc  = ask(f"  Nova descrição (Enter para manter): ", task.description)
    print("  Nova prioridade:")
    new_priority = ask_priority()

    service.repo.update(task_id, title=new_title,
                        description=new_desc, priority=new_priority)
    print(f"\n  ✅  Tarefa #{task_id} atualizada!")


def menu_delete(service: TaskService):
    print(f"\n{SEPARATOR}\n  🗑️  Excluir Tarefa\n{SEPARATOR}")
    try:
        task_id = int(ask("  ID da tarefa: "))
    except ValueError:
        print("  ❌  ID inválido.")
        return
    confirm = ask(f"  Tem certeza? (s/N): ").lower()
    if confirm != "s":
        print("  Operação cancelada.")
        return
    try:
        service.delete_task(task_id)
        print(f"\n  ✅  Tarefa #{task_id} excluída!")
    except LookupError as e:
        print(f"\n  ❌  {e}")


# ── loop principal ────────────────────────────────────────────────────────────

MENU_OPTIONS = {
    "1": ("Criar tarefa",       menu_create),
    "2": ("Listar todas",       menu_list),
    "3": ("Ver quadro Kanban",  menu_kanban),
    "4": ("Mover tarefa",       menu_move),
    "5": ("Editar tarefa",      menu_update),
    "6": ("Excluir tarefa",     menu_delete),
    "0": ("Sair",               None),
}


def main():
    repo    = TaskRepository(filepath="tasks.json")
    service = TaskService(repo)

    print_header()

    while True:
        print("\n  MENU PRINCIPAL")
        for key, (label, _) in MENU_OPTIONS.items():
            print(f"  [{key}] {label}")

        choice = ask("\n  Opção: ")

        if choice == "0":
            print("\n  👋  Até logo!\n")
            break

        action = MENU_OPTIONS.get(choice)
        if action:
            action[1](service)
        else:
            print("  ⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
