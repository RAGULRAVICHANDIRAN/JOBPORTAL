"""
JobPilot AI — Demo Seed Data

Seeds the database with demo job portals and sample jobs for the mock connector.
All demo data is clearly labeled.
"""

from sqlalchemy import select
from app.database import async_session
from app.models.portal import JobPortal
from app.models.job import Job, JobSkill


async def seed_demo_data():
    """Seed demo portals and sample jobs if they don't already exist."""
    async with async_session() as db:
        # Check if already seeded
        result = await db.execute(select(JobPortal).where(JobPortal.slug == "demo"))
        if result.scalar_one_or_none():
            return  # Already seeded

        # --- Seed Job Portals ---
        portals = [
            JobPortal(
                name="Demo Portal",
                slug="demo",
                base_url="https://demo.jobpilot.local",
                supports_search=True,
                supports_apply=True,
                supports_status_tracking=True,
                supports_oauth=False,
                requires_manual_auth=False,
                is_demo=True,
            ),
            JobPortal(
                name="LinkedIn",
                slug="linkedin",
                base_url="https://www.linkedin.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=True,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Indeed",
                slug="indeed",
                base_url="https://www.indeed.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Naukri",
                slug="naukri",
                base_url="https://www.naukri.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Wellfound",
                slug="wellfound",
                base_url="https://wellfound.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Internshala",
                slug="internshala",
                base_url="https://internshala.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Glassdoor",
                slug="glassdoor",
                base_url="https://www.glassdoor.com",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
            JobPortal(
                name="Foundit",
                slug="foundit",
                base_url="https://www.foundit.in",
                supports_search=True,
                supports_apply=False,
                supports_status_tracking=False,
                supports_oauth=False,
                requires_manual_auth=True,
                is_demo=False,
            ),
        ]
        db.add_all(portals)
        await db.flush()

        # --- Seed Demo Jobs ---
        demo_jobs = [
            {
                "title": "Python Developer",
                "company": "TechCorp India (DEMO)",
                "location": "Bangalore",
                "remote_type": "hybrid",
                "salary_min": 600000, "salary_max": 1200000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 2,
                "company_type": "product",
                "description": "We are looking for a Python Developer to join our engineering team. You will work on building scalable backend services using Python, Django/FastAPI, and PostgreSQL. Ideal for freshers with strong Python fundamentals.",
                "requirements": "Strong Python skills, understanding of REST APIs, SQL databases, Git. Nice to have: Docker, AWS, CI/CD.",
                "skills": [("Python", True), ("Django", True), ("PostgreSQL", True), ("REST APIs", True), ("Git", True), ("Docker", False), ("AWS", False)],
            },
            {
                "title": "Data Analyst",
                "company": "DataMinds Analytics (DEMO)",
                "location": "Chennai",
                "remote_type": "onsite",
                "salary_min": 400000, "salary_max": 800000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 1,
                "company_type": "mnc",
                "description": "Join our analytics team to transform raw data into actionable insights. Work with SQL, Python, Excel, and Power BI to create dashboards and reports for business stakeholders.",
                "requirements": "SQL proficiency, Python (Pandas, NumPy), Excel, Power BI or Tableau. Statistics knowledge preferred.",
                "skills": [("SQL", True), ("Python", True), ("Power BI", True), ("Excel", True), ("Pandas", True), ("Statistics", False)],
            },
            {
                "title": "AI/ML Engineer",
                "company": "NeuralWorks AI (DEMO)",
                "location": "Hyderabad",
                "remote_type": "remote",
                "salary_min": 800000, "salary_max": 1500000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 3,
                "company_type": "startup",
                "description": "Build and deploy machine learning models for NLP, computer vision, and recommendation systems. Work with cutting-edge AI frameworks and large language models.",
                "requirements": "Python, TensorFlow/PyTorch, scikit-learn, NLP, Computer Vision. Experience with LLMs and fine-tuning is a plus.",
                "skills": [("Python", True), ("TensorFlow", True), ("PyTorch", False), ("NLP", True), ("scikit-learn", True), ("Computer Vision", False), ("LLMs", False)],
            },
            {
                "title": "Full Stack Developer",
                "company": "WebSphere Solutions (DEMO)",
                "location": "Pune",
                "remote_type": "hybrid",
                "salary_min": 500000, "salary_max": 1000000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 2,
                "company_type": "service",
                "description": "Develop end-to-end web applications using React, Node.js, and MongoDB. You will be involved in the full software development lifecycle from design to deployment.",
                "requirements": "React.js, Node.js, MongoDB, HTML/CSS, JavaScript, REST APIs. Knowledge of TypeScript and cloud services is a bonus.",
                "skills": [("React", True), ("Node.js", True), ("MongoDB", True), ("JavaScript", True), ("HTML/CSS", True), ("TypeScript", False)],
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudNative Systems (DEMO)",
                "location": "Bangalore",
                "remote_type": "remote",
                "salary_min": 700000, "salary_max": 1400000,
                "employment_type": "full-time",
                "experience_min": 1, "experience_max": 3,
                "company_type": "product",
                "description": "Manage CI/CD pipelines, infrastructure as code, and cloud deployments. Work with Docker, Kubernetes, Terraform, and AWS/GCP.",
                "requirements": "Linux, Docker, Kubernetes, CI/CD (Jenkins/GitHub Actions), Terraform, AWS or GCP. Scripting with Python/Bash.",
                "skills": [("Docker", True), ("Kubernetes", True), ("AWS", True), ("Terraform", True), ("Linux", True), ("CI/CD", True), ("Python", False)],
            },
            {
                "title": "Software Engineer Intern",
                "company": "InnovateTech (DEMO)",
                "location": "Remote",
                "remote_type": "remote",
                "salary_min": 15000, "salary_max": 30000,
                "salary_period": "monthly",
                "employment_type": "internship",
                "experience_min": 0, "experience_max": 0,
                "company_type": "startup",
                "description": "3-month internship for final year students. Work on real projects using Python, JavaScript, and learn modern development practices. Possibility of full-time conversion.",
                "requirements": "Currently pursuing B.Tech/BE/MCA. Knowledge of any programming language. Eager to learn.",
                "skills": [("Python", False), ("JavaScript", False), ("Git", False)],
            },
            {
                "title": "Data Scientist",
                "company": "Quantix Research (DEMO)",
                "location": "Mumbai",
                "remote_type": "hybrid",
                "salary_min": 900000, "salary_max": 1800000,
                "employment_type": "full-time",
                "experience_min": 1, "experience_max": 4,
                "company_type": "mnc",
                "description": "Apply statistical modeling, machine learning, and deep learning to solve complex business problems. Work with large datasets and build predictive models.",
                "requirements": "Python, R, SQL, Machine Learning, Deep Learning, Statistics, Data Visualization. PhD or Master's preferred.",
                "skills": [("Python", True), ("R", False), ("SQL", True), ("Machine Learning", True), ("Statistics", True), ("Deep Learning", False)],
            },
            {
                "title": "Backend Engineer",
                "company": "FinServe Technologies (DEMO)",
                "location": "Bangalore",
                "remote_type": "onsite",
                "salary_min": 600000, "salary_max": 1100000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 2,
                "company_type": "product",
                "description": "Build high-performance backend services for our fintech platform. Work with Java/Python, microservices, message queues, and relational databases.",
                "requirements": "Java or Python, Spring Boot or FastAPI, SQL, Redis, message queues (Kafka/RabbitMQ). Understanding of financial systems is a plus.",
                "skills": [("Python", True), ("FastAPI", True), ("SQL", True), ("Redis", True), ("Microservices", True), ("Kafka", False)],
            },
            {
                "title": "QA Engineer",
                "company": "TestPro Labs (DEMO)",
                "location": "Chennai",
                "remote_type": "onsite",
                "salary_min": 400000, "salary_max": 700000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 1,
                "company_type": "service",
                "description": "Design and execute test plans, write automated tests, perform regression testing, and ensure product quality. Work closely with development teams.",
                "requirements": "Manual testing, Selenium/Playwright, Python or Java, SQL, API testing, JIRA. ISTQB certification is a plus.",
                "skills": [("Selenium", True), ("Python", True), ("SQL", True), ("API Testing", True), ("JIRA", False)],
            },
            {
                "title": "Mobile Developer — React Native",
                "company": "AppForge Studio (DEMO)",
                "location": "Hyderabad",
                "remote_type": "hybrid",
                "salary_min": 500000, "salary_max": 1000000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 2,
                "company_type": "startup",
                "description": "Build cross-platform mobile applications using React Native. Collaborate with designers and backend engineers to deliver beautiful, performant apps.",
                "requirements": "React Native, JavaScript/TypeScript, React, Redux/Zustand, REST APIs. Experience with native modules (iOS/Android) is a bonus.",
                "skills": [("React Native", True), ("JavaScript", True), ("TypeScript", False), ("React", True), ("Redux", False)],
            },
            {
                "title": "Cloud Engineer",
                "company": "SkyScale Infrastructure (DEMO)",
                "location": "Pune",
                "remote_type": "remote",
                "salary_min": 700000, "salary_max": 1300000,
                "employment_type": "full-time",
                "experience_min": 1, "experience_max": 3,
                "company_type": "mnc",
                "description": "Design, deploy, and maintain cloud infrastructure on AWS/GCP. Implement security best practices, cost optimization, and high-availability architectures.",
                "requirements": "AWS or GCP certified, Terraform, CloudFormation, Networking, Security, Python/Bash scripting, Monitoring (Prometheus/Grafana).",
                "skills": [("AWS", True), ("GCP", False), ("Terraform", True), ("Networking", True), ("Python", False), ("Monitoring", False)],
            },
            {
                "title": "Business Analyst (EXCLUDE TEST — Sales)",
                "company": "SalesForce Co (DEMO)",
                "location": "Delhi",
                "remote_type": "onsite",
                "salary_min": 300000, "salary_max": 600000,
                "employment_type": "full-time",
                "experience_min": 0, "experience_max": 1,
                "company_type": "service",
                "description": "Drive sales growth through cold calling, telecalling, and business development activities. Meet monthly sales targets.",
                "requirements": "Sales experience, telecalling, business development, CRM tools.",
                "skills": [("Sales", True), ("Telecalling", True), ("CRM", True)],
            },
        ]

        from datetime import datetime, timezone, timedelta
        import hashlib

        for i, job_data in enumerate(demo_jobs):
            skills_data = job_data.pop("skills")
            posted = datetime.now(timezone.utc) - timedelta(hours=(i * 6 + 2))
            content = f"{job_data['title']}|{job_data['company']}|{job_data['location']}"
            content_hash = hashlib.sha256(content.encode()).hexdigest()

            job = Job(
                source="demo",
                external_job_id=f"DEMO-{i+1:03d}",
                external_url=f"https://demo.jobpilot.local/jobs/DEMO-{i+1:03d}",
                posted_at=posted,
                content_hash=content_hash,
                salary_period=job_data.pop("salary_period", "yearly"),
                **job_data,
            )
            db.add(job)
            await db.flush()

            for skill_name, is_required in skills_data:
                db.add(JobSkill(job_id=job.id, name=skill_name, is_required=is_required))

        await db.commit()
        print(f"  -> Seeded {len(portals)} portals and {len(demo_jobs)} demo jobs.")
