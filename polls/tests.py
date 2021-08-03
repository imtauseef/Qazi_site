from django.test import TestCase
from .models import Question
from django.utils import timezone
import datetime
from django.urls import reverse
# Create your tests here.

def create_question(question_text, days):
    """ Create a question with the given `question_text` and published the given number of `days`
    offset to now (negative for the question published in the past, positive for the question yet
    to be published. """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestiionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the 
        index page.
        """
        question = create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question'], [question])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the
        indexed page.
        """
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future exists, only past questions are
        displayed.
        """
        create_question(question_text='Future question.', days=30)
        question = create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question'], [question])

    def test_two_past_questions(self):
        """
        The question index page may displayed multiple questions..
        """
        question1 = create_question(question_text='Past question 1.', days=-30)
        question2 = create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question'], [question2, question1])    

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_recently_pub() returns false for questions whose pub_date is
        in future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_recently_pub() returns false for question whose pub_date is 
        older than one day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        older_question = Question(pub_date=time)
        self.assertIs(older_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_recently_pub() returns true for question whose pub_date is within 
        the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)