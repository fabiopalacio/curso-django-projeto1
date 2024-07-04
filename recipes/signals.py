import os

from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from recipes.models import Recipe


def delete_cover(instance):
    if instance.cover.name:
        try:
            os.remove(instance.cover.path)
        except (ValueError, FileNotFoundError):
            ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    if instance.cover.name:
        delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update_pre_save(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    if old_instance:
        is_new_cover = old_instance.cover != instance.cover
        if is_new_cover:
            instance.old_instance = old_instance


@receiver(post_save, sender=Recipe)
def recipe_cover_update_post_save(sender, instance, *args, **kwargs):
    if instance.old_instance:
        delete_cover(instance.old_instance)
