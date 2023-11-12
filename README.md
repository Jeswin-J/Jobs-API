
# Job API

This is a simple Flask application that provides an API for managing job details and applications. The application uses SQLite as its database and SQLAlchemy as the ORM.


## Prerequisites

Make sure you have Python and Flask installed on your machine. You can install Flask using the following command:

```
pip install Flask

```
## Setup

#### 1. Clone the repository to your local machine.

```
git clone https://github.com/Jeswin-J/Jobs-API.git
cd Jobs-API

```

#### 2. Install the required dependencies.

```
pip install -r requirements.txt

```

#### 3. Run the application.

```
python job_api.py

```

The application will start, and you should see output indicating that the Flask development server is running.
## API Reference

#### Get all jobs

```http
  GET /jobs
```

| Parameter | Description                |
| :-------- |:------------------------- |
| `none`    | Retrieve details of all jobs. |

#### Get job details

```http
  GET /jobs/${job_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `job_id`      | `integer` | **Required**. Id of item to fetch |

#### Get Applied Job

```http
  GET /applied-jobs/${user_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`      | `integer` | **Required**. ID of the user to fetch applied jobs for. |

#### Apply for a job

```http
  POST /apply
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`      | `integer` | **Required**.  ID of the user applying for the job. |
| `job_id`      | `integer` | **Required**.  ID of the job to apply for. |


## Database Initialization

The application includes a commented-out section to initialize the database with dummy job data. Uncomment and customize this section to add initial job data.

``` 
# Uncomment the following lines to initialize the database with dummy job data
"""
with app.app_context():
    db.create_all()

    data_stub = [
        {
            "title": "Chef",
            "description": "Prepare and cook food in a restaurant",
            # Add more job details as needed
        },
        # Add more job details as needed
    ]

    for data in data_stub:
        job = Job(
            title=data["title"],
            description=data["description"],
            # Add more job details as needed
        )
        db.session.add(job)

    db.session.commit()
"""
```
This will create the database tables and populate them with sample job data.

**Note:** Make sure to comment out or remove this section after the initial setup to avoid re-creating the same dummy data each time the application is run.
