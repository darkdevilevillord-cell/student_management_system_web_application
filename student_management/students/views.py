from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from django.contrib import messages
from django.db.models import Q

def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(Q(name__icontains=query))
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        course = request.POST.get('course')
        if name and age and course:
            try:
                age = int(age)
                Student.objects.create(name=name, age=age, course=course)
                messages.success(request, 'Student added successfully!')
                return redirect('student_list')
            except ValueError:
                messages.error(request, 'Invalid age.')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'students/student_form.html', {'title': 'Add Student'})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        course = request.POST.get('course')
        if name and age and course:
            try:
                age = int(age)
                student.name = name
                student.age = age
                student.course = course
                student.save()
                messages.success(request, 'Student updated successfully!')
                return redirect('student_list')
            except ValueError:
                messages.error(request, 'Invalid age.')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'students/student_form.html', {'student': student, 'title': 'Edit Student'})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
