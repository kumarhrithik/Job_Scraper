### **README.md**

# **Job Scraper Project**

## **Overview**
This project is a Python-based web scraping and data analysis tool designed to:
1. Scrape job listings from **Indeed.com**.
2. Store the scraped job data in a **MongoDB database**.
3. Provide a **Django Admin panel** to view, edit, and manage the job data.
4. Perform salary analysis using **NumPy** to compute the average salary for Python developers.

---

## **Directory Structure**

```
job_scraper/
├── scraper/
│   ├── scrape_jobs.py                 # Main scraping script with Selenium & BeautifulSoup
│   ├── scraper_jobs_request_method.py # Alternative scraper using Requests & BeautifulSoup
│   ├── requirements.txt               # Project dependencies
├── django_app/
│   ├── job_manager/
│   │   ├── admin.py                   # Django admin configurations
│   │   ├── models.py                  # Django model for job data
│   │   ├── views.py                   # Views for job management
│   │   ├── urls.py                    # URL routing for the job manager
│   ├── job_scraper/
│   │   ├── settings.py                # Django project settings
│   │   ├── urls.py                    # URL routing for the Django app
│   │   ├── wsgi.py                    # WSGI configuration
│   ├── manage.py                      # Django management tool
├── analysis/
│   ├── salary_analysis.py             # Salary analysis using NumPy
```

---

## **Features**

1. **Web Scraping**:
   - Scrapes job data (title, company, location, salary, description, etc.) using **Selenium** and **BeautifulSoup**.
   - Handles pagination to scrape multiple pages.

2. **Database Integration**:
   - Stores the scraped data in a **MongoDB database** for persistence and further analysis.

3. **Django Admin Panel**:
   - Provides a user-friendly interface for viewing, editing, and managing job data.

4. **Salary Analysis**:
   - Computes the average salary for Python developers using **NumPy**.

---

## **Setup**

### **Prerequisites**
- Python 3.8+
- MongoDB
- Google Chrome and ChromeDriver (ensure the versions match)
- Install the required Python packages.

---

### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/job-scraper.git
   cd job-scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r scraper/requirements.txt
   ```

3. **Set Up MongoDB**:
   - Ensure MongoDB is running locally or provide your MongoDB URI in `.env`.

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory and add:
     ```env
     MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
     ```

5. **Run the Scraper**:
   - Using Selenium:
     ```bash
     python scraper/scrape_jobs.py
     ```
   - Using Requests:
     ```bash
     python scraper/scraper_jobs_request_method.py
     ```

6. **Run Django Server**:
   - Navigate to the `django_app/` directory:
     ```bash
     python manage.py runserver
     ```
   - Open the Django admin panel at `http://127.0.0.1:8000/admin/`.

---

## **Usage**

### **Scrape Job Data**
1. Define the search keyword and location in `scraper/scrape_jobs.py`.
2. Run the script to scrape job data:
   ```bash
   python scraper/scrape_jobs.py
   ```

### **Analyze Salary Data**
1. Run the salary analysis script:
   ```bash
   python analysis/salary_analysis.py
   ```
2. View the average salary output in the console.

### **Manage Job Data**
1. Open the Django admin panel at `http://127.0.0.1:8000/admin/`.
2. View, edit, or delete job records.

---

## **Scripts Overview**

### **1. Scraper Scripts**

- **`scrape_jobs.py`**:
  - Uses Selenium for dynamic page handling.
  - Extracts job details from individual job pages.

- **`scraper_jobs_request_method.py`**:
  - Uses Requests for fast static page scraping.
  - Suitable for scraping without dynamic content.

### **2. Salary Analysis Script**

- **`salary_analysis.py`**:
  - Connects to MongoDB to fetch job data.
  - Parses salary ranges and calculates the average using NumPy.

---

## **Technology Stack**

- **Backend**: Django
- **Scraping Tools**: Selenium, BeautifulSoup, Requests
- **Database**: MongoDB
- **Analysis**: NumPy

---

## **Dependencies**

Listed in `requirements.txt`:
```txt
beautifulsoup4==4.12.2
numpy==1.26.0
pymongo==4.7.0
requests==2.31.0
selenium==4.12.0
selenium-stealth==1.0.6
python-dotenv==1.0.0
Django==4.2
```

---

## **Known Issues**

1. **Cloudflare Captchas**:
   - Some job pages may require manual verification.
   - Use the `selenium_stealth` package to bypass detection but its still not able to bypass it.

2. **Rate Limiting**:
   - Add random delays between requests to avoid blocking.

---
