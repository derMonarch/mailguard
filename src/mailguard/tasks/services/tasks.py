from mailguard.tasks.models.task_model import TaskModel


def get_all():
    return TaskModel.objects.all()


def get_all_active_tasks():
    return TaskModel.objects.filter(active=1).all()


def get_inactive_tasks():
    return TaskModel.objects.filter(active=0).all()


def get_tasks_by_active_flag(active=0):
    return TaskModel.objects.filter(active=active).all()


def remove_task():
    pass


def get_state_error_tasks():
    return TaskModel.objects.filter(state="ERROR").all()


def get_tasks_by_state(state):
    return TaskModel.objects.filter(state=state).all()
