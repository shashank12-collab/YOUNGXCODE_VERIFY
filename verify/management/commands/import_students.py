import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from verify.models import Student


class Command(BaseCommand):
    help = "Import students from CSV"

    def handle(self, *args, **kwargs):

        imported = 0
        skipped = 0

        with open("students.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Remove spaces from column names
            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            for row in reader:

                row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}

                try:
                    name = row.get("Name", "")
                    role = row.get("Role", "")
                    internship_id = row.get("Internship ID", "")
                    email = row.get("Email", "")
                    status = row.get("Status", "Verified")

                    if not name or not internship_id:
                        skipped += 1
                        continue

                    start_date = row.get("Start Date", "")

                    if not start_date:
                        skipped += 1
                        continue

                    start_date = datetime.strptime(
                        start_date,
                        "%d-%m-%Y"
                    ).date()

                    end_date = row.get("End Date", "")

                    if not end_date:
                        end_date = datetime.strptime(
                            "06-07-2026",
                            "%d-%m-%Y"
                        ).date()
                    else:
                        end_date = datetime.strptime(
                            end_date,
                            "%d-%m-%Y"
                        ).date()

                    Student.objects.update_or_create(
                        internship_id=internship_id,
                        defaults={
                            "name": name,
                            "email": email,
                            "role": role,
                            "start_date": start_date,
                            "end_date": end_date,
                            "status": status if status else "Verified",
                        },
                    )

                    imported += 1

                except Exception as e:
                    skipped += 1
                    print(f"Skipped Row: {e}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported: {imported}\nSkipped: {skipped}"
            )
        )