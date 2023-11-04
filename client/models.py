from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

RACE_CHOICES = (
    ('human', 'HUMAN'),
    ('orc', 'ORC'),
    ('elf', 'elf'),
    ('elf2', 'elf2'),
    ('ГНОМ', 'ГНОМ'),
    ('Кожаный мешок', 'Кожаный мешок'),
)

CLASS_CHOICES = (
    ('warrior', 'WARRIOR'),
    ('wizard', 'WIZARD'),
)

RARE_CHOICES = (
    ('basic', 'BASIC'),
    ('rare', 'RARE'),
    ('epic', 'EPIC'),
    ('legendary', 'LEGENDARY'),
)

PRODUCT_TYPE_CHOICES = (
    ('basic', 'BASIC'),
    ('magic', 'MAGIC'),
    ('alchemy', 'ALCHEMY'),
)

LOCS_CHOICES = (
    ('forest', 'FOREST'),
    ('hometown', 'HOMETOWN'),
    ('big cityy', 'BIG CITY'),
)


class ClassChoice(models.Model):
    class_name = models.CharField(max_length=255)


for_race_choice = [(i.class_name,i.class_name) for i in ClassChoice.objects.all()]
print(f"Debug {for_race_choice}")

class Product(models.Model):
    user_pk = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    number_of_uses = models.CharField(max_length=255)
    product_img = models.ImageField(null=True, blank=True, upload_to="images/product/",
                                    default='images/deafult-product-image.png')
    price = models.IntegerField(default=1)
    rare = models.CharField(max_length=10, choices=RARE_CHOICES, default='basic')
    type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default='basic')
    location = models.CharField(max_length=20, choices=LOCS_CHOICES, default='hometown')

    def get_absolute_url(self):
        return reverse('product', args=[self.id])


class CustomClient(AbstractUser):
    game_username = models.CharField(max_length=30, default='username for game')
    race = models.CharField(max_length=30, choices=RACE_CHOICES, default='human')
    # слово class зарезервированно в python
    telegram_username = models.CharField(max_length=30, default='username_not_here')
    class_name = models.CharField(max_length=30, choices=for_race_choice, default='warrior')
    history = models.TextField(default='История скрыта')
    money = models.IntegerField(default=0)
    profile_avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/",
                                       default='images/deafult-profile-image.png')  # нужно скачать аву по умолчанию
    location = models.CharField(max_length=20, choices=LOCS_CHOICES, default='hometown')
