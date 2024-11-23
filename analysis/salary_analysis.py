import pymongo
import numpy as np

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["job_data"]
collection = db["jobs"]

# Helper to extract salary range
def extract_salary(salary_text):
    if not salary_text:
        return None
    try:
        salary_text = salary_text.replace("$", "").replace(",", "").split()
        return int(salary_text[0])
    except (ValueError, IndexError):
        return None

# Extract and clean salaries
salaries = [extract_salary(job["salary"]) for job in collection.find() if job["salary"]]
salaries = [s for s in salaries if s is not None]

# Calculate statistics
average_salary = np.mean(salaries)
median_salary = np.median(salaries)
std_dev_salary = np.std(salaries)

print(f"Average Salary: ${average_salary:.2f}")
print(f"Median Salary: ${median_salary:.2f}")
print(f"Standard Deviation: ${std_dev_salary:.2f}")
