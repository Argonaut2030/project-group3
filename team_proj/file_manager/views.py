from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import UploadedFile

@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect("file_manager:file_list") 
    else:
        form = FileUploadForm()
    return render(request, "upload_file.html", {"form": form})


@login_required
def list_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, "file_list.html", {"files": files})
