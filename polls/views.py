from django.db.models.base import Model
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choices
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index_page.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail_page.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results_page.html'


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