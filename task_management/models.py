from django.db import models


status_choices = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done")
    ]


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        unique_together = ("name",)

    def __str__(self):
        return self.name



class Task(models.Model):
    title = models.CharField(max_length=50, unique_for_date="deadline")
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=100, choices=status_choices, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        ordering = ("-created_at",)
        unique_together = ("title",)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_choices)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_subtask"
        ordering= ("-created_at",)
        verbose_name = "SubTask"
        unique_together = ("title",)

    def __str__(self):
        return self.title
