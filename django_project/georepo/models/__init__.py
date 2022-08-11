from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from ..models.entity import *  # noqa
from ..models.language import *  # noqa
from ..models.dataset import *  # noqa
from ..models.code import *  # noqa
from ..models.style import *  # noqa
from ..models.dataset_tile_config import *  # noqa


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created or not Token.objects.filter(user=instance).exists():
        Token.objects.create(user=instance)
