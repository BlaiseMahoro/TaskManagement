from rest_framework import serializers
from task_management import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['user.username']

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
        #print("template internal value")
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

class FlatUserName(serializers.CharField):
    def to_representation(self, value):
        return value.user.username

class RoleSerializer(serializers.ModelSerializer):
    username = FlatUserName(source="profile")

    def update(self, instance, validated_data):
        print(validated_data)
        profile = models.Profile.objects.get(user=models.User.objects.get(username=validated_data['profile']))

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
        Create and return a new `Snippet` instance, given the validated data.
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