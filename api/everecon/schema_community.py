import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.forms import ModelForm
from .models import Community, Event, Category, Tag
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import *
from .schema_users import UserType
from django.contrib.auth.models import User

# Object types
class CommunityType(DjangoObjectType):
    class Meta:
        model = Community


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


# Queries

# Mutations
# Using serializer
# class CreateCommunity(SerializerMutation):
#     class Meta:
#         serializer_class = CommunitySerializer
#         model_operations = ['create', 'update']
#         lookup_field = 'id'

# Using ModelForm
# class CommunityForm(ModelForm):
#     class Meta:
#         model = Community
#         fields = '__all__'


# class CreateCommunity(DjangoFormMutation):
#     community = graphene.Field(CommunityType)

#     class Meta:
#         form_class = CommunityForm


class CreateCommunity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        featured_video = graphene.String()
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        email = graphene.String()
        website = graphene.String()
        facebook = graphene.String()
        linkedin = graphene.String()
        twitter = graphene.String()
        instagram = graphene.String()
        discord = graphene.String()
        # leader = graphene.ID(required=True)

    community = graphene.Field(CommunityType)
    leader = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        # leader = User.objects.get(id=kwargs.pop('leader'))
        leader = info.context.user
        community = Community(**kwargs, leader=leader)
        community.save()
        return cls(community=community, leader=leader)


class UpdateCommunity(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        featured_video = graphene.String()
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        email = graphene.String()
        website = graphene.String()
        facebook = graphene.String()
        linkedin = graphene.String()
        instagram = graphene.String()
        discord = graphene.String()
        is_active = graphene.Boolean()
        followers = graphene.List(graphene.ID)

    community = graphene.Field(CommunityType)
    # followers = graphene.Field(UserType) # TODO: Check if this is required

    @classmethod
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop("id")
        followers = None
        try:
            followers = kwargs.pop("followers")
        except Exception:
            pass
        # print(followers)
        # community = Community.objects.get(id=id)
        # for k, v in kwargs.items():
        #     print(k, v)
        #     community.k = v
        #     print(community.k)
        # community.save(force_update=True)
        # community = Community.objects.filter(id=id).update(**kwargs)
        community, created = Community.objects.update_or_create(defaults=kwargs, id=id)
        print(community.name)
        if followers:
            community.followers.add(*followers)
        # print(community.followers.all())
        return cls(community=community)


class DeleteCommunity(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Community.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class AddCoreMember(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.core_members.add(kwargs.get("user"))
        return cls(ok=True)


class RemoveCoreMember(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.core_members.remove(kwargs.get("user"))
        return cls(ok=True)


class AddVolunteer(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.volunteers.add(kwargs.get("user"))
        return cls(ok=True)


class RemoveVolunteer(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.volunteers.remove(kwargs.get("user"))
        return cls(ok=True)


class AddFollower(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.followers.add(kwargs.get("user"))
        return cls(ok=True)


class RemoveFollower(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.followers.remove(kwargs.get("user"))
        return cls(ok=True)


# Query Class
class Query(graphene.ObjectType):
    community_by_id = graphene.Field(CommunityType, id=graphene.ID())

    def resolve_community_by_id(root, info, id):
        return Community.objects.get(pk=id)


# Mutation Class
class Mutation(graphene.ObjectType):
    create_community = CreateCommunity.Field()
    update_community = UpdateCommunity.Field()
    # create_update_community = CreateCommunity.Field()
    delete_community = DeleteCommunity.Field()

    add_core_member = AddCoreMember.Field()
    remove_core_member = RemoveCoreMember.Field()
    add_volunteer = AddVolunteer.Field()
    remove_volunteer = RemoveVolunteer.Field()
