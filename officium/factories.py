import factory
from faker import Factory
from .models import Officium, OfficiumSite, OfficiumUser
from django.contrib.auth import get_user_model

fake = Factory.create()

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)
    username = factory.LazyAttribute(lambda a: fake.user_name())

class OfficiumFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Officium
    name = factory.LazyAttribute(lambda a: fake.sentence())


class OfficiumSiteFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = OfficiumSite
    url = factory.LazyAttribute(lambda a: fake.url())
    officium = factory.SubFactory(OfficiumFactory)


class OfficiumUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = OfficiumUser

    officium = factory.SubFactory(OfficiumFactory)
    user = factory.SubFactory(UserFactory)
