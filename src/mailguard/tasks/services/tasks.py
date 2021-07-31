from mailguard.tasks.models.task_model import TaskModel


def get_all():
    return TaskModel.objects.all()


def get_inactive_tasks():
    return TaskModel.objects.filter(active=0).all()


def remove_task():
    pass


def get_state_error_tasks():
    return TaskModel.objects.filter(state="ERROR").all()
