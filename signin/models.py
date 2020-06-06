from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    available_for_hire = models.BooleanField(default=False)
    occupation = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(max_length=1000, blank=True, default='')

    gender_choices = (
        ("M","Male"),
        ("F","Female"),
        ("O","Other"),
    )
    gender = models.CharField(max_length=13, choices=gender_choices, blank=True,
                              default='')

    education = models.CharField(max_length=24, blank=True, default='')
    skills = TaggableManager(verbose_name='skills', blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)


class Hiree(models.Model):
    hirees = models.ManyToManyField(User, null=True)
    hirer = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                     related_name='hirer')

    @classmethod
    def hire(_class, hirer, new_hiree):
        _hirer, created = _class.objects.get_or_create(hirer=hirer)
        _hirer.hirees.add(new_hiree)

    @classmethod
    def free(_class, hirer, new_hiree):
        _hirer, created = _class.objects.get_or_create(hirer=hirer)
        _hirer.hirees.remove(new_hiree)

