from sqlalchemy.orm import Session
from models import Profile
from sqlalchemy.exc import SQLAlchemyError

def get_by_name(db: Session, name: str):
    return db.query(Profile).filter(Profile.name == name).first()

def get_by_id(db: Session, id: str):
    return db.query(Profile).filter(Profile.id == id).first()

def get_all(db: Session, gender=None, country_id=None, age_group=None):
    q = db.query(Profile)
    if gender:
        q = q.filter(Profile.gender == gender.lower())
    if country_id:
        q = q.filter(Profile.country_id == country_id.upper())
    if age_group:
        q = q.filter(Profile.age_group == age_group.lower())
    return q.all()

def create(db: Session, profile: Profile):
    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    except SQLAlchemyError:
        db.rollback()
        raise

def delete(db: Session, profile: Profile):
    try:
        db.delete(profile)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


# from sqlalchemy.orm import Session
# from models import Profile

# def get_by_name(db: Session, name: str):
#     return db.query(Profile).filter(Profile.name == name).first()

# def get_by_id(db: Session, id: str):
#     return db.query(Profile).filter(Profile.id == id).first()

# def get_all(db: Session, gender=None, country_id=None, age_group=None):
#     q = db.query(Profile)
#     if gender:
#         q = q.filter(Profile.gender == gender.lower())
#     if country_id:
#         q = q.filter(Profile.country_id == country_id.upper())
#     if age_group:
#         q = q.filter(Profile.age_group == age_group.lower())
#     return q.all()

# def create(db: Session, profile: Profile):
#     db.add(profile)
#     db.commit()
#     db.refresh(profile)
#     return profile

# def delete(db: Session, profile: Profile):
#     db.delete(profile)
#     db.commit()