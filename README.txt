MEDIFLOW - HOSPITAL APPOINTMENT AND NAVIGATION SYSTEM

1. PROJECT OVERVIEW

MediFlow is a Python-based hospital appointment and navigation
system designed to help patients manage their hospital visits.

The system supports patient registration, appointment booking,
medical team recommendations, clinic navigation and follow-up visits.

It aims to make the hospital experience easier for patients,
especially those attending the hospital for the first time.


2. MAIN FEATURES

- New patient registration
- Returning patient login
- Department and doctor selection
- Appointment booking and cancellation
- Appointment capacity and time conflict checking
- Doctor recommendations based on consultation fees
- Medical team information
- First-visit guidance
- Hospital navigation and clinic location search
- Follow-up recommendations
- Appointment completion demonstration


3. PROJECT STRUCTURE

main.py
    MediFlow class
    Controls the main program and menus.

data_manager.py
    DataManager class
    Loads, stores and searches hospital data.

user_interface.py
    PatientSystem class
    Manages patient registration, login and visit guidance.

actions/appointment.py
    AppointmentSystem class
    Manages booking rules, appointment records and visit status.

recommendation.py
    RecommendationSystem class
    Handles department selection and doctor recommendations.

navigation.py
    NavigationSystem class
    Provides hospital directions and department navigation.

test_mediflow.py
    MediFlowTests class
    Tests core system functions.


4. DATA FILES

The hospital_data folder contains:

patients.json
appointments.json
doctors.json
departments.json
teams.json
schedules.json

These files provide the information used by the system.


5. ADVANCED PYTHON CONCEPTS

File Input/Output:
The DataManager class loads and saves JSON files.
Patient and appointment information is stored between program runs.

Error Handling:
Try-except blocks handle invalid user input and file errors.
The program provides error messages instead of stopping unexpectedly.

Recursion:
The NavigationSystem class uses recursion to find the hierarchy
of hospital departments.

Classes and Objects:
The system uses separate classes to organise related functions
and manage shared data.


6. HOW TO RUN

Open a terminal in the MediFlow folder.

Run the main program:

python3 main.py

To run the tests:

python3 test_mediflow.py


7. SAMPLE PATIENTS

Patient ID: 100
Name: Tom

Patient ID: 101
Name: Alice

Patient ID: 102
Name: Jack

New patients can also register through the main menu.


8. IMPORTANT NOTES

This project is a simulation for educational purposes.

The medical information, doctors, fees and clinic locations
are fictional.

The Complete Visit option is included for demonstration.

Appointment availability depends on the dates stored in
schedules.json.


9. TESTING

The test program checks:

- Data loading
- Record searching
- Department selection
- Doctor sorting
- Appointment capacity
- Appointment conflicts
- Recursive department paths

Tests are written using Python assert statements.
