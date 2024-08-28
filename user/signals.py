from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(customer=instance)
        try:
            # Si quiero quiero que el gpo al guardar por defecto sea estudiantes
            group1 = Group.objects.get(name="Customers")
        # Si no existe
        except Group.DoesNotExist:
            group1 = Group.objects.create(name="Customers")
            group2 = Group.objects.create(name="Employees")
            group3 = Group.objects.create(name="DBAs")
            group4 = Group.objects.create(name="Admins")
        instance.groups.add(group1)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
