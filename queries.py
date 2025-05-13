import os

import django
from django.db.models import Q, F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()

from datetime import datetime, timedelta
from task_management.models import Task, SubTask

to_date = datetime.now().astimezone()
# task_id = Task.objects.create(title="Prepare a presentation for the report",
#                               description="Prepare materials and slides for the presentation",
#                               status="New",
#                               deadline=(to_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
#                               ).id
# SubTask.objects.bulk_create([SubTask(title="Collect information",
#                                      description="Find necessary information for the presentation",
#                                      status="Done",
#                                      deadline=(to_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
#                                      task_id=task_id),
#                              SubTask(title="Create 3 slides",
#                                      description="Create presentation slides",
#                                      status="In Progress",
#                                      deadline=(to_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
#                                      task_id=task_id)
#                              ])
task_id = Task.objects.create(title="Prepare presentation",
                              description="Prepare materials and slides for the presentation",
                              status="New",
                              deadline=(to_date + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
                              ).id
# print(task_id)
SubTask.objects.bulk_create([SubTask(title="Gather information",
                                     description="Find necessary information for the presentation",
                                     status="New",
                                     deadline=(to_date + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
                                     task_id=task_id),
                             SubTask(title="Create slides",
                                     description="Create presentation slides",
                                     status="New",
                                     deadline=(to_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                                     task_id=task_id)
                             ])

all_tasks_new = Task.objects.filter(status="New")
for task in all_tasks_new:
    print(f"{task.title=},{task.description=},{task.status=},{task.deadline=}")

print('-' * 30)

all_subtasks_done = SubTask.objects.filter(
    Q(status="Done") & Q(deadline__lt=to_date)
)
for subtask in all_subtasks_done:
    print(f"{subtask.title=},{subtask.description=},{subtask.status=},{subtask.deadline=}")

Task.objects.filter(title="Prepare presentation").update(status="In progress")

SubTask.objects.filter(title="Gather information").update(
    deadline=F('deadline') - timedelta(days=2)
)

subtask = SubTask.objects.get(title="Create slides")
subtask.description = "Create and format presentation slides"
subtask.save()


Task.objects.filter(title="Prepare presentation").delete()









