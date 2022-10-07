from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import NewQuestionForm, NewResponseForm, NewReplyForm
from django.contrib import messages

@login_required
def community(request):
    questions = Question.objects.all().order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'community/questions.html', context)

@login_required
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'community/new-question.html', context)

@login_required
def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'community/question.html', context)

@login_required
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')

@login_required
def updateQuestion(request, id):
    question = Question.objects.get(id=id)
    if question.author == request.user:
        form = NewQuestionForm(instance=question)
        if request.method=='POST':
            form = NewQuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                messages.info(request, "The question has been updated successfully")
                return redirect('update_question', id)
    else:
        return redirect('community')
    return render(request, 'community/update_question.html', {'form': form, 'question':question})

@login_required
def deleteQuestion(request, id):
    question = Question.objects.get(id=id)
    obj = get_object_or_404(Question, id=id)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The question has been deleted successfully")
        return redirect('community')
    return render(request, 'community/question_confirm_delete.html', {'question':question})
