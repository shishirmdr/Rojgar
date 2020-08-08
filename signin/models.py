from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    available_for_hire = models.BooleanField(default=False)
    occupation = models.CharField(max_length=50, blank=True, default='')
    image = models.ImageField(upload_to="profile_pictures/%Y%m%d", default="", null=True, blank=True)
    cover_image = models.ImageField(upload_to="cover_images/%Y%m%d", default="", null=True, blank=True)

    category_choices = (
        ("P&T","Programming & Technology"),
        ("G&D","Graphics & Design"),
        ("DM","Digital Marketing"),
        ("W&T","Writing & Translation"),
        ("DE","Data Entry"),
        ("V&M","Video & Animation"),
        ("M&A","Music & Audio"),
        ("B&I","Business & Investment"),
        ("CS","Consulting Service"),
        ("M&P","Medical & Pharma"),
        ("AH","Architect Designs"),
        ("LI","Lifestyle"),
        ("AUD","Audit & Taxation"),
        ("QA","Quality Assurance"),
        ("ENG","Engineering Consultancy"),
        ("OM", "Organization Management"),
        ("RP","Repair & Technical Support"),
        ("E&T","Education & Teaching"),
    )

    category = models.CharField(max_length=40, choices=category_choices, default='E&T',)
    description = models.TextField(max_length=1000, default='', blank=True)

    gender_choices = (
        ("M","Male"),
        ("F","Female"),
        ("O","Other"),
    )
    gender = models.CharField(max_length=13, choices=gender_choices, blank=True,
                             default='')
    education = models.CharField(max_length=24, blank=True, default='')
    skills = TaggableManager(verbose_name='skills', blank=True)
    price = models.PositiveIntegerField(default=0, blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)


class Hiree(models.Model):
    hirees = models.ManyToManyField(User)
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


class Comment(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body      = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
