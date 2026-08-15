import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings

# <HINT> Create a Question Model with:
# Used to persist question content for a course
# - Many-to-one relationship with Course
# - Question content
# - Grade point for each question
# - Has calculate is_get_score method
class Question(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return "Question: " + self.content

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_incorrect == 0:
            return True
        return False


#  <HINT> Create a Choice Model with:
# - Used to persist choice content for a question
# - Many-to-one relationship with Question
# - Choice content
# - Indicate if this choice is the correct answer or not
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Choice: " + self.content


# <HINT> Create a Submission Model with:
# - Many-to-one relationship with Enrollment
# - Many-to-many relationship with Choice
# - Date and time of the submission
class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateField(default=now)

    def __str__(self):
        return "Enrollment: " + str(self.enrollment) + ", " + \
               "Date: " + str(self.date_submitted)
