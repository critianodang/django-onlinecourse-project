from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    if not user.is_authenticated:
        return redirect('onlinecourse:login')

    # Get enrollment instance
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # Collect selected choices from POST request
    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choice_ids.append(int(value))

    # Create submission and link choices
    submission = Submission.objects.create(enrollment=enrollment)
    for choice_id in selected_choice_ids:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)
    submission.save()

    return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id,)))


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    max_score = 0
    selected_ids = submission.choices.values_list('id', flat=True)

    for question in course.question_set.all():
        max_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context['course'] = course
    context['grade'] = total_score
    context['max_score'] = max_score
    context['submission'] = submission

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
