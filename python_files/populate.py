#!/usr/bin/env python3
"""
CareConnect - Data generator

This script was built in python and intended to be run on m series macs. Everything should also work well on linux.
There is no garantee that this script will run 100% without errors in a windows environment.


The goal of this script is to generate bulk SQL INSERT statements for the CareConnect Database.

Output file:
  - careconnect_data.sql


Env vars can be used or set explicity in the script: 
  CARECONNECT_SEED=2102
  CARECONNECT_NUM_PATIENTS=3000
  CARECONNECT_NUM_PROVIDERS=200
  CARECONNECT_NUM_APPOINTMENTS=8000
"""

# Import Faker library so we can generate nice looking realish data
from faker import Faker

# Import OS for env vars, random and datetime for date/time fields
import os, random, datetime



# Basic Configuration
# Setting a seed so we can garantee the same thing each run
SEED = int(os.getenv("CARECONNECT_SEED", "2102"))

# Setting default values for env vars
NUM_PATIENTS = int(os.getenv("CARECONNECT_NUM_PATIENTS", "30000"))
NUM_PROVIDERS = int(os.getenv("CARECONNECT_NUM_PROVIDERS", "2000"))
NUM_APPOINTMENTS = int(os.getenv("CARECONNECT_NUM_APPOINTMENTS", "80000"))

# Create a faker instance and just seed it
fake = Faker()
Faker.seed(SEED)

# seed python's default random function so the "randomness" is repeatable
random.seed(SEED)



# Some Helper functions
def sql_escape(s: str) -> str:
    # SQL is weird so we need to be able escape backslashes and single quotes for SQL string insertion
    return s.replace("\\", "\\\\").replace("'", "''")

def gen_email(first: str, last: str, domain: str) -> str:
    #generate a unique-ish email address, append a random number to reduce collision risk
    base = f"{first}.{last}".lower().replace("'", "").replace(" ", "")
    return f"{base}{random.randint(1, 999999)}@{domain}"  

def rand_region() -> str:
    # Setting up the region numbers
    return str(random.choice([1,2,3,4,5,6,7,8,9,10]))

def gen_guyana_phone() -> str:
    # Setting up the phone number pattern
    return "5926" + "".join(str(random.randint(0, 9)) for _ in range(6))

def pick_timeslot(base_dt: datetime.datetime) -> datetime.datetime:
    # Create the appointment start time for a day within regular working hours, 30 min intervals

    #Set working hours
    hour = random.choice([8, 9, 10, 11, 13, 14, 15, 16])

    # Set up intervals
    minute = random.choice([0, 30])

    # Apply hour/minute to base datetime
    return base_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)


# Set up reference data for DB

# Defining Specialties
specialties = [
    ("Family Medicine","Primary care and general practice."),
    ("Pediatrics","Healthcare for infants, children, and adolescents."),
    ("Cardiology","Heart and vascular system."),
    ("Dermatology","Skin, hair, and nail conditions."),
    ("Orthopedics","Musculoskeletal system and injuries."),
    ("Obstetrics & Gynecology","Pregnancy and women's health."),
    ("Internal Medicine","Adult medicine and complex conditions."),
    ("Psychiatry","Mental health and behavioral disorders.")
]

# Defining the clinics
clinic_names = [
    "Georgetown Public Hospital",
    "New Amsterdam Regional Hospital",
    "Linden Hospital Complex",
    "Suddie Regional Hospital",
    "West Demerara Regional Hospital",
    "Skeldon Public Hospital"
]

# Just setting some reasons for appointments
reasons = [
    "Routine check-up", "Follow-up visit", "Lab results review",
    "Medication refill", "New symptoms evaluation", "Pre-op consultation",
    "Vaccination", "Prenatal visit", "Dermatology consult", "Cardiac screening"
]


# Actual script to do the generation of the data

def main():
   
   # We need to generate clinics first as appointments reference these
    clinics = [] 
    for name in clinic_names:
        clinics.append({
            "clinic_name": name,
            "status": random.choice(["open", "open", "open", "renovation"]),  # creating more open clinics 
            "lot_number": str(random.randint(1, 200)),
            "street_name": fake.street_name(),
            "village": fake.city_suffix(),
            "city": random.choice(["Georgetown", "Linden", "New Amsterdam", "Anna Regina"]),
            "region_number": rand_region()
        })


    # create specialties
    spec_rows = [] 
    for n, d in specialties:
        spec_rows.append({
            "specialty_name": n,
            "specialty_description": d
        })

    # create medical providers
    providers = []
    for _ in range(NUM_PROVIDERS):
        fn = fake.first_name()  # provider first name
        ln = fake.last_name()   # provider last name
        providers.append({
            "first_name": fn,
            "last_name": ln,
            "phone": gen_guyana_phone(),  # Guyana phone format required
            "email": gen_email(fn, ln, "careconnect.gy")  # unique-ish email
        })

    #create patients
    patients = []
    for _ in range(NUM_PATIENTS):
        fn = fake.first_name()  # patient first name
        ln = fake.last_name()   # patient last name
        dob = fake.date_of_birth(minimum_age=0, maximum_age=90)  # date_of_birth
        patients.append({
            "first_name": fn,
            "last_name": ln,
            "date_of_birth": dob.isoformat(),  # stored as YYYY-MM-DD
            "sex": random.choice(["male", "female", "other", "unknown"]),  # matches ENUM
            "phone": gen_guyana_phone(),
            "email": gen_email(fn, ln, "patientmail.gy"),  # unique-ish email
            "lot_number": str(random.randint(1, 300)),
            "street_name": fake.street_name(),
            "village": fake.city_suffix(),
            "city": random.choice(["Georgetown", "Linden", "New Amsterdam", "Anna Regina"]),
            "region_number": rand_region()
        })

   
    # create provider_specialty (associative table)
    provider_specs = set()  # use set to avoid duplicates
    for provider_id in range(1, len(providers) + 1): 
        k = random.randint(1, 3)  # each provider gets 1-3 specialties
        for specialty_id in random.sample(range(1, len(spec_rows) + 1), k):
            provider_specs.add((provider_id, specialty_id))


    # set up licenses
    today = datetime.date.today()
    licenses = []
    for provider_id in range(1, len(providers) + 1):
        # random issue date in the past
        issue_date = today - datetime.timedelta(days=random.randint(30, 500))
        status = "active"  # default active

        # 25% expiry rate
        if random.random() < 0.25:
            issue_date = today - datetime.timedelta(days=random.randint(400, 900))
            status = "expired"

        licenses.append({
            "provider_id": provider_id,
            "issue_date": issue_date.isoformat(),
            "status": status
        })

    # set up appointments use sets to track pairs to ensure uniqueness
    start_base = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    used_provider_slots = set()  # tracks (provider_id, start_datetime_str)
    used_patient_slots = set()   # tracks (patient_id, start_datetime_str)

    appts = []
    attempts = 0  # guard against infinite loops
    max_attempts = NUM_APPOINTMENTS * 20  # safety limit

    while len(appts) < NUM_APPOINTMENTS and attempts < max_attempts:
        attempts += 1 

        # Choose existing FK values
        patient_id = random.randint(1, len(patients))
        provider_id = random.randint(1, len(providers))
        clinic_id = random.randint(1, len(clinics))

        day_offset = random.randint(-120, 60)
        day_dt = (start_base + datetime.timedelta(days=day_offset)).replace(hour=0, minute=0)

        # Pick a valid timeslot within the work day
        start_dt = pick_timeslot(day_dt)

        # convert to date time format
        start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")

        # prevent double booking
        if (provider_id, start_str) in used_provider_slots:
            continue 
        if (patient_id, start_str) in used_patient_slots:
            continue 

        # set appt length
        end_dt = start_dt + datetime.timedelta(minutes=random.choice([30, 60]))

        # set the statuses
        status = random.choices(
            ["scheduled", "completed", "cancelled", "no_show"],
            weights=[35, 45, 10, 10],
            k=1
        )[0]

        # Future appointments should not be completed/no_show
        if start_dt > datetime.datetime.now():
            status = random.choices(["scheduled", "cancelled"], weights=[85, 15], k=1)[0]

        # Store appointment record
        appts.append({
            "patient_id": patient_id,
            "provider_id": provider_id,
            "clinic_id": clinic_id,
            "start": start_dt,
            "end": end_dt,
            "status": status,
            "reason": random.choice(reasons)
        })

        # Mark slot as used
        used_provider_slots.add((provider_id, start_str))
        used_patient_slots.add((patient_id, start_str))

    # If we hit the safety limit just fail so we can see errors
    if len(appts) < NUM_APPOINTMENTS:
        raise RuntimeError(
            f"Could only generate {len(appts)} appointments out of {NUM_APPOINTMENTS} "
            f"without violating unique constraints. Increase max_attempts or widen time range."
        )

    # set up appointment notes
    notes = []
    for appointment_id, appt in enumerate(appts, start=1): 
        if appt["status"] == "completed" and random.random() < 0.55:
            for _ in range(random.randint(1, 2)):
                notes.append({
                    "appointment_id": appointment_id,
                    "author_provider_id": appt["provider_id"],
                    "note_text": random.choice([
                        "Patient assessed; vitals stable. Advised follow-up in 2 weeks.",
                        "Discussed symptoms and treatment plan. Prescribed medication.",
                        "Reviewed labs; no critical findings. Lifestyle advice provided.",
                        "Condition improving. Continue current regimen and monitor."
                    ])
                })

    #build the sql statements order is important here otherwise script breaks
    out = []

    # Insert clinics first
    out.append("-- Populate clinics")
    for c in clinics:
        out.append(
            "INSERT INTO clinic (clinic_name,status,lot_number,street_name,village,city,region_number) VALUES "
            f"('{sql_escape(c['clinic_name'])}','{c['status']}','{sql_escape(c['lot_number'])}','{sql_escape(c['street_name'])}',"
            f"'{sql_escape(c['village'])}','{sql_escape(c['city'])}','{sql_escape(c['region_number'])}');"
        )

    # Insert specialties
    out.append("\n-- Populate specialties")
    for s in spec_rows:
        out.append(
            "INSERT INTO specialty (specialty_name,specialty_description) VALUES "
            f"('{sql_escape(s['specialty_name'])}','{sql_escape(s['specialty_description'])}');"
        )

    # Insert providers (provider_specialty, medical_license, appointment_note reference providers)
    out.append("\n-- Populate medical providers")
    for p in providers:
        out.append(
            "INSERT INTO medical_provider (first_name,last_name,phone,email) VALUES "
            f"('{sql_escape(p['first_name'])}','{sql_escape(p['last_name'])}','{sql_escape(p['phone'])}','{sql_escape(p['email'])}');"
        )

    # Insert patients (appointments reference patients)
    out.append("\n-- Populate patients")
    for p in patients:
        out.append(
            "INSERT INTO patient (first_name,last_name,date_of_birth,sex,phone,email,lot_number,street_name,village,city,region_number) VALUES "
            f"('{sql_escape(p['first_name'])}','{sql_escape(p['last_name'])}','{p['date_of_birth']}','{p['sex']}','{sql_escape(p['phone'])}',"
            f"'{sql_escape(p['email'])}','{sql_escape(p['lot_number'])}','{sql_escape(p['street_name'])}','{sql_escape(p['village'])}',"
            f"'{sql_escape(p['city'])}','{sql_escape(p['region_number'])}');"
        )

    # Insert provider_specialty 
    out.append("\n-- Populate provider_specialty")
    for provider_id, specialty_id in sorted(provider_specs):
        out.append(f"INSERT INTO provider_specialty (provider_id,specialty_id) VALUES ({provider_id},{specialty_id});")

    # Insert medical licenses (provider_id should exist)
    out.append("\n-- Populate medical_license")
    for lic in licenses:
        out.append(
            "INSERT INTO medical_license (provider_id, issue_date, status) VALUES "
            f"({lic['provider_id']}, '{lic['issue_date']}', '{lic['status']}');"
        )

    # Insert appointments (patient_id/provider_id/clinic_id must already exist)
    out.append("\n-- Populate appointments")
    for appt in appts:
        out.append(
            "INSERT INTO appointment (patient_id,provider_id,clinic_id,start_datetime,end_datetime,status,reason) VALUES "
            f"({appt['patient_id']},{appt['provider_id']},{appt['clinic_id']},"
            f"'{appt['start'].strftime('%Y-%m-%d %H:%M:%S')}','{appt['end'].strftime('%Y-%m-%d %H:%M:%S')}',"
            f"'{appt['status']}','{sql_escape(appt['reason'])}');"
        )

    # Insert appointment notes last
    out.append("\n-- Populate appointment notes")
    for n in notes:
        out.append(
            "INSERT INTO appointment_note (appointment_id, author_provider_id, note_text) VALUES "
            f"({n['appointment_id']},{n['author_provider_id']},'{sql_escape(n['note_text'])}');"
        )

    # Write final SQL file
    with open("careconnect_data.sql", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    # Print success message so we know all is well
    print("Wrote careconnect_data.sql")
    print(f"Counts: patients={len(patients)}, providers={len(providers)}, appointments={len(appts)}, notes={len(notes)}")

# Start the program at main
if __name__ == "__main__":
    main()
