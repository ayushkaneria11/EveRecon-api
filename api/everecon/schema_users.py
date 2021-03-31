import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from everecon.models import Profile
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import create_refresh_token, get_token

# Mutation: Create User
# We want to return:
# - The new `user` entry
# - The new associated `profile` entry - from our extended model
# - The access_token (so that we're automatically logged in)
# - The refresh_token (so that we can refresh my access token)

# Make models available to graphene.Field


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile


# CreateUser


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(UserProfile)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(
            user=user, profile=profile_obj, token=token, refresh_token=refresh_token
        )


# Finalize creating mutation for schema


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


# Query: Find users / my own profile
# Demonstrates auth block on seeing all user - only if I'm a manager
# Demonstrates auth block on seeing myself - only if I'm logged in


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_whoami(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception("Authentication Failure: Your must be signed in")
        return user

    # def resolve_users(self, info):
    #     user = info.context.user
    #     print(user)
    #     # Check to ensure user is a 'manager' to see all users
    #     if user.is_anonymous:
    #         raise Exception('Authentication Failure: Your must be signed in')
    #     if user.profile.role != 'manager':
    #         raise Exception('Authentication Failure: Must be Manager')
    #     return get_user_model().objects.all()