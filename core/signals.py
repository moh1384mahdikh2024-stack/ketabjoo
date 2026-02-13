import uuid
from django.utils.text import  slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book, Category,Author


@receiver(pre_save, sender=Book)
def set_slug_book(sender, instance, **kwargs):
    if instance.pk:  # اگر آپدیت است
        old_title = sender.objects.get(pk=instance.pk).title
        if old_title != instance.title:
            base_slug = slugify(instance.title,allow_unicode=True)
            instance.slug = base_slug + "-" + uuid.uuid4().hex
    else:  # اگر ایجاد شی جدید است
        base_slug = slugify(instance.title,allow_unicode=True)
        instance.slug = f"{base_slug}-{uuid.uuid4().hex}"


@receiver(pre_save, sender=Category)
def set_slug_category(sender, instance, **kwargs):
    if instance.pk:
        print("slug")
        old_title = sender.objects.get(pk=instance.pk).title
        if old_title != instance.title:
            print("old_title")
            base_slug = slugify(instance.title,allow_unicode=True)
            slug = base_slug
            instance.slug = slug

    else:
        print("new slug")
        base_slug = slugify(instance.title,allow_unicode=True)
        slug = base_slug
        instance.slug = slug

@receiver(pre_save, sender=Author)
def set_slug_author(sender, instance, **kwargs):
    if instance.pk:
        old_name = sender.objects.get(pk=instance.pk).name
        if old_name != instance.name:
            base_slug = slugify(instance.name,allow_unicode=True)
            instance.slug = base_slug + "-" + uuid.uuid4().hex
    else:
        base_slug = slugify(instance.name,allow_unicode=True)
        instance.slug = f"{base_slug}-{uuid.uuid4().hex}"

