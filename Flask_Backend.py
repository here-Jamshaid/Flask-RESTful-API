from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6999@localhost/Backend_Jobs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()
    
    if not Job.query.first():
        sample_jobs = [
            Job(title='Software Engineer', company='Google', location='California', description='Develop and maintain software.'),
            Job(title='Data Scientist', company='Facebook', location='New York', description='Analyze and process data.'),
            Job(title='Backend Developer', company='Amazon', location='Seattle', description='Work on backend APIs.'),
            Job(title='Frontend Developer', company='Netflix', location='Los Angeles', description='Develop user interfaces.'),
            Job(title='DevOps Engineer', company='Microsoft', location='Redmond', description='Manage cloud infrastructure.'),
            Job(title='Cybersecurity Analyst', company='IBM', location='Texas', description='Ensure system security.'),
            Job(title='Machine Learning Engineer', company='Tesla', location='Palo Alto', description='Build AI models for automation.'),
            Job(title='Product Manager', company='Apple', location='San Francisco', description='Manage product lifecycles.'),
            Job(title='Database Administrator', company='Oracle', location='Austin', description='Maintain database performance.'),
            Job(title='QA Engineer', company='Adobe', location='San Jose', description='Test software quality.')
        ]
        db.session.bulk_save_objects(sample_jobs)
        db.session.commit()

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    job_list = [{"id": job.id, "title": job.title, "company": job.company, "location": job.location, "description": job.description} for job in jobs]
    return jsonify(job_list)

@app.route('/jobs', methods=['POST'])
def add_job():
    data = request.json
    new_job = Job(title=data['title'], company=data['company'], location=data['location'], description=data['description'])
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"message": "Job added successfully!"})

@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
