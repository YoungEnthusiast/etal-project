from django.db import models

# Create your models here.
class Question(models.Model):
    question_choices = [
		('Anyone', 'Anyone'),
        ('Affiliation', 'Affiliation'),
	]
    author = models.ForeignKey('account.Researcher', null=True, on_delete=models.SET_NULL)
    title = models.CharField(unique=True, max_length=200, null=True)
    question_type = models.CharField(max_length=11, default="Anyone", choices=question_choices, null=True)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_responses(self):
        return self.responses.filter(parent=None)

class Response(models.Model):
    user = models.ForeignKey('account.Researcher', null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField(null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def get_responses(self):
        return Response.objects.filter(parent=self)
