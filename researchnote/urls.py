from django.urls import path
from researchnote import views

urlpatterns = [
    # path('create-account', views.join, name='join'),
    # path('join/<str:username>', views.create, name='account'),
    # path('where-next/', views.loginTo),
    # path('profile/change-password', views.researcherChangePassword, name='researcher_change_password'),
    # path('dashboard', views.showResearcherBoard, name='researcher_board'),
    # path('profile', views.showResearcherProfile, name='researcher_profile'),
    # path('collab', views.showCollabs, name='collab'),
    # path('collab/create-collab', views.createCollab, name='create_collab'),
    # path('collab/view-researcher/<str:email>/', views.showUser, name='show_user'),
    # path('collab/view/<str:id>/', views.showCollab, name='show_collab'),
    # path('collab/view/<str:id>/update', views.updateCollab, name='update_collab'),
    # path('collab/view/<str:id>/delete', views.deleteCollab, name='delete_collab'),
    #
    # path('collab/view-initiated/<str:id1>/', views.showCollabInitiated, name='show_collab_initiated'),
    # path('collab/view-initiated/<str:id1>/collab-docs', views.showCollabDocsInitiated, name='collab_docs_initiated'),
    # path('collab/view-initiated/<str:id1>/tasks', views.showTasksInitiated, name='tasks_initiated'),
    # path('collab/view-accepted/<str:id1>/tasks', views.showTasksAccepted, name='tasks_accepted'),

    path('collab/view-initiated/<str:id1>/notes', views.showNotesInitiated, name='notes_initiated'),
    path('collab/view-initiated/<str:id1>/notes/<str:id2>', views.showNoteInitiated, name='show_note_initiated'),
    path('collab/view-accepted/<str:id1>/notes/<str:id2>', views.showNoteInitiated, name='show_note_accepted'),
    path('collab/view-accepted/<str:id1>/notes', views.showNotesInitiated, name='notes_accepted'),

    path('collab/view-initiated/<str:id1>/notes/delete/<str:id2>', views.deleteNoteInitiated, name='delete_note_initiated'),
    path('collab/view-accepted/<str:id1>/notes/delete/<str:id2>', views.deleteNoteInitiated, name='delete_note_accepted'),

    path('collab/view-initiated/<str:id1>/notes/pin/<str:id2>', views.pinNote, name='pin_note'),
    path('collab/view-accepted/<str:id1>/notes/pin/<str:id2>', views.pinNote, name='pin_note'),
    #
    # path('collab/view-initiated/<str:id1>/collab-docs/select/<str:id2>', views.selectDocInitiated, name='select_doc_initiated'),
    # path('collab/view-initiated/<str:id1>/collab-docs/deselect/<str:id2>', views.deselectDocInitiated, name='deselect_doc_initiated'),
    # path('collab/view-initiated/<str:id1>/collab-docs/update/<str:id2>', views.updateDocInitiated, name='update_doc_initiated'),
    #
    # path('collab/view-initiated/<str:id1>/tasks/edit/<str:id2>', views.editTaskInitiated, name='edit_task_initiated'),
    # path('collab/view-accepted/<str:id1>/tasks/update/<str:id2>', views.updateTaskAccepted, name='update_task_accepted'),
    # path('collab/view-initiated/<str:id1>/tasks/delete/<str:id2>', views.deleteTaskInitiated, name='delete_task_initiated'),
    #
    # path('collab/view-initiated/<str:id1>/tasks/pin/<str:id2>', views.pinTask, name='pin_task'),
    # path('collab/view-accepted/<str:id1>/tasks/pin/<str:id2>', views.pinTask, name='pin_task'),
    #
    # path('collab/view-initiated/<str:id1>/collab-docs/delete-all', views.deleteAllDocsInitiated, name='delete_all_docs_initiated'),
    # path('collab/view-initiated/<str:id1>/upload-doc', views.uploadDoc, name='upload_doc'),
    # path('collab/view-accepted/<str:id1>/upload-doc', views.uploadDoc, name='upload_doc'),
    # path('collab/view-initiated/<str:id1>/add-task', views.addTask, name='task'),
    # path('collab/view-accepted/<str:id1>/add-task', views.addTask, name='task'),
    #
    # path('collab/view-initiated/<str:id>/removed/<str:username>', views.removeCollab, name='remove_collab'),
    # path('collab/view-initiated/<str:id>/reported/<str:username>', views.reportCollaborator, name='report_collaborator'),
    #
    # path('collab/view-accepted/<str:id>/remove-requested/<str:username>', views.requestRemoveCollab, name='request_remove_collab'),
    # path('collab/view-accepted/<str:id>/', views.showCollabAccepted, name='show_collab_accepted'),
    # path('collab/view-accepted/<str:id1>/collab-docs', views.showCollabDocsAccepted, name='collab_docs_accepted'),
    #
    # path('collab/view-accepted/<str:id1>/collab-docs/select/<str:id2>', views.selectDocAccepted, name='select_doc_accepted'),
    # path('collab/view-accepted/<str:id1>/collab-docs/deselect/<str:id2>', views.deselectDocAccepted, name='deselect_doc_accepted'),
    #
    # path('collab/view-accepted/<str:id1>/collab-docs/delete-all', views.deleteAllDocsAccepted, name='delete_all_docs_accepted'),
    #
    # path('collab/view-accepted/<str:id>/reported', views.reportResearcher, name='report_researcher'),
    # path('collab/view-accepted/<str:id>/left/<str:username>', views.leaveCollab, name='leave_collab'),
    # path('collab/view-initiated/<str:id>/leave-accepted/<str:username>', views.acceptLeaveCollab, name='accept_leave_collab'),
    # path('collab/view/<str:id>/offered/<str:username>', views.offerCollab, name='offer_collab'),
    # path('collab/view/<str:id>/declined/<str:username>', views.declineCollab, name='decline_collab'),

]
