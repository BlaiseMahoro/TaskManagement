from django.contrib import admin
from .models import Profile, Project, Role, Comment, Ticket, TicketTemplate, File, Attribute, Type, State, AttributeType, Relationship, RelationshipType, File
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

class AttributeInlineAdmin(admin.TabularInline):
    model = Attribute
    extra = 0
class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 0
class RelationshipInlineAdmin(admin.TabularInline):
    model = Relationship
    extra = 0
    fk_name = "ticket_1"
class FileInlineAdmin(admin.TabularInline):
    model = File
    extra = 0
class TicketAdmin(admin.ModelAdmin):
    inlines = [AttributeInlineAdmin,CommentInlineAdmin,RelationshipInlineAdmin,FileInlineAdmin]

class StateInlineAdmin(admin.TabularInline):
    model = State
    extra = 0
class TypeInlineAdmin(admin.TabularInline):
    model = Type
    extra = 0
class AttributeTypeInlineAdmin(admin.TabularInline):
    model = AttributeType
    extra = 0
class RelationshipTypeInlineAdmin(admin.TabularInline):
    model = RelationshipType
    extra = 0

class TicketTemplateAdmin(admin.ModelAdmin):
    inlines = [StateInlineAdmin, TypeInlineAdmin, AttributeTypeInlineAdmin, RelationshipTypeInlineAdmin]
    list_display=('project',)

class RelationshipAdmin(admin.ModelAdmin):
    list_display=('__str__','ticket_1','ticket_2')

class RoleInlineAdmin(admin.TabularInline):
    model = Role
    extra = 0
class ProjectAdmin(admin.ModelAdmin):
    inlines = [RoleInlineAdmin]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile)
#admin.site.register(Role)
admin.site.register(TicketTemplate, TicketTemplateAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(File)
#admin.site.register(Comment)
#admin.site.register(Attribute)
#admin.site.register(State)
#admin.site.register(Type)
#admin.site.register(AttributeType)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(RelationshipType)
