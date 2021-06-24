from .models.task_model import TaskModel


def get_all():
    return TaskModel.objects.all()
