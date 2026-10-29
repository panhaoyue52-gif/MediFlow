class NavigationSystem:
    # Manages clinic locations and hospital directions.

    def __init__(self, data, appointments):
        self.data = data
        self.appointments = appointments

    def find_department(self, department_id):
        return self.data.find_record(self.data.departments, department_id)

    def department_path(self, department_id):
        # Recursively finds the department hierarchy.

        department = self.find_department(department_id)

        if department is None:
            return []

        if department['parent_id'] == 0:
            return [department['name']]

        path = self.department_path(department['parent_id'])
        path.append(department['name'])

        return path

    def show_department_path(self, department_id):
        path = self.department_path(department_id)

        for name in path:
            print(name)

    def find_clinic(self, department_id):
        department = self.find_department(department_id)

        if department is None:
            print('Clinic not found.')
            return

        print('\nDepartment Path')
        self.show_department_path(department_id)

        print('\nClinic:', department['name'])
        print('Building:', department['building'])
        print('Floor:', department['floor'])
        print('Reception:', department['reception'])
        print('Room:', department['room'])

    def choose_clinic(self):
        departments = self.data.departments

        if len(departments) == 0:
            print('No departments available.')
            return

        print('\nHospital Departments')

        for i in range(len(departments)):
            print(i + 1, departments[i]['name'])

        try:
            choice = int(input('Choose a department (0 to return): '))
        except ValueError:
            print('Invalid choice.')
            return

        if choice == 0:
            return

        if choice < 1 or choice > len(departments):
            print('Invalid choice.')
            return

        department_id = departments[choice - 1]['id']
        self.find_clinic(department_id)

    def visit_directions(self, patient_id):
        bookings = self.appointments.patient_bookings(patient_id)
        active_bookings = []

        print('\nMy Appointments')

        for booking in bookings:
            if booking['status'] in [1, 2]:
                active_bookings.append(booking)
                print(booking['id'], booking['doctor_name'],
                      booking['visit_date'])

        if len(active_bookings) == 0:
            print('No active appointments.')
            return

        try:
            booking_id = int(input('Booking reference (0 to return): '))
        except ValueError:
            print('Invalid booking reference.')
            return

        if booking_id == 0:
            return

        for booking in active_bookings:
            if booking['id'] == booking_id:
                print('\nYour Visit Plan')
                print('Doctor:', booking['doctor_name'])
                print('Date:', booking['visit_date'])
                print('Time:', booking['start_time'],
                      '-', booking['end_time'])

                self.find_clinic(booking['dept_id'])

                print('\nVisit Instructions')
                print('1. Arrive at the outpatient building.')
                print('2. Check in at the clinic reception.')
                print('3. Wait for your consultation.')
                print('4. Follow your doctor\'s instructions.')
                return

        print('Booking not found.')

    def after_visit_help(self):
        while True:
            print('\nAfter-Visit Help')
            print('1. Tests and imaging')
            print('2. Collect films or reports')
            print('3. Payment and pharmacy')
            print('4. Admission or surgery')
            print('5. Follow-up visit')
            print('0. Back')

            choice = input('Choose: ')

            if choice == '1':
                print('\nTests and Imaging')
                print('1. Confirm your test request.')
                print('2. Complete payment if required.')
                print('3. Go to Diagnostic Building, Ground Floor.')
                print('4. Check in at the imaging reception.')

            elif choice == '2':
                print('\nFilms and Reports')
                print('1. Go to Diagnostic Building, Ground Floor.')
                print('2. Visit the report collection desk.')
                print('3. Follow the collection instructions.')

            elif choice == '3':
                print('\nPayment and Pharmacy')
                print('1. Go to Outpatient Building, Ground Floor.')
                print('2. Complete payment if required.')
                print('3. Collect medicine from the pharmacy.')

            elif choice == '4':
                print('\nAdmission and Surgery')
                print('1. Follow your doctor\'s instructions.')
                print('2. Go to Inpatient Building, Ground Floor.')
                print('3. Visit the admissions desk.')
                print('4. Confirm your admission arrangements.')

            elif choice == '5':
                print('\nFollow-up Visit')
                print('1. Return to the main menu.')
                print('2. Select Follow-up Visit.')
                print('3. Choose a doctor from your care team.')

            elif choice == '0':
                break

            else:
                print('Invalid choice.')

    def hospital_navigation(self, patient_id):
        while True:
            print('\nHospital Guide')
            print('1. My directions')
            print('2. Find a clinic')
            print('3. After-visit help')
            print('0. Back')

            choice = input('Choose: ')

            if choice == '1':
                self.visit_directions(patient_id)

            elif choice == '2':
                self.choose_clinic()

            elif choice == '3':
                self.after_visit_help()

            elif choice == '0':
                break

            else:
                print('Invalid choice.')
