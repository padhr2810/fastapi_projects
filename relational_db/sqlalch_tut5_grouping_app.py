
from sqlalch_tut5_grouping_models import Patient, engine
from sqlalchemy import and_, func, not_, or_
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# If there is data in the database, dont add more data
if session.query(Patient).count() < 1:
    session.add(Patient(patient_name="Iron Man", patient_age=23))
    session.add(Patient(patient_name="Coding Man", patient_age=33))
    session.add(Patient(patient_name="Banana Man", patient_age=78))
    session.add(Patient(patient_name="Zeq", patient_age=99))

    session.commit()


# ========================================================================================
print("\nGROUP BY (AGE,)")
users_count_by_age = (
    session.query(Patient.patient_age).group_by(Patient.patient_age).all()
)
print(users_count_by_age)

# ========================================================================================
print("\nGROUP BY ADDITIONAL CRITERIA (AGE, COUNT)")
# count the number of users by age
users_count_by_age = session.query(Patient.patient_age, func.count(Patient.patient_id)).group_by(Patient.patient_age).all()
print(users_count_by_age)

# ========================================================================================
print("\nCHAINING METHODS")
users = (
    session.query(Patient).filter(Patient.patient_age > 24).filter(Patient.patient_age < 50).all()
)

for user in users:
    print(f"{user.patient_age = }")

# or like this
users_tuple = (
    session.query(Patient.patient_age, func.count(Patient.patient_id))
    .filter(Patient.patient_age > 24)
    .order_by(Patient.patient_age)
    .filter(Patient.patient_age < 50)
    .group_by(Patient.patient_age)
    .all()
)
for age, count in users_tuple :
    print(f"Age: {age} - Patients: {count}")


# ========================================================================================
print("\nDELAY .all()")
only_iron_man = True
group_by_age = True

users = session.query(Patient)
if only_iron_man:
    users = users.filter(Patient.patient_name == "Iron Man")
if group_by_age:
    users = users.group_by(Patient.patient_age)
users = users.all()
for user in users:
    print(f"Patient age: {user.patient_age}, name: {user.patient_name}")
    
    
