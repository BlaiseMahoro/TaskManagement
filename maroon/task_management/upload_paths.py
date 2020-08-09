import os

#https://stackoverflow.com/questions/5135556/dynamic-file-path-in-django
def get_file_upload_path(instance, filename):
    return os.path.join(
        "project_files",
        "project_%d" % instance.ticket.project.pk, 
        "ticket_%d" % instance.ticket.id_in_project, 
        filename
    )

def get_avatar_upload_path(instance, filename):
    return os.path.join(
        "avatars",
        "users",
        "user_%d" % instance.user.pk,
        filename
    )

def get_project_avatar_upload_path(instance, filename):
    return os.path.join(
        "avatars",
        "projects",
        "project_%d" % instance.pk,
        filename
    )