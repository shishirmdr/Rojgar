from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

class Seller(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False) # validators should be a list
    gender_choices = (
    ("Male","Male"),
    ("Female","Female"),
    ("Others","Others"),
    )
    gender = models.CharField(max_length=100, choices=gender_choices, default='')
    # profile_pic = models.ImageField(upload_to="profile_images/%Y%m%d", default='')
    description = models.TextField(max_length=1000, blank=False, default='')
    occupation = models.CharField(max_length=100, blank=False, default='')

    education_choices = (
    ("Currently Studying","Currently Studying"),
    ("Under SLC","Under SLC"),
    ("SLC","SLC"),
    ("Intermediate","Intermediate"),
    ("Bachelor","Bachelor"),
    ("Masters","Masters"),
    )
    education = models.CharField(max_length=100, choices=education_choices, default='')

    skills_choices = (
        ("Programming & Tech","Programming & Tech"),
        ("Graphics & Design","Graphics & Design"),
        ("Digital Marketing","Digital Marketing"),
        ("Writing & Translation","Writing & Translation"),
        ("Data Entry","Data Entry"),
        ("Video & Animation","Video & Animation"),
        ("Music & Sound","Music & Sound"),
        ("Business & Life Style","Business & Life Style"),
        ("Engineering","Engineering"),
        ("Teaching & Counselling","Teaching & Counselling"),
        ("Audit & Accountancy","Audit & Accountancy"),
        )
    skills = models.CharField(max_length=150, choices=skills_choices, default="")
    personal_website = models.URLField(max_length=250, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name



