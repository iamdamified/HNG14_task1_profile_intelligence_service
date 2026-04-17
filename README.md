# Profile Intelligence API

A production-ready **FastAPI** service that generates demographic profile insights (gender, age group, and nationality) from a given name using trusted public APIs.  
Built for **HNG Internship (Backend Track)** and deployed on **Vercel** with **Neon PostgreSQL**.

---

## Live API

**Base URL**


https://profile-intelligence-ruby.vercel.app/


---

## Features

-  Infers **gender**, **age**, and **country** from a name
-  Computes **age group** classification
-  Idempotent profile creation (no duplicate names)
-  Persistent storage with **PostgreSQL (Neon)**
-  All timestamps in **UTC ISO 8601**
-  FastAPI with async HTTP requests
-  Production deployment on **Vercel**

---

## Tech Stack

| Layer        | Technology |
|-------------|------------|
| Framework   | FastAPI |
| Database    | PostgreSQL (Neon) |
| ORM         | SQLAlchemy |
| HTTP Client | httpx |
| Deployment  | Vercel |
| Python      | 3.10+ |

---

## Project Structure


profile_intelligence/
│

├── main.py # FastAPI app & routes

├── models.py # SQLAlchemy models

├── database.py # Database engine & session

├── crud.py # Database operations

├── utils.py # UUID, UTC timestamps, helpers

├── requirements.txt # Python dependencies

├── vercel.json # Vercel configuration

├── .env # Environment variable template

├── .gitignore # Environment variable template

└── README.md


---

## Environment Variables

Create a `.env` file locally (do NOT commit it):


DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require

ENV=development


Add the same variables on **Vercel** via:


Project → Settings → Environment Variables


---

## Local Installation

### Clone the Repository


git clone https://github.com/your-username/profile_intelligence.git

cd profile_intelligence


### Create Virtual Environment


python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate


### Install Dependencies


pip install -r requirements.txt


---

## Run Locally


uvicorn main:app --reload


Access:

- Swagger Docs → http://127.0.0.1:8000/docs  
- OpenAPI Spec → http://127.0.0.1:8000/openapi.json  

---

## API Endpoints

### Create Profile

**POST** `/api/profiles`

**Request Body**
```json
{
  "name": "emmanuel"
}

Response (201 Created)

{
  "status": "success",
  "data": {
    "id": "019d9b9b-1ee2-0000-0000-762b8269747b",
    "name": "emmanuel",
    "gender": "male",
    "gender_probability": 0.99,
    "sample_size": 12345,
    "age": 32,
    "age_group": "adult",
    "country_id": "NG",
    "country_probability": 0.87,
    "created_at": "2026-04-17T14:22:10Z"
  }
}
```

## Get All Profiles

**GET** `/api/profiles`

### Optional Query Parameters
- `gender`
- `country_id`
- `age_group`

**Response (200 OK)**
```json
{
  "status": "success",
  "list of data": { ... }
}
```

---

### Get Profile

**GET** `/api/profiles/{profile_id}`

**Response (200 OK)**
```json
{
  "status": "success",
  "data": { ... }
}
```

## Delete Profile

**DELETE** `/api/profiles/{profile_id}`

**Response:**  
- `204 No Content` on successful deletion

---

## Timestamp Standard

All timestamps are:
- UTC
- ISO 8601 compliant
- Stored and returned consistently

**Example:**

2026-04-17T14:22:10Z


---

## External APIs Used

- **Gender prediction:** genderize.io  
- **Age estimation:** agify.io  
- **Nationality inference:** nationalize.io  

Graceful error handling is implemented for upstream failures.

---

## ☁️ Deployment (Vercel)

### Install Vercel CLI

npm install -g vercel


### Login

vercel login


### Deploy

vercel


### Production Deployment

vercel --prod


---

## Database (Neon PostgreSQL)

- Serverless PostgreSQL
- SSL enabled
- Compatible with Vercel
- Connected via `psycopg[binary]`

---

## Task Compliance Checklist

- ✔ FastAPI backend  
- ✔ RESTful endpoints  
- ✔ PostgreSQL persistence  
- ✔ UTC ISO 8601 timestamps  
- ✔ Deployed on Vercel  
- ✔ Clean architecture  
- ✔ Submission-ready documentation  

---

## Author

**Emmanuel Adekoya**  
HNG Internship — Backend Engineering Track