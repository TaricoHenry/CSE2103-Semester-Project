-- CareConnect database schema
-- I chose to implement this schema using Maria DB as it open source and easily deployable and scalable acros any OS and computing environemt


-- Dropping the database if it already exists. Then creating a fresh instance of the database.
DROP DATABASE IF EXISTS careconnect;
CREATE DATABASE careconnect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE careconnect;


-- ### Main tables for the database ###

-- patient table (Defines an individual receiving care)
CREATE TABLE patient (
  patient_id      INT AUTO_INCREMENT PRIMARY KEY,
  first_name      VARCHAR(50) NOT NULL,
  last_name       VARCHAR(50) NOT NULL,
  date_of_birth   DATE NOT NULL,
  sex             ENUM('male','female','other','unknown') NOT NULL DEFAULT 'unknown', -- sometimes a patients sex may not be collected due for various reasons
  phone           VARCHAR(30),
  email           VARCHAR(254) NOT NULL, -- email addresses are mandatory as they are unique
  lot_number      VARCHAR(20),
  street_name     VARCHAR(100),
  village         VARCHAR(100),
  city            VARCHAR(100),
  region_number   VARCHAR(20),
  CONSTRAINT uq_patient_email UNIQUE (email)
);

-- provider table (Defines the doctors and other medical professionals delivering care.)
CREATE TABLE medical_provider (
  provider_id     INT AUTO_INCREMENT PRIMARY KEY,
  first_name      VARCHAR(50) NOT NULL,
  last_name       VARCHAR(50) NOT NULL,
  phone           VARCHAR(30),
  email           VARCHAR(254) NOT NULL, -- email addresses are mandatory as they are unique
  CONSTRAINT uq_provider_email UNIQUE (email)
);

-- clinic table (Defines the physical facilities where appointments are conducted.)
CREATE TABLE clinic (
  clinic_id       INT AUTO_INCREMENT PRIMARY KEY,
  clinic_name     VARCHAR(120) NOT NULL,

  -- a clinic can be "open" as in functional and operating normally, it can be "closed" as in permanently shut down and it can be in status "renovation" indicating it is temporarily closed for rennovation 
  status          ENUM('open','closed','renovation') NOT NULL DEFAULT 'open', 
  lot_number      VARCHAR(20),
  street_name     VARCHAR(100),
  village         VARCHAR(100),
  city            VARCHAR(100),
  region_number   VARCHAR(20)
);

-- specialty table (Defines the specialty of a particular medical provider.)
CREATE TABLE specialty (
  specialty_id          INT AUTO_INCREMENT PRIMARY KEY,
  specialty_name        VARCHAR(120) NOT NULL, -- specialty name is mandatory as it is unique
  specialty_description VARCHAR(255),
  CONSTRAINT uq_specialty_name UNIQUE (specialty_name)
);

-- associative entity table (Defines an associative entity that allows the many-to-many relationship between providers and specialties.)
CREATE TABLE provider_specialty (
  provider_id    INT NOT NULL,
  specialty_id   INT NOT NULL,
  PRIMARY KEY (provider_id, specialty_id),
  CONSTRAINT fk_ps_provider
    FOREIGN KEY (provider_id) REFERENCES medical_provider(provider_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_ps_specialty
    FOREIGN KEY (specialty_id) REFERENCES specialty(specialty_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

-- medical license table  (Special entity used to track a medical provider's license status (active, expired, revoked))
CREATE TABLE medical_license (
  license_id     INT AUTO_INCREMENT PRIMARY KEY,
  provider_id    INT NOT NULL,
  issue_date     DATE NOT NULL,

  -- expiry_date is a derived attribute because a medical license expires exactly 1 year after issue
  expiry_date    DATE GENERATED ALWAYS AS (DATE_ADD(issue_date, INTERVAL 1 YEAR)) VIRTUAL,

  -- a particular medical license can be in one of three statuses "active", "expired" or "revoked" by the medical board
  status         ENUM('active','expired','revoked') NOT NULL DEFAULT 'active',

  -- In order to enforce only one active license per provider a simple solution is to use a generated flag.
  -- UNIQUE allows multiple NULLs, so only one row with active_license_flag=1 is permitted.
  active_license_flag TINYINT
    GENERATED ALWAYS AS (CASE WHEN status='active' THEN 1 ELSE NULL END) VIRTUAL,

  CONSTRAINT fk_license_provider
    FOREIGN KEY (provider_id) REFERENCES medical_provider(provider_id)
    ON UPDATE CASCADE ON DELETE CASCADE,

  CONSTRAINT uq_one_active_license_per_provider UNIQUE (provider_id, active_license_flag)
);



-- ### Transactional tables in the sense that these are the main tables that records are added to during transactions with the DB ###

-- appointment table (Defines a time blocked slot scheduled for interactions between patients and providers at a clinic.)
CREATE TABLE appointment (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id     INT NOT NULL,
  provider_id    INT NOT NULL,
  clinic_id      INT NOT NULL,
  start_datetime DATETIME NOT NULL,
  end_datetime   DATETIME NOT NULL,
  status         ENUM('scheduled','completed','cancelled','no_show') NOT NULL DEFAULT 'scheduled',
  reason         VARCHAR(255),
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_appt_patient
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_appt_provider
    FOREIGN KEY (provider_id) REFERENCES medical_provider(provider_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  CONSTRAINT fk_appt_clinic
    FOREIGN KEY (clinic_id) REFERENCES clinic(clinic_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,

  -- We neeed to prevent a medical provider from double booking we add a constraint
  CONSTRAINT uq_provider_start UNIQUE (provider_id, start_datetime),

  -- We can do the same from the patient side
  CONSTRAINT uq_patient_start UNIQUE (patient_id, start_datetime),

  CONSTRAINT ck_appt_times CHECK (end_datetime > start_datetime)
);


-- appointment_note table (Special entity used to capture notes by a medical provider or outcomes of an appointment.)
CREATE TABLE appointment_note (
  note_id            INT AUTO_INCREMENT PRIMARY KEY,
  appointment_id     INT NOT NULL,
  author_provider_id INT NULL,
  note_text          TEXT NOT NULL,
  created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_note_appt
    FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id)
    ON UPDATE CASCADE ON DELETE CASCADE,

  CONSTRAINT fk_note_author
    FOREIGN KEY (author_provider_id) REFERENCES medical_provider(provider_id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating indexes for reporting for the application
CREATE INDEX idx_appt_provider_time ON appointment(provider_id, start_datetime);
CREATE INDEX idx_appt_clinic_time   ON appointment(clinic_id, start_datetime);
CREATE INDEX idx_appt_status_time   ON appointment(status, start_datetime);
