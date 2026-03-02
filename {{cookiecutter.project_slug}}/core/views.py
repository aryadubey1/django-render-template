from django.shortcuts import render


def home(request):
    context = {
        'project_name': '{{cookiecutter.project_name}}',
        'description': '{{cookiecutter.description}}',
    }
    return render(request, 'core/home.html', context)
