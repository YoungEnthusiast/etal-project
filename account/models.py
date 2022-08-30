from django.db import models
from django.contrib.auth.models import AbstractUser

class Researcher(AbstractUser):
    TYPE_CHOICES = [
        ('Researcher', 'Researcher'),
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
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Researcher', null=True)
    # bell = models.ForeignKey('account.Notification', null=True, blank=True, on_delete=models.SET_NULL)
    bell_unreads = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Researcher's Profile"
        verbose_name_plural = "Researcher's Profiles"

    def __str__(self):
        try:
            return str(self.first_name) + " " + str(self.last_name)
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
    education_choices = [
		('Bachelor (BSc.)','Bachelor (BSc.)'),
        ('Masters (MSc.)','Masters (MSc.)'),
        ('Doctorate (PhD)','Doctorate (PhD)'),
	]

    collaborators_choices = [
		('Anyone', 'Anyone'),
        ('Affiliation', 'Affiliation'),
	]

    researcher = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="researcher")
    collaborators_type = models.CharField(max_length=11, default="Anyone", choices=collaborators_choices, null=True)
    collaborators = models.ManyToManyField(Researcher, verbose_name="My Selection", blank=True, related_name="collaborator")
    title = models.CharField(max_length=255, null=True)
    abstract = models.TextField(max_length=500, null=True)
    proposed_timeline = models.CharField(max_length=255, null=True, verbose_name="Proposed Timeline")
    education = models.CharField(max_length=15, choices=education_choices, null=True)
    field = models.CharField(max_length=255, null=True)
    expertise_required = models.CharField(max_length=255, null=True, verbose_name="Expertise Required")
    on_premises = models.CharField(max_length=255, null=True, verbose_name="On Premises")
    funding = models.CharField(max_length=255, null=True)
    collaborators_no = models.CharField(max_length=255, null=True, verbose_name="Number of Collaborators")
    ownership = models.CharField(max_length=255, null=True, verbose_name="Research Ownership")

    interested_people = models.ManyToManyField(Researcher, blank=True, related_name="interested_people")
    interest = models.BooleanField(max_length=5, default = False)
    flag = models.ForeignKey('account.Flag', null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_collab")
    researcher_report = models.ForeignKey('account.ResearcherReport', null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_researcher_report")
    collaborator_report = models.ForeignKey('account.CollaboratorReport', null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_collaborator_report")
    is_locked = models.BooleanField(max_length=5, default = False)
    removed_people = models.ManyToManyField(Researcher, blank=True, related_name="removed_people")
    locked_date = models.DateTimeField(null=True, blank=True)
    accepted_date = models.DateTimeField(null=True, blank=True)
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

class Notification(models.Model):
    owner = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="owner")
    message = models.CharField(max_length=255, null=True, blank=True)
    unreads = models.PositiveIntegerField(default=0)
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="notification_collab")
    sender = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="sender")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.message)
        except:
            return str(self.id)

class Flag(models.Model):
    is_flagged = models.BooleanField(max_length=5, default = False)
    complainer = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_complainer")
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="flag_reason")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_collab")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.reason)
        except:
            return str(self.id)

class ResearcherReport(models.Model):
    is_reported = models.BooleanField(max_length=5, default = False)
    complainer = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="researcher_complainer")
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="researcher_collab")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.reason)
        except:
            return str(self.id)

class CollaboratorReport(models.Model):
    is_reported = models.BooleanField(max_length=5, default = False)
    complainer = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="collaborator_complainer")
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collaborator_collab")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.reason)
        except:
            return str(self.id)
