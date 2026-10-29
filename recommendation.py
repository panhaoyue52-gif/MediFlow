class RecommendationSystem:
    # Handles department selection and doctor recommendations.

    def __init__(self, data, appointments):
        self.data = data
        self.appointments = appointments

    def get_departments(self):
        choices = []

        for department in self.data.departments:
            for doctor in self.data.doctors:
                if doctor['department_id'] == department['id']:
                    choices.append(department)
                    break

        return choices

    def choose_department(self):
        choices = self.get_departments()

        if len(choices) == 0:
            print('No departments available.')
            return 0

        print('\nChoose a Department')

        for i in range(len(choices)):
            print(i + 1, choices[i]['name'])

        try:
            choice = int(input('Choose a department (0 to return): '))
        except ValueError:
            print('Invalid choice.')
            return 0

        if choice == 0:
            return 0

        if choice < 1 or choice > len(choices):
            print('Invalid choice.')
            return 0

        return choices[choice - 1]['id']

    def show_doctors(self, department_id):
        print('\nDoctors')
        found = False

        for doctor in self.data.doctors:
            if doctor['department_id'] == department_id:
                print(doctor['name'], '-', doctor['title'], '- $', doctor['fee'])
                found = True

        if not found:
            print('No doctors found.')

    def show_team(self, team_id):
        team = self.data.find_record(self.data.teams, team_id)

        if team is None:
            print('Team not found.')
            return

        print('\nTeam:', team['name'])

        for doctor in self.data.doctors:
            if doctor['id'] in team['doctor_ids']:
                print(doctor['name'], '-', doctor['title'], '- $', doctor['fee'])

    def choose_team(self):
        print('\nMedical Teams')

        for i in range(len(self.data.teams)):
            print(i + 1, self.data.teams[i]['name'])

        try:
            choice = int(input('Choose a team (0 to return): '))
        except ValueError:
            print('Invalid choice.')
            return

        if choice == 0:
            return

        if choice < 1 or choice > len(self.data.teams):
            print('Invalid choice.')
            return

        team_id = self.data.teams[choice - 1]['id']
        self.show_team(team_id)

    def sort_by_fee(self, sessions):
        # Sorts available appointments by consultation fee.

        for i in range(len(sessions)):
            for j in range(i + 1, len(sessions)):
                if sessions[i]['doctor']['fee'] > sessions[j]['doctor']['fee']:
                    temp = sessions[i]
                    sessions[i] = sessions[j]
                    sessions[j] = temp

        return sessions

    def show_sessions(self, sessions, patient_id):
        if len(sessions) == 0:
            print('No appointments available.')
            return

        print('\nAvailable Appointments')

        for i in range(len(sessions)):
            doctor = sessions[i]['doctor']
            schedule = sessions[i]['schedule']

            print(i + 1, doctor['name'], '- $', doctor['fee'])
            print(schedule['schedule_date'], schedule['start_time'],
                  '-', schedule['end_time'])

        try:
            choice = int(input('Choose a doctor (0 to return): '))
        except ValueError:
            print('Invalid choice.')
            return

        if choice == 0:
            return

        if choice < 1 or choice > len(sessions):
            print('Invalid choice.')
            return

        selected = sessions[choice - 1]
        doctor = selected['doctor']
        schedule = selected['schedule']

        print('\nDoctor:', doctor['name'])
        print('Fee: $', doctor['fee'])
        print('Date:', schedule['schedule_date'])
        print('Time:', schedule['start_time'], '-', schedule['end_time'])

        confirm = input('Confirm booking? (y/n): ')

        if confirm.lower() == 'y':
            booking = self.appointments.create_booking(patient_id, schedule['id'])

            if booking is not None:
                print('Booking confirmed. Reference:', booking['id'])
                print('View My Directions for your visit details.')

    def recommend_doctors(self, department_id, patient_id):
        sessions = self.appointments.available_sessions(department_id=department_id)
        sessions = self.sort_by_fee(sessions)
        self.show_sessions(sessions, patient_id)

    def recommend_team_doctors(self, team_id, patient_id):
        sessions = self.appointments.available_sessions(team_id=team_id)
        sessions = self.sort_by_fee(sessions)
        self.show_sessions(sessions, patient_id)
