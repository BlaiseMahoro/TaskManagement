from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from colorfield.fields import ColorField
import random

#Refence:https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    avatar = models.ImageField(upload_to="avatars/users",help_text="Profile picture", blank=True )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to="avatars/projects",help_text="Project Avatar", blank=True )
    


ROLES_CHOICES = (
    ("is_admin", "Admin"),
    ("is_normal","Normal"),
)
class Role(models.Model):
    role = models.CharField(max_length=10,choices=ROLES_CHOICES, default="is_admin", help_text="User role")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    

class Comment(models.Model):
    # The ticket of the comment
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="comments")
    # The author of the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")

    # The title of the Ticket
    title = models.CharField(max_length=200, unique=True)
    # The last date that the ticket was updated
    updated_date = models.DateTimeField(auto_now=True)
    # The date that the ticket was created
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_date"]


class TicketTemplate(models.Model):
    # The project that this template will be applied to
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="ticket_template")

class State(models.Model):
    # The ticket template that contains these states
    ticket_template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE, related_name="states")

    # The name of the state
    state_name = models.TextField(max_length=50)

    # The color of the state
    color = ColorField(default="%06x" % random.randint(0, 0xFFFFFF))

class Type(models.Model):
    # The ticket template that contains these types
    ticket_template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE, related_name="types")   

    # The name of the type
    type_name = models.TextField(max_length=50)

    # The color of the type
    color = ColorField(default="%06x" % random.randint(0, 0xFFFFFF))

class Attribute(models.Model):
    # The parent of the attribute
    ticket_template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE, related_name="attributes")

    # For simplicity value will be a text field to accept any alphanumeric value
    value = models.TextField()
    # The name of the attribute
    name = models.TextField()

class File(models.Model):
    # The parent of the file
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="files")

    # The name of the File
    name = models.CharField(max_length=200, unique=True)
    # The file
    file = models.FileField()
    # The date that the file was created
    created_date = models.DateTimeField(auto_now_add=True)
