from django.shortcuts import render, get_object_or_404
from .models import Student


def home(request):
    student = None
    error = None

    if request.method == "POST":
        internship_id = request.POST.get("internship_id")

        try:
            student = Student.objects.get(internship_id=internship_id)
        except Student.DoesNotExist:
            error = "Certificate Not Found"

    return render(request, "home.html", {
        "student": student,
        "error": error
    })


def verify_certificate(request, internship_id):
    student = get_object_or_404(
        Student,
        internship_id=internship_id
    )

    return render(
        request,
        "verify.html",
        {
            "student": student
        }
    )