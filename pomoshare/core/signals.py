from .models import ModifiedUserModel, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ModifiedUserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(profile_of = instance)
        profile.save()
