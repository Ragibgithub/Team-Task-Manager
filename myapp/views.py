from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count

@login_required
def dashboard(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    total_tasks = tasks.count()
    done_tasks = tasks.filter(status__iexact='Done').count()
    pending_tasks = tasks.exclude(status__iexact='Done').count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'pending_tasks': pending_tasks,
    }

    return render(request, 'dashboard.html', context)


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        project_id = request.POST['project']

        from .models import Project
        project = Project.objects.get(id=project_id)

        Task.objects.create(
            title=title,
            description=description,
            project=project,
            assigned_to=request.user
        )

        return redirect('dashboard')

    from .models import Project
    projects = Project.objects.all()
    return render(request, 'create_task.html', {'projects': projects})


@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.status == 'To Do':
        task.status = 'In Progress'
    elif task.status == 'In Progress':
        task.status = 'Done'
    else:
        task.status = 'To Do'

    task.save()
    return redirect('dashboard')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'signup.html')


