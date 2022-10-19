from django.db import models
from django.contrib.auth.models import AbstractUser

class Stranger(models.Model):
    first_username = models.EmailField(max_length=255, verbose_name="Enter institution email address")

class Researcher(AbstractUser):
    TYPE_CHOICES = [
        ('Researcher', 'Researcher'),
		('Admin', 'Admin'),
        ('SuperAdmin', 'SuperAdmin'),
    ]
    username = models.EmailField(max_length=255, unique=True, null=True, blank=True, verbose_name="Email")
    first_name = models.CharField(max_length=45, null=True, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=45, null=True, blank=True, verbose_name="Last Name")
    photograph = models.ImageField(upload_to='users_img/%Y/%m/%d', null=True, blank=True)
    affiliation_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Affiliation")
    affiliation_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Affiliation Address")
    city = models.CharField(max_length=255, blank=True, null=True,)
    state = models.CharField(max_length=255, blank=True, null=True,)
    country = models.CharField(max_length=255, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Researcher', null=True)
    # bell = models.ForeignKey('account.Notification', null=True, blank=True, on_delete=models.SET_NULL)
    bell_unreads = models.PositiveIntegerField(default=0)
    envelope_unreads = models.PositiveIntegerField(default=0)
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
		('0-2 years','0-2 years'),
        ('3-5 years','3-5 years'),
        ('6-10 years','6-10 years'),
        ('10+ years','10+ years'),
	]
    collaborators_choices = [
		('Anyone', 'Anyone'),
	]
    model_choices = [
		('On premise','On premise'),
        ('Remote','Remote'),
        ('Field','Field'),
        ('Remote (Field)','Remote (Field)'),
        ('Others','Others'),
	]
    researcher = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="researcher")
    collaborators_type = models.CharField(max_length=11, default="Anyone", choices=collaborators_choices, null=True)
    collaborators = models.ManyToManyField(Researcher, verbose_name="My Selection", blank=True, related_name="collaborator")
    title = models.CharField(max_length=255, null=True)
    abstract = models.TextField(max_length=2000, null=True, verbose_name="Reearch Description")
    proposed_timeline = models.CharField(max_length=255, null=True, verbose_name="Proposed Timeline")
    education = models.CharField(max_length=20, choices=education_choices, null=True, verbose_name="Collaborators Research Experience")
    field = models.CharField(max_length=255, null=True)
    expertise_required = models.CharField(max_length=255, null=True, verbose_name="Collaborator's Expertise")
    collaborators_no = models.CharField(max_length=255, null=True, verbose_name="Number of Collaborators")
    funding = models.CharField(max_length=100, null=True, verbose_name="Funding")
    model = models.CharField(max_length=14, choices=model_choices, null=True, verbose_name="Collaboration Model")

    interested_people = models.ManyToManyField(Researcher, blank=True, related_name="interested_people")
    interest = models.BooleanField(max_length=5, default = False)
    flag = models.ForeignKey('account.Flag', null=True, blank=True, on_delete=models.SET_NULL, related_name="flag_collab")
    report = models.ForeignKey('account.Report', null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_report")
    is_locked = models.BooleanField(max_length=5, default = False)
    removed_people = models.ManyToManyField(Researcher, blank=True, related_name="removed_people")
    request_removed_people = models.ManyToManyField(Researcher, blank=True, related_name="request_removed_people")
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
    sender = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="notification_sender")
    room = models.CharField(max_length=255, null=True, blank=True)
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

class Report(models.Model):
    is_reported = models.BooleanField(max_length=5, default = False)
    complainer = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="report_complainer")
    # reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="researcher_collab")
    receiver = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.reason)
        except:
            return str(self.id)

class Folder(models.Model):
    name = name = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL)
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_folder")
    is_selected = models.ManyToManyField(Researcher, blank=True, related_name="is_selected_folder")
    # created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.reason)
        except:
            return str(self.id)

class CollabDoc(models.Model):
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_collab_doc")
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_collab_folder")
    shared_by = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    document = models.FileField(upload_to='collab_documents/', verbose_name="File")
    is_selected = models.ManyToManyField(Researcher, blank=True, related_name="is_selected")
    doc_collaborators = models.ManyToManyField(Researcher, blank=True, related_name="doc_collaborators")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.name)
        except:
            return str(self.id)

class Task(models.Model):
    STATUS_CHOICES = [
        ('Ongoing','Ongoing'),
        ('Completed', 'Completed'),
        ('Stopped', 'Stopped')
    ]
    poster = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="task_poster")
    serial = models.CharField(max_length=4, null=True, blank=True)
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_task")
    is_pinned = models.BooleanField(max_length=5, default = False)

    assigned_to = models.ManyToManyField(Researcher, blank=True, verbose_name="Assign", related_name="assigned_to")
    title = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=150, null=True)
    update_text = models.CharField(max_length=150, blank=True, verbose_name="Description", null=True)
    text_editor = models.ManyToManyField(Researcher, blank=True, related_name="text_editor")
    is_selected = models.ManyToManyField(Researcher, blank=True, related_name="is_selected_task")
    due_date = models.DateField(blank=True, null=True, verbose_name="Due Date")
    updated_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Ongoing', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('serial',)

    def __str__(self):
        try:
            return str(self.title)
        except:
            return str(self.id)
