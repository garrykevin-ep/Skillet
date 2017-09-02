from django.test import TestCase

from .models import *
from .views import *

# Create your tests here.


def create_user():
	return User.objects.create(username="dummy",password="qwerty123")

def create_question():
	return FillQuestion.objects.create(question_text="1st fill")

def create_choice(question):
	return FillChoice.objects.create(question=question,choice_text="correct")

def create_status(user,question):
	return FillStatus.objects.get_or_create(User = user,question = question)

class FillQuestionTestCase(TestCase):
	
	def setUp(self):
		self.user = create_user()
		self.question = create_question()
		self.choice = create_choice(self.question)
		self.status = create_status(self.user,self.question)
	
	#answer_first_time
	def test_answer_first_time_correct(self):
		pass

	def test_answer_first_time_incorrect(self):
		pass

	def test_answer_first_time_blank(self):
		pass

	# blank_answer
	def test_blank_answer_last_answer_is_correct(self):
		pass

	def blank_answer_last_answer_is_incorrect(self):
		pass

	# answer_is_correct
	def answer_is_correct_last_answer_is_correct(self):
		pass

	def answer_is_correct_last_answer_is_incorrect(self):
		pass

	# answer_is_incorrect
	def answer_is_incorrect_last_answer_is_correct(self):
		pass

	def answer_is_incorrect_last_answer_is_incorrect(self):
		pass

class MultoQuestionTestCase(TestCase):
	
	def setUp(self):
		self.user = create_user()
		self.question = create_question()
		self.choice = create_choice(self.question)
		self.status = create_status(self.user,self.question)
	
	# answer_first_time
	def test_answer_first_time_correct(self):
		pass

	def test_answer_first_time_incorrect(self):
		pass

	def test_answer_first_time_blank(self):
		pass

	# blank_answer
	def test_blank_answer_last_answer_is_correct(self):
		pass

	def blank_answer_last_answer_is_incorrect(self):
		pass

	# answer_is_correct
	def answer_is_correct_last_answer_is_correct(self):
		pass

	def answer_is_correct_last_answer_is_incorrect(self):
		pass

	# answer_is_incorrect
	def answer_is_incorrect_last_answer_is_correct(self):
		pass

	def answer_is_incorrect_last_answer_is_incorrect(self):
		pass
