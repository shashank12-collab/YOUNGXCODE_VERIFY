import pandas as pd
from datetime import datetime

from django.core.management.base import BaseCommand
from verify.models import Student


class Command(BaseCommand):
    help = "Import students from CSV"

    def handle(self, *args, **kwargs):

        df = pd.read_csv("students.csv")

        # Remove spaces from column names
        df.columns = df.columns.str.strip()

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            try:
                name = str(row.get("Name", "")).strip()
                role = str(row.get("Role", "")).strip()
                internship_id = str(row.get("Internship ID", "")).strip()
                email = str(row.get("Email", "")).strip()
                status = str(row.get("Status", "Verified")).strip()

                # Skip invalid rows
                if (
                    name == ""
                    or internship_id == ""
                    or internship_id.lower() == "nan"
                    or name.lower() == "nan"
                ):
                    skipped += 1
                    continue

                # Start Date
                start_date = row.get("Start Date")

                if pd.isna(start_date):
                    skipped += 1
                    continue

                start_date = pd.to_datetime(
                    start_date,
                    dayfirst=True
                ).date()

                # End Date
                end_date = row.get("End Date")

                if pd.isna(end_date):
                    end_date = datetime.strptime(
                        "06-07-2026",
                        "%d-%m-%Y"
                    ).date()
                else:
                    end_date = pd.to_datetime(
                        end_date,
                        dayfirst=True
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
                print(f"Skipped Row : {e}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImported : {imported}\nSkipped : {skipped}"
            )
        )