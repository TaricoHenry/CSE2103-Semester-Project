# What is CareConnect
CareConnect is a unique custom built application that is inspired by the tried and true capabilities of Salesforce Health Cloud. As a certified and seasoned salesforce developer I have personally seen how great software helps organizations scale and improve productivity and positively impact client satisfaction.


CareConnect aims to solve the issue in Guyana where public hospitals are over-run by large numbers of patients showing up at the same time for their appointments on a given day. This usually causes over-crowded waiting rooms and greatly increases the time a patient spends waiting to see their respective doctor or medical provider. Furthermore, medical providers are usually overwhelmed as a result of the poor scheduling and subsequently they are not able to spend as much time as they would like with their respective patients.

### Why CareConnect
CareConnect is a lightweight custom solution tailored to the unique requirements of the public hospital system in Guyana. Normal Salesforce implementations usually have a three year timeline and usually go over budget making them not ideal for a country with limited spending power such as Guyana. CareConnect keeps core time-tested entities such as patients and medical providers while maintaining a lightweight, cost effective and scalable architecture.


### High level Summary
In a broad sense CareConnect aims to allow patients to schedule, review, and modify upcoming appointments. Additionally, CareConnect will allow providers (doctors and other medical staff) to manage their schedules and generate critical reports such as no-show rates, utilization and workload or capacity distribution.


### Entities
The ERD for this project describes the following entities:
- Patient – Defines an individual receiving care, this entity stores their key information such as name and contact information
- Provider – Defines the doctors and other medical professionals delivering care.
- Clinic – Defines the physical facilities where appointments are conducted.
- Appointment – Defines a time blocked slot scheduled for interactions between patients and providers at a clinic.
- Appointment_Note – Special entity used to capture notes by a medical provider or outcomes of an appoitment.
- Specialty – Defines the specialty of a particular medical provider.
- Provider_Specialty – Defines an associative entity that allows the many-to-many relationship between providers and specialties.
- Medical_License – Special entity used to track a medical provider's license status (valid, expired, suspended, etc)


### Relationships
- A patient can have many appointments, but each appointment is for one patient.
- A medical provider can be booked for many appointments, but each appointment is done by one provider.
- A specific clinic can host many appointments, but one appointment occurs at one clinic.
- A medical provider can have multiple specialties, as well as a specialty can belong to multiple providers (this is done through the use of an associative entity).
- An particular appointment can have multiple appointment notes, but each appointment note belongs to exactly one appointment.
- A medical provider can hold multiple medical licenses over time, but only one medical license may be active and valid at a time.


### Core Application functionality
The core functionality of this application is as follows:
- Register, track and maintain patient demographic and contact information.
- Register, track and maintain providers (doctors and other medical professionals) and their clinic assignment(s) and specialties.
- CRUD various appointments with different statuses (e.g., Scheduled, Completed, Cancelled, No-Show).
- Allow patients to query “my appointments” and “my assigned provider(s)”.
- Allow providers to query “my schedule” and “my patient list for a date range”.
- Track appointment notes/outcomes (lightweight “encounter note” style).

### Assumptions Made for this solution
- A patient can have many appointments. Essentially an appointment belongs to exactly one patient.
- A medical provider can have many appointments. Essentially an appointment is with exactly one provider.
- An appointment can happen only at one clinic location.
- A medical providers can have multiple specialties. Essentially many to many
- An Appointment must have a start/end time and a valid lifecycle status
- A medical provider cannot be double booked, meaning they are booked for two appointments at the same time.

### Reporting needs
A provider or clinic must be able to generate the following reports:
- Appointments per provider per week/month
- No-show rate by provider, specialty, clinic
- Top appointment reasons by specialty
- Daily clinic schedule and capacity utilization
- Patient appointment history and upcoming visits



### Architecture Summary
CareConnect architecture is a standard three tiered model based on client server interactions. 

#### Database and Back End
Maria- Db acts as the backend of the entire application and is responsible for hosting and storing all data critical to the normal functioning of the application.  

Deep-dive into the architecture can be found: https:// deep-dive


#### Middleware
In terms of middleware and ESB everything is ran through python based API's. In this way no operation is allowed to be done on the database directly by any client. This vastly improves secruity of the application and helps to centralize logging of all operations being passed through the application.

Deepdive into the middleware architecture can be found: https:deep-dive


#### Front-end
From the front end perspective, both mobile and web applications are powered by REACT Native due to its versatility and commonnesss throughout the software development industry.

deepdive into the front-end can be found: https: deep-dive




### Limitations and difficult aspects of this domain
- Given the limited nature of the application it is unable to cover the great amount of customizations that are needed for the Guyana healthcare environment. 
--> many clinics want the ability to track supply usage and tie it back t individual patients
--> clinics and hospitals also like the ability to tie CareConnect to the internal scheduling systems as in many cases the consulting doctors are also the ones that are scheduled for various surgeries and other emergency procedures due to the limited amount of specialists in Guyana.

--> these additional customizations would expand the scope of this project and exceed the guidelines outlined, i.e "domain that is relatively substantial but not enormous" and "a range of five or so entity sets, and a similar number of relationship set".


