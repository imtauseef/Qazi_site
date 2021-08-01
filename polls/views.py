from django.db.models.base import Model
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choices

# Create your views here.
def index(request):
    latest_question = Question.objects.order_by('-pub_date')[:3]
    return render(request, 'polls/index_page.html', {'latest_question': latest_question})


def detail(request, pk):
    question = get_object_or_404(Question, id=pk)
    return render(request, 'polls/detail_page.html', {'question': question})

def result(request, pk):
    question = Question.objects.get(id=pk)
    return render(request, 'polls/results_page.html', {'question': question})

def vote(request, pk):
    question = get_object_or_404(Question, id=pk)
    try:
        selected_choice = question.choices_set.get(id=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        return render(request, 'polls/detail_page.html',
        {'question': question, 'error_message': 'this choice does not exist.'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))