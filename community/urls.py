from django.urls import path
from . import views

urlpatterns = [
    path('community', views.community, name='community'),
    path('ask-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    # path('reply', views.replyPage, name='reply')
]
