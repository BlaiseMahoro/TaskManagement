from rest_framework import serializers
from task_management import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['name']

class TicketTemplateSerializer(serializers.ModelSerializer):
    types = serializers.SlugRelatedField(many=True,read_only=True,slug_field='type_name')
    states = serializers.SlugRelatedField(many=True,read_only=True,slug_field='state_name')
    #attributes = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')

    class Meta:
        model = models.TicketTemplate
        fields = ['types', 'states'] #, 'attributes'

class RoleSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = models.Role
        fields = ['role', 'profile']

class ProjectSerializer(serializers.ModelSerializer):
    ticket_template = TicketTemplateSerializer(read_only=True)
    # roles = serializers.
    #roles = serializer_related_field.RoleSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = ('id','name', 'description', 'ticket_template', 'roles')