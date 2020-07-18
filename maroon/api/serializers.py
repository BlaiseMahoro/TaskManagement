from rest_framework import serializers
from task_management import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['avatar']

class TicketTemplateSerializer(serializers.ModelSerializer):
    types = serializers.SlugRelatedField(many=True,read_only=True,slug_field='type_name')
    states = serializers.SlugRelatedField(many=True,read_only=True,slug_field='state_name')
    #attributes = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')

    class Meta:
        model = models.TicketTemplate
        fields = ['types', 'states'] #, 'attributes'

class ProjectSerializer(serializers.ModelSerializer):
    ticket_template = TicketTemplateSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = ('name', 'description', 'ticket_template', 'roles')

    # def create_role(self, instance, user, role_title):
    #     role = Role(role_title, instance, user)
    #     role.save()