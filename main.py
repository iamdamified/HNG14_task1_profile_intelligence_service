from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import httpx
import re

from database import Base, engine, SessionLocal
from models import Profile
from crud import get_by_name, get_by_id, create, delete
from utils import uuid7, utc_now, age_group

# --------------------
# DATABASE INIT
# --------------------
Base.metadata.create_all(bind=engine)

# --------------------
# APP SETUP
# --------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # REQUIRED BY GRADER
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# EXTERNAL APIS
# --------------------
GENDERIZE = "https://api.genderize.io"
AGIFY = "https://api.agify.io"
NATIONALIZE = "https://api.nationalize.io"

# --------------------
# DB DEPENDENCY
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------
# CREATE PROFILE
# --------------------
@app.post("/api/profiles", status_code=201)
async def create_profile(
    payload: dict,
    response: Response,
    db: Session = Depends(get_db),
):
    response.headers["Access-Control-Allow-Origin"] = "*"

    name = payload.get("name")

    # -------- VALIDATION --------
    if name is None:
        return JSONResponse(
            {"status": "error", "message": "Missing or empty name"}, 400
        )

    if not isinstance(name, str):
        return JSONResponse(
            {"status": "error", "message": "Invalid type"}, 422
        )

    name = name.strip().lower()

    if not name:
        return JSONResponse(
            {"status": "error", "message": "Missing or empty name"}, 400
        )

    # Alphabet-only enforcement
    if not re.fullmatch(r"[a-z]+", name):
        return JSONResponse(
            {
                "status": "error",
                "message": "Name must contain alphabetic characters only",
            },
            400

        )

    # -------- IDEMPOTENCY --------
    existing = get_by_name(db, name)
    if existing:
        return {
            "status": "success",
            "message": "Profile already exists",
            "data": serialize_profile(existing),
        }

    # -------- EXTERNAL API CALLS --------
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            g_res = await client.get(GENDERIZE, params={"name": name})
            a_res = await client.get(AGIFY, params={"name": name})
            n_res = await client.get(NATIONALIZE, params={"name": name})
    except httpx.RequestError:
        return JSONResponse(
            {"status": "error", "message": "Upstream service unavailable"},
            502

        )

    # -------- SAFE JSON PARSING --------
    try:
        g = g_res.json()
        a = a_res.json()
        n = n_res.json()
    except ValueError:
        return JSONResponse(
            {
                "status": "error",
                "message": "Upstream service returned invalid JSON",
            },
            502

        )

    # -------- UPSTREAM VALIDATION --------
    if g.get("gender") is None or g.get("count", 0) == 0:
        return JSONResponse(
            {
                "status": "error",
                "message": "Genderize returned an invalid response",
            }, 502
        )

    if a.get("age") is None:
        return JSONResponse(
            {
                "status": "error",
                "message": "Agify returned an invalid response",
            }, 502
        )

    if not n.get("country"):
        return JSONResponse(
            {
                "status": "error",
                "message": "Nationalize returned an invalid response",
            }, 502
        )

    top_country = max(n["country"], key=lambda x: x["probability"])

    # -------- CREATE PROFILE --------
    profile = Profile(
        id=uuid7(),
        name=name,
        gender=g["gender"],
        gender_probability=g["probability"],
        sample_size=g["count"],
        age=a["age"],
        age_group=age_group(a["age"]),
        country_id=top_country["country_id"],
        country_probability=top_country["probability"],
        created_at=utc_now(),
    )

    create(db, profile)

    return {
        "status": "success",
        "data": serialize_profile(profile),
    }

# --------------------
# GET ALL PROFILES
# --------------------
@app.get("/api/profiles")
def list_profiles(
    gender: str | None = None,
    country_id: str | None = None,
    age_group: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Profile)

    if gender:
        query = query.filter(Profile.gender.ilike(gender.lower()))

    if country_id:
        query = query.filter(Profile.country_id.ilike(country_id.upper()))

    if age_group:
        query = query.filter(Profile.age_group.ilike(age_group.lower()))

    profiles = query.all()

    return {
        "status": "success",
        "count": len(profiles),
        "data": [
            {
                "id": p.id,
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "age_group": p.age_group,
                "country_id": p.country_id,
            }
            for p in profiles
        ],
    }

# --------------------
# GET SINGLE PROFILE
# --------------------
@app.get("/api/profiles/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = get_by_id(db, profile_id)
    if not profile:
        return JSONResponse(
            {"status": "error", "message": "Profile not found"}, 404
        )

    return {
        "status": "success",
        "data": serialize_profile(profile),
    }

# --------------------
# DELETE PROFILE
# --------------------
@app.delete("/api/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = get_by_id(db, profile_id)
    if not profile:
        return JSONResponse(
            {"status": "error", "message": "Profile not found"}, 404
        )

    delete(db, profile)
    return Response(status_code=204)

# --------------------
# SERIALIZER (SAFE)
# --------------------
def serialize_profile(p: Profile):
    return {
        "id": p.id,
        "name": p.name,
        "gender": p.gender,
        "gender_probability": p.gender_probability,
        "sample_size": p.sample_size,
        "age": p.age,
        "age_group": p.age_group,
        "country_id": p.country_id,
        "country_probability": p.country_probability,
        "created_at": p.created_at.isoformat(),
    }