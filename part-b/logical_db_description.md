# Normalization Process
This section explains the normalization process applied to the Clinic Appointment System. The primary key and functional dependencies were applied to all relations derived from the ER diagram to evaluate whether the relation satisfies the requirements of First, Second, and Third Normal Forms.


The normalization process includes the following:
- Identifying each relation and its attributes.
- Identifying the primary key for each relation.
- Specifying the functional dependencies based on real-world assumptions of the domain.
- Verifying which form the relation identifies with (First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF)).
- Determine whether decomposition is required.


## Analysis of Each Relation

### Patient
(PatientID (Primary Key), FirstName, LastName, DateOfBirth, Gender, Phone, Email, AddressDetails)
Functional Dependency:
- PatientID -> FirstName, LastName, DateOfBirth, Gender, Phone, Email, AddressDetails

Normalization:
- All attributes contain atomic values (1NF).
- Address information is being treated as an atomic attribute for the normalization process since it is not further decomposed in the logical design
- PatientID is a single-attribute primary key. Therefore, no partial dependencies exist (2NF).
- No non-key attribute depends on another non-key attribute (3NF).

Result: The Patient relation is in Third Normal Form (3NF).


### Provider
(ProviderID (Primary Key), FirstName, LastName, Phone, Email)
Functional Dependency:
- ProviderID -> FirstName, LastName, Phone, Email

Normalization:
- The relation satisfies 1NF as all attributes are atomic.
- The primary key is not composite, so 2NF is satisfied.
- All non-key attributes depend only on ProviderID, therefore, it is 3NF.

Result: Provider is in Third Normal Form (3NF).


### Clinic
(ClinicID (Primary Key), ClinicName, Location, ContactNumber)
Functional Dependency:
- ClinicID -> ClinicName, Location, ContactNumber

Normalization:
- Attributes are atomic (1NF).
- There are no partial dependencies exist (2NF).
- No transitive dependencies exist (3NF).

Result: Clinic is in Third Normal Form (3NF).


### Appointment
AppointmentID (Primary Key), AppointmentDate, StartTime, EndTime, Status, PatientID, ProviderID, ClinicID
Functional Dependency:
- AppointmentID -> AppointmentDate, StartTime, EndTime, Status, PatientID, ProviderID, ClinicID

Normalization:
- All attributes are atomic (1NF).
- The primary key is a single attribute, which satisfies 2NF.
- All non-key attributes depend only on AppointmentID, with no transitive dependencies (3NF).
Result: Appointment is in Third Normal Form (3NF).


### AppointmentNote
NoteID (Primary Key), NoteContent, CreatedDate, AppointmentID)
Functional Dependency:
- NoteID -> NoteContent, CreatedDate, AppointmentID

Normalization:
- Attributes are atomic (1NF).
- Single-attribute primary key, therefore 2NF.
- No transitive dependencies are present (3NF).

Result: AppointmentNote is in Third Normal Form (3NF).


### MedicalLicense
LicenseID (Primary Key), LicenseNumber, IssueDate, ExpiryDate, ProviderID)
Functional Dependency:
- LicenseID -> LicenseNumber, IssueDate, ExpiryDate, ProviderID

Normalization:
- All values are atomic (1NF).
- Single-attribute primary key satisfies 2NF.
- All attributes depend on the LicenseID (3NF).

Result: MedicalLicense is in Third Normal Form (3NF).


### Specialty
SpecialtyID (Primary Key), SpecialtyName)
Functional Dependency:
- SpecialtyID -> SpecialtyName

Normalization:
- The relation satisfies 1NF, 2NF, and 3NF.

Result: Specialty is in Third Normal Form (3NF).


### ProviderSpecialty
ProviderID (Primary Key), SpecialtyID
Functional Dependency:
- (ProviderID, SpecialtyID) -> none

Normalization:
- This associative relation resolves a many-to-many relationship.
- The composite primary key ensures uniqueness.
- No attributes exist since the relation link two entities

Result: Any table that consists only of foreign keys forming a composite primary key is automatically in 3NF. Therefore, ProviderSpecialty is in Third Normal Form (3NF).

All relations derived from the ER diagram were evaluated against normalization process. Each relation satisfied the requirements of First, Second, and Third Normal Forms. No partial or transitive dependencies were identified. As a result, no decomposition was required. The resulting schema is suitable for implementation.

