from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    # The ticket of the comment
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    # The author of the comment
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # The text of the comment
    body = models.TextField()
    # The date that the comment was created
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_date"]


class Ticket(models.Model):
    # The project of the ticket
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tickets")
    # The author of the ticket
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # The title of the Ticket
    title = models.CharField(max_length=200, unique=True)
    # The last date that the ticket was updated
    updated_date = models.DateTimeField(auto_now=True)
    # The date that the ticket was created
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_date"]

class TicketTemplate(models.Model):
    # The name of the template (Bug, Task, Issue)
    name = models.TextField()
    # The author of the ticket template
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

class File(models.Model):
    # The parent of the file
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="files")

    # The name of the File
    name = models.CharField(max_length=200, unique=True)
    # The file
    file = models.FileField()
    # The date that the file was created
    created_date = models.DateTimeField(auto_now_add=True)

class Attribute(models.Model):
    # The parent of the attribute
    ticket_template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE, related_name="attributes")

    # For simplicity value will be a text field to accept any alphanumeric value
    value = models.TextField()
    # The name of the attribute
    name = models.TextField()

class Project(models.Model):
    # The author of the project
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # The name of the project
    name = models.CharField(max_length=200, unique=True)
