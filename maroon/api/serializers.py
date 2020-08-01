from rest_framework import serializers
from task_management import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['username','first_name','last_name','email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = models.Profile
        fields = ['user']

class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            #print(self.ticket_template)
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data}, ticket_template=self.ticket_template)
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')

class TicketTemplateSerializer(serializers.ModelSerializer):
    types = CustomSlugRelatedField(many=True,queryset=models.Type.objects.all(),slug_field='type_name')#TypeSerializer(many=True)
    states = CustomSlugRelatedField(many=True,queryset=models.State.objects.all(),slug_field='state_name')
    attributeTypes = CustomSlugRelatedField(many=True,queryset=models.AttributeType.objects.all(),slug_field='name')

    def get_fields(self, *args, **kwargs):
        #Save instance to pass as primary key for creating new items
        fields = super(TicketTemplateSerializer, self).get_fields(*args, **kwargs)
        fields['types'].child_relation.ticket_template = self.instance
        fields['states'].child_relation.ticket_template = self.instance
        fields['attributeTypes'].child_relation.ticket_template = self.instance    
        return fields

    class Meta:
        model = models.TicketTemplate
        fields = ['types','states','attributeTypes']

    def to_internal_value(self, data):
        #Delete Types and States before the new ones are added to the database
        models.Type.objects.filter(ticket_template=self.instance).delete()
        models.State.objects.filter(ticket_template=self.instance).delete()
        return super(TicketTemplateSerializer, self).to_internal_value(data=data)

    def update(self, instance, validated_data):
        self.delete_removed_attributes(instance, validated_data.get('attributeTypes'))
        return instance

    def delete_removed_attributes(self, instance, validated_data):
        names = [new_attribute.name for new_attribute in validated_data]
        for attribute in models.AttributeType.objects.filter(ticket_template=instance):
            if attribute.name not in names:
                attribute.delete()

class RoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile.user.username')

    def update(self, instance, validated_data):
        #Validated data embeds username weirdly
        valid_username = validated_data['profile']['user']['username']
        profile = models.Profile.objects.get(user=models.User.objects.get(username=valid_username))

        #'instance' in this case is the project to find the role
        role, created = models.Role.objects.all().get_or_create(profile=profile, project=instance)
        role.role = validated_data['role']
        role.save()

        return role

    class Meta:
        model = models.Role
        fields = ['role', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    ticket_template = TicketTemplateSerializer(read_only=True)
    roles = RoleSerializer(many=True)

    class Meta:
        model = models.Project
        fields = ('id','name', 'description', 'ticket_template', 'roles')

    def create(self, validated_data):
        """
        Create and return a new `Project` instance, given the validated data.
        """
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance

    def delete_removed_roles(self, instance, validated_data):
        roles = [new_role['username'] for new_role in validated_data]
        for role in models.Role.objects.filter(project=instance):
            if role.profile.user.username not in roles:
                role.delete()

class AttributeSerialier(serializers.ModelSerializer):
    attribute_type = serializers.CharField(source='attribute_type.name')

    class Meta:
        model = models.Attribute
        fields = ('attribute_type','value')


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ('state_name','color')
        extra_kwargs = {'color': {'required' : False}}
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = ('type_name','color')
        extra_kwargs = {'color': {'required' : False}}

class TicketSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source='project.name', required=False)
    project_pk = serializers.IntegerField(source='project.pk', required=False)
    state = serializers.CharField(source='state.state_name', required=False)
    type = serializers.CharField(source='type.type_name')
    assignees = ProfileSerializer(many=True, required=False)
    attributes = AttributeSerialier(many=True, required=False)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description','project', 'project_pk','id_in_project', 'state', 'type', 'attributes','assignees']
        extra_kwargs = {'id_in_project': {'required' : False}}

    def create(self, validated_data):
        """
        Create and return a new `Ticket` instance, given the validated data.
        """
        #print(validated_data)
        project = models.Project.objects.get(pk=validated_data.pop('project')['pk'])
        
        #Check that state is in the ticket template
        state = validated_data.pop('state')
        if state not in project.ticket_template.states.all().values('state_name'):
            raise serializers.ValidationError("The state is not valid")

        #Check that type is in the ticket template
        type = validated_data.pop('type')
        if type not in project.ticket_template.types.all().values('type_name'):
            raise serializers.ValidationError("The type is not valid")

        #check that all attributes are in the ticket template
        attributes = validated_data.pop('attributes')
        attribute_types = [ attribute['attribute_type'] for attribute in attributes]
        project_attribute_types = project.ticket_template.attributeTypes.all().values('name')
        for attribute_type in attribute_types:
            if attribute_type not in project_attribute_types:
                raise serializers.ValidationError("An attribute type is not valid.")
            #attribute = ticket.attributes.get(name=)

        #Check that all assignees are part of the project
        # assignees = validated_data.pop('assignees')
        # current_users = 
        # for user in assignees:
        #     if user not in project.
        # if assignees
        #project_pk = validated_data.pop('project')['name']

        ticket = models.Ticket(
            title=validated_data['title'], 
            description=validated_data['description'],
            state=project.ticket_template.states.all().get(state_name=state['state_name']),
            type=project.ticket_template.types.all().get(type_name=type['type_name']),
            project=project, 
            attributes=AttributeSerialier(attributes))
        ticket.attributes.set(AttributeSerialier(attributes))
        
        #ticket.save()
        return ticket
    