"""
Faker floods the app with hundreds or thousands of mock analysis records to 
stress test how the system performs under real-world pressure.

python manage.py seed_stress_data --count 500
"""

import os
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from faker import Faker

from counter.models import AnalysisRecord
from counter.services.quality_insights import analyze_quality, get_basic_metrics
from counter.services.summarizer import generate_summary

load_dotenv()

class Command(BaseCommand):
    help = "Generate synthetic AnalysisRecord entries using Faker for stress testing."

    def add_arguments(self, parser):
        """Define command-line arguments for the stress-test seeding command."""
        
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of synthetic analysis records to generate.",
        )

        parser.add_argument(
            "--username",
            type=str,
            default=os.getenv("SEED_USERNAME", "stresstest_user"),
            help="Username to attach the generated records to."
        )


    def handle(self, *args, **options):
        """Execute the command to generate and save synthetic analysis records."""

        count = options["count"]
        username = options["username"]
        password = os.getenv("SEED_PASSWORD", "SecureStressTestPassword")
        fake = Faker()

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created test user: {username}"))
        else:
            self.stdout.write(f"Using existing user: {username}")

        self.stdout.write(f"Generating {count} synthetic analysis records for '{username}'..")

        records_to_create = []

        for _ in range(count):
            text = " ".join(fake.paragraphs(nb=random.randint(3, 8)))
            metrics = get_basic_metrics(text)
            summary_data = generate_summary(text)
            quality_data = analyze_quality(text)

            records_to_create.append(
                AnalysisRecord(
                    user=user,
                    title=fake.sentence(nb_words=4),
                    original_text=text,
                    word_count=metrics["word_count"],
                    summary=summary_data["summary"],
                    topics=summary_data["topics"],
                    bullets=summary_data["bullets"],
                    longest_sentence=quality_data["longest_sentence"],
                    ttr=quality_data["ttr"],
                    overused=quality_data["overused"],
                    passive_count=quality_data["passive_count"],
                )
            )

        # Bulk create for optimal performance during large stress runs
        AnalysisRecord.objects.bulk_create(records_to_create, batch_size=100)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {count} stress-test records."
            )
        )
