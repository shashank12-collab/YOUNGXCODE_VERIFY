from django.shortcuts import render
from .models import Student
from django.shortcuts import render, get_object_or_404

def home(request):
    student = None
    error = None

    if request.method == "POST":
        certificate_id = request.POST.get("certificate_id")

        try:
            student = Student.objects.get(certificate_id=certificate_id)
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