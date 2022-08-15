from django.db import models
from django.contrib.auth.models import AbstractUser

class Researcher(AbstractUser):
    TYPE_CHOICES = [
        ('Researcher', 'Researcher'),
        ('Collaborator', 'Collaborator'),
		('Admin', 'Admin'),
        ('SuperAdmin', 'SuperAdmin'),
    ]
    username = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=45, null=True, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=45, null=True, blank=True, verbose_name="Last Name")
    photograph = models.ImageField(upload_to='users_img/%Y/%m/%d', null=True, blank=True)
    affiliation_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Affiliation Name")
    affiliation_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Affiliation Address")
    city = models.CharField(max_length=255, blank=True, null=True,)
    state = models.CharField(max_length=255, blank=True, null=True,)
    country = models.CharField(max_length=255, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)

    type = models.CharField(max_length=12, choices=TYPE_CHOICES, default='Researcher', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Researcher's Profile"
        verbose_name_plural = "Researcher's Profiles"

    def __str__(self):
        try:
            return str(self.username) + " | " + str(self.first_name) + " " + str(self.last_name)
        except:
            return str(self.id)

    @property
    def photographURL(self):
        try:
            url = self.photograph.url
        except:
            url = ''
        return url


    # def get_absolute_url(self):
    #     return reverse('detail', kwargs={'pk': self.pk})

class Collab(models.Model):
    education_type = [
		('Bachelor (BSc.)','Bachelor (BSc.)'),
        ('Masters (MSc.)','Masters (MSc.)'),
        ('Doctorate (PhD)','Doctorate (PhD)'),
	]

    # user = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)
    # order_Id = models.IntegerField(blank=True, null=True)
    # cylinder = models.ManyToManyField('products.Product', related_name='anti_cylinders')
    title = models.CharField(max_length=255, null=True)
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='anti_products')
    abstract = models.TextField(max_length=500, null=True)
    # outlet_static = models.CharField(max_length=30, blank=True, null=True)
    # who6_2 = models.CharField(max_length=9, blank=True, null=True)
    # quantity = models.PositiveIntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        # verbose_name = "Researcher's Profile"
        # verbose_name_plural = "Researcher's Profiles"

    def __str__(self):
        try:
            return str(self.title)
        except:
            return str(self.id)
