import qrcode
from io import BytesIO

from django.core.files import File
from django.core.management.base import BaseCommand

from verify.models import Student


class Command(BaseCommand):
    help = "Generate QR Codes for all students"

    def handle(self, *args, **kwargs):

        count = 0

        for student in Student.objects.all():

            if student.qr_image:
                continue

            url = f"http://127.0.0.1:8000/verify/{student.internship_id}/"

            qr = qrcode.make(url)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            filename = f"{student.internship_id}.png"

            student.qr_image.save(
                filename,
                File(buffer),
                save=True
            )

            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} QR Codes Generated Successfully."
            )
        )