from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Refence:https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/",help_text="Profile picture", blank=True )

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


ROLES_CHOICES = (
    ("is_admin", "Admin"),
    ("is_normal","Normal"),
)
class Role(models.Model):
    role = models.CharField(max_length=10,choices=ROLES_CHOICES, default="is_admin", help_text="User role")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    


class TicketTemplate(models.Model):
    pass

class Attribute(models.Model):
    pass