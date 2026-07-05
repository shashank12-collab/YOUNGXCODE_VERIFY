from django.db import models
import uuid
import qrcode

from io import BytesIO
from django.core.files import File


class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()

    internship_id = models.CharField(max_length=50, unique=True)

    role = models.CharField(max_length=100)

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=20, default="Verified")

    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    qr_image = models.ImageField(upload_to="qr/", blank=True)

    certificate_1 = models.FileField(upload_to="certificates/", blank=True, null=True)
    certificate_2 = models.FileField(upload_to="certificates/", blank=True, null=True)

    def __str__(self):
        return self.name

    def generate_qr(self):
        url = f"http://127.0.0.1:8000/verify/{self.internship_id}/"

        qr = qrcode.make(url)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        filename = f"{self.internship_id}.png"

        self.qr_image.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_image:
            self.generate_qr()
            super().save(update_fields=["qr_image"])