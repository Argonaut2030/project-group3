from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


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
    return render(request, "file_manager/upload_file.html", {"form": form})


@login_required
def list_files(request, page=1):
    if not request.user.is_authenticated:
        return render(request, "files/file_list.html", {"user_authenticated": False})
    category = request.GET.get("category", "all")

    files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    if category != "all":
        files = files.filter(file__contains=f"/{category}/")
    per_page = 10
    paginator = Paginator(files, per_page)
    files_on_page = paginator.page(page)
    return render(
        request,
        "file_manager/file_list.html",
        {
            "files": files_on_page,
            "selected_category": category,
            "user_authenticated": True,
        },
    )


@login_required
def search_files(request):
    query = request.GET.get("f_search", "")
    category = request.GET.get("category", "all")

    files = UploadedFile.objects.filter(user=request.user)

    if query:
        files = files.filter(file__icontains=query)

    if category != "all":
        files = files.filter(file__contains=f"/{category}/")

    return render(
        request,
        "file_manager/file_list.html",
        {
            "files": files,
            "selected_category": category,
            "f_search": query,
        },
    )


@login_required
def delete_file(request, file_id):
    file = UploadedFile.objects.get(id=file_id)
    file.delete()
    messages.success(request, "File deleted successfully")
    return redirect("file_manager:file_list")