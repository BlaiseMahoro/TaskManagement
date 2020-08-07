from rest_framework import serializers
from task_management import models

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = ['username']

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
    relationshipTypes = CustomSlugRelatedField(many=True,queryset=models.RelationshipType.objects.all(),slug_field='name')

    def get_fields(self, *args, **kwargs):
        #Save instance to pass as primary key for creating new items
        fields = super(TicketTemplateSerializer, self).get_fields(*args, **kwargs)
        fields['types'].child_relation.ticket_template = self.instance
        fields['states'].child_relation.ticket_template = self.instance
        fields['attributeTypes'].child_relation.ticket_template = self.instance
        fields['relationshipTypes'].child_relation.ticket_template = self.instance     
        return fields

    class Meta:
        model = models.TicketTemplate
        fields = ['types','states','attributeTypes','relationshipTypes']

    def to_internal_value(self, data):
        #Delete Types and States before the new ones are added to the database
        models.Type.objects.filter(ticket_template=self.instance).delete()
        models.State.objects.filter(ticket_template=self.instance).delete()
        return super(TicketTemplateSerializer, self).to_internal_value(data=data)

    def update(self, instance, validated_data):
        self.delete_removed_attributes(instance, validated_data.get('attributeTypes'))
        self.delete_removed_relationships(instance, validated_data.get('relationshipTypes'))
        return instance

    def delete_removed_attributes(self, instance, validated_data):
        names = [new_attribute.name for new_attribute in validated_data]
        for attribute in models.AttributeType.objects.filter(ticket_template=instance):
            if attribute.name not in names:
                attribute.delete()

    def delete_removed_relationships(self, instance, validated_data):
        names = [new_relationship.name for new_relationship in validated_data]
        for relationship in models.RelationshipType.objects.filter(ticket_template=instance):
            if relationship.name not in names:
                relationship.delete()

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
    project_pk = serializers.IntegerField(source='project.pk', required=False, write_only=True)
    state = serializers.CharField(source='state.state_name', default="None")
    type = serializers.CharField(source='type.type_name', default="None")
    assignee_list = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    assignees = ProfileSerializer(many=True, read_only=True)
    attributes = AttributeSerialier(many=True, required=False)

    class Meta:
        model = models.Ticket
        fields = ['title','description','project', 'project_pk','id_in_project', 'state', 'type', 'attributes','assignee_list','assignees']
        extra_kwargs = {'id_in_project': {'required' : False}}

    def create(self, validated_data):
        """
        Create and return a new `Ticket` instance, given the validated data.
        """
        project = models.Project.objects.get(pk=validated_data.pop('project')['pk'])

        #Create ticket for project
        ticket = models.Ticket(project=project)
        self.update(instance=ticket, validated_data=validated_data)

        return ticket

    def update(self, instance, validated_data):
        #Check that state is in the ticket template
        ticket_template = instance.project.ticket_template
        state = validated_data.pop('state')
        if state not in ticket_template.states.all().values('state_name'):
            raise serializers.ValidationError("The state is not valid")
        instance.state = ticket_template.states.all().get(state_name=state['state_name'])

        #Check that type is in the ticket template
        type = validated_data.pop('type')
        if type not in ticket_template.types.all().values('type_name'):
            raise serializers.ValidationError("The type is not valid")
        instance.type = ticket_template.types.all().get(type_name=type['type_name'])

        #Create ticket on required values
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.save()

        #Update attributes and assignees
        if 'attributes' in validated_data:
            self.update_attributes(validated_data.pop('attributes'), instance)
        if 'assignee_list' in validated_data:
            self.update_assignees(validated_data.pop('assignee_list'), instance)

        return instance


    def update_attributes(self, validated_data, ticket):
        #Get the attribute type names to check requested names against
        project_attributes = ticket.project.ticket_template.attributeTypes.all().values('name')

        #For each attribute in the request
        for attribute in validated_data:
            #Raise an error if the attribute type is not in the ticket template
            if attribute['attribute_type'] not in project_attributes:
                raise serializers.ValidationError("A listed attribute type is not valid.")
                
            #Update or create the attribute on the ticket
            name = attribute['attribute_type']['name']
            db_project_attribute = models.AttributeType.objects.get(ticket_template=ticket.project.ticket_template,name=name)
            db_attribute, created = models.Attribute.objects.all().get_or_create(ticket=ticket, attribute_type=db_project_attribute)
            db_attribute.value = attribute['value']
            db_attribute.save()

    def update_assignees(self, validated_data, ticket):
        #Get the project users to check request users against
        project_usernames = [ role.profile.user.username for role in ticket.project.roles.all()]

        #For each username in the request
        for username in validated_data:
            #Raise error if the user does not have a role in the project
            if username not in project_usernames:
                raise serializers.ValidationError("A listed user is not a collaborator on this project.")
    
            #Add user to ticket if they are not already there
            db_profile = models.Profile.objects.get(user=models.User.objects.get(username = username))
            if db_profile not in ticket.assignees.all():
                ticket.assignees.add(db_profile)

        for profile in ticket.assignees.all():
            if profile.user.username not in validated_data:
                ticket.assignees.remove(profile)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False, read_only=True)
    created_date = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = models.Comment
        fields = ('pk','author','created_date','body')

class LinkSerializer(serializers.ModelSerializer):
    relationship_type = serializers.CharField(source='relationship_type.name')
    ticket_2 = serializers.CharField(source='ticket_2.title', required=False, read_only=True)

    class Meta:
        model = models.Comment
        fields = ('pk','relationship_type','ticket_2')

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.File
        fields = ('pk','name','created_date')



        

    