from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm, FileAnalysisForm, UserLoginForm
from .models import FileAnalysis

global site_name
site_name = "AutoCAD Take-off"
@login_required
def home(request):
    form = FileAnalysisForm()

    if request.method == 'POST':
        form = FileAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the user field to the logged-in user
            form.instance.user = request.user
            form.save()
            messages.success(request, "File analysis data saved successfully.")
            return redirect('analysis')
        else:
            print(form.errors)
    else:
        form = FileAnalysisForm()

    # Retrieve analyses for the current user
    analyses = FileAnalysis.objects.filter(user=request.user)

    return render(request, 'homepage.html', {'form': form, 'analyses': analyses})





def public_home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)

            # Add a success message
            messages.success(request, "Registration successful. You are now logged in.")

            return redirect('login')  # Redirect to your home page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')  # Redirect to your home page
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


@login_required
def file_analysis(request):
    if request.method == 'POST':
        form = FileAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.filename = form.cleaned_data['filename']
            form.instance.note = form.cleaned_data['note']
            form.save()
            messages.success(request, "File analysis data saved successfully.")
            return redirect('analysis')
    else:
        form = FileAnalysisForm()

    analyses = FileAnalysis.objects.filter(user=request.user)
    context = {
        'form': form,
        'analyses': analyses
    }
    return render(request, 'analysis.html', context)




@login_required
def delete_file(request, file_id):
    file_analysis = get_object_or_404(FileAnalysis, id=file_id, user=request.user)

    if request.method == 'POST':
        file_analysis.delete()
        messages.success(request, "File analysis data deleted successfully.")
        return redirect('analysis')  # Redirect to your homepage or wherever you want

    return render(request, 'delete_confirmation.html', {'file_analysis': file_analysis})