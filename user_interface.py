class PatientSystem:
    # Manages patient registration, login and visit guidance.

    def __init__(self, data, appointments, recommendations):
        self.data = data
        self.appointments = appointments
        self.recommendations = recommendations

    def register(self):
        name = input('Your name: ').strip()

        if name == '':
            print('Please enter your name.')
            return None

        patient_id = 100

        for patient in self.data.patients:
            if patient['id'] >= patient_id:
                patient_id = patient['id'] + 1

        patient = {
            'id': patient_id,
            'name': name
        }

        self.data.patients.append(patient)

        if self.data.save_patients():
            print('Registration successful.')
            print('Patient ID:', patient_id)
            return patient_id

        self.data.patients.remove(patient)
        print('Registration could not be saved.')
        return None

    def login(self):
        try:
            patient_id = int(input('Patient ID: '))
        except ValueError:
            print('Invalid patient ID.')
            return None

        patient = self.data.find_record(self.data.patients, patient_id)

        if patient is None:
            print('Patient not found.')
            return None

        print('Welcome back,', patient['name'])
        return patient_id

    def first_visit(self):
        print('\nFirst Visit Guide')
        print('1. Choose a department and book a doctor.')
        print('2. Check your building, floor and room.')
        print('3. Check in at reception before your visit.')
        print('4. Follow your doctor\'s instructions after the visit.')

    def follow_up(self, patient_id):
        bookings = self.appointments.patient_bookings(patient_id)
        previous_doctor_id = None

        for booking in bookings:
            if booking['status'] == 4:
                previous_doctor_id = booking['doctor_id']

        if previous_doctor_id is None:
            print('No previous completed visits.')
            return

        doctor = self.data.find_record(self.data.doctors, previous_doctor_id)

        if doctor is None:
            print('Previous doctor not found.')
            return

        print('\nPrevious doctor:', doctor['name'])

        team = self.data.find_record(self.data.teams, doctor['team_id'])

        if team is not None:
            print('Medical team:', team['name'])

        self.recommendations.recommend_team_doctors(
            doctor['team_id'], patient_id
        )
