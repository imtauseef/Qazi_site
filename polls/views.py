from django.db.models.base import Model
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choices
from django.views import generic
from django.utils import timezone

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index_page.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """ Return the last five question (not include those set to be published in the future.)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:3]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail_page.html'

    def get_queryset(self):
        """
        Exclude all that questions whose pub_date is in future."""
        return Question.objects.filter(pub_date__lte=timezone.now())


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