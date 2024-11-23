from django.db import models
from pymongo import MongoClient

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255, null=True, blank=True)
    scraped_at = models.DateTimeField()

    def __str__(self):
        return self.title

    @classmethod
    def load_from_mongodb(cls):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["job_data"]
        collection = db["jobs"]
        for job in collection.find():
            cls.objects.update_or_create(
                title=job["title"],
                company=job["company"],
                location=job["location"],
                defaults={"salary": job["salary"], "scraped_at": job["scraped_at"]}
            )
