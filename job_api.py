from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

# Model for Job
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    stipend = db.Column(db.Float)
    gender = db.Column(db.String(10))
    accommodation = db.Column(db.Boolean)
    transport = db.Column(db.Boolean)
    benefits = db.Column(db.String(200))
    working_hours = db.Column(db.String(50))
    applications = db.relationship('JobApplication', backref='job', lazy=True)


# Model for Job Applications
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)


# API to fetch all job details
@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    jobs = Job.query.all()
    job_list = [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "stipend": job.stipend,
            "gender": job.gender,
            "accommodation": job.accommodation,
            "transport": job.transport,
            "benefits": job.benefits,
            "working_hours": job.working_hours
        }
        for job in jobs
    ]
    return jsonify({"jobs": job_list})


# API to fetch details of a particular job
@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_details(job_id):
    job = Job.query.get(job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "job": {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "stipend": job.stipend,
            "gender": job.gender,
            "accommodation": job.accommodation,
            "transport": job.transport,
            "benefits": job.benefits,
            "working_hours": job.working_hours
        }
    })


# API to apply for a job and fetch the list of applied jobs for a particular user
@app.route('/apply', methods=['POST'])
def apply_for_job():
    data = request.get_json()

    user_id = data.get('user_id')
    job_id = data.get('job_id')

    if user_id is None or job_id is None:
        return jsonify({"error": "User ID and Job ID are required"}), 400

    job = Job.query.get(job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    job_application = JobApplication(user_id=user_id, job_id=job_id)
    db.session.add(job_application)
    db.session.commit()

    return jsonify({"message": "Application successful", "user_id": user_id, "job_id": job_id})


# API to fetch applied jobs for a particular user
@app.route('/applied-jobs/<int:user_id>', methods=['GET'])
def get_applied_jobs(user_id):
    applications = JobApplication.query.filter_by(user_id=user_id).all()
    applied_jobs = [
        {
            "job_id": application.job_id,
            "title": application.job.title,
            "description": application.job.description,
            "stipend": application.job.stipend,
            "gender": application.job.gender,
            "accommodation": application.job.accommodation,
            "transport": application.job.transport,
            "benefits": application.job.benefits,
            "working_hours": application.job.working_hours
        }
        for application in applications
    ]
    return jsonify({"applied_jobs": applied_jobs})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        """
        # Dummy job data
        data_stub = [
            {
                "title": "Chef",
                "description": "Prepare and cook food in a restaurant",
                "stipend": 3000.0,
                "gender": "Male",
                "accommodation": True,
                "transport": False,
                "benefits": "Free meals",
                "working_hours": "Full-time"
            },
            {
                "title": "Server",
                "description": "Serve food and beverages to customers",
                "stipend": 2500.0,
                "gender": "Female",
                "accommodation": False,
                "transport": True,
                "benefits": "Tips",
                "working_hours": "Part-time"
            },
            # Add more job details as needed
        ]

        for data in data_stub:
            job = Job(
                title=data["title"],
                description=data["description"],
                stipend=data["stipend"],
                gender=data["gender"],
                accommodation=data["accommodation"],
                transport=data["transport"],
                benefits=data["benefits"],
                working_hours=data["working_hours"]
            )
            db.session.add(job)

        db.session.commit()"""

    app.run(debug=True)
