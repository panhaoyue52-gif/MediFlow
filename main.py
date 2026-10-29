from data_manager import DataManager
from actions.appointment import AppointmentSystem
from recommendation import RecommendationSystem
from user_interface import PatientSystem
from navigation import NavigationSystem


class MediFlow:
    # Connects all hospital systems and manages the menus.

    def __init__(self):
        self.data = DataManager()
        self.appointments = AppointmentSystem(self.data)
        self.recommendations = RecommendationSystem(self.data, self.appointments)

        self.patients = PatientSystem(
            self.data, self.appointments, self.recommendations
        )

        self.navigation = NavigationSystem(self.data, self.appointments)

    def get_number(self, message):
        try:
            return int(input(message))
        except ValueError:
            print('Invalid number.')
            return 0

    def my_appointments(self, patient_id):
        bookings = self.appointments.patient_bookings(patient_id)

        if len(bookings) == 0:
            print('No appointments found.')
            return

        print('\nMy Appointments')

        for booking in bookings:
            print(booking['id'], booking['doctor_name'],
                  booking['visit_date'])

            if booking['status'] == 1:
                print('Status: Booked')
            elif booking['status'] == 2:
                print('Status: Checked in')
            elif booking['status'] == 3:
                print('Status: Cancelled')
            elif booking['status'] == 4:
                print('Status: Completed')

        choice = input('\nCancel an appointment? (y/n): ')

        if choice.lower() == 'y':
            booking_id = self.get_number('Booking reference: ')

            if booking_id != 0:
                if self.appointments.cancel_booking(patient_id, booking_id):
                    print('Appointment cancelled.')

    def complete_visit(self, patient_id):
        bookings = self.appointments.patient_bookings(patient_id)
        found = False

        print('\nMy Active Appointments')

        for booking in bookings:
            if booking['status'] in [1, 2]:
                print(booking['id'], booking['doctor_name'],
                      booking['visit_date'])
                found = True

        if not found:
            print('No active appointments.')
            return

        booking_id = self.get_number('Booking reference (0 to return): ')

        if booking_id == 0:
            return

        if self.appointments.complete_booking(patient_id, booking_id):
            print('Visit completed.')

    def patient_menu(self, patient_id):
        while True:
            print('\n====== MEDIFLOW ======')
            print('1. Book appointment')
            print('2. My appointments')
            print('3. Follow-up visit')
            print('4. Hospital guide')
            print('5. After-visit help')
            print('6. Find a clinic')
            print('7. Medical teams')
            print('8. Doctors')
            print('9. First-visit guide')
            print('10. Complete visit (demo)')
            print('0. Sign out')

            choice = input('Choose: ')

            if choice == '1':
                department_id = self.recommendations.choose_department()

                if department_id != 0:
                    self.recommendations.recommend_doctors(
                        department_id, patient_id
                    )

            elif choice == '2':
                self.my_appointments(patient_id)

            elif choice == '3':
                self.patients.follow_up(patient_id)

            elif choice == '4':
                self.navigation.hospital_navigation(patient_id)

            elif choice == '5':
                self.navigation.after_visit_help()

            elif choice == '6':
                self.navigation.choose_clinic()

            elif choice == '7':
                self.recommendations.choose_team()

            elif choice == '8':
                department_id = self.recommendations.choose_department()

                if department_id != 0:
                    self.recommendations.show_doctors(department_id)

            elif choice == '9':
                self.patients.first_visit()

            elif choice == '10':
                self.complete_visit(patient_id)

            elif choice == '0':
                print('Signed out.')
                break

            else:
                print('Invalid choice.')

    def run(self):
        if not self.data.is_ready():
            print('Hospital data could not be loaded.')
            return

        while True:
            print('\n====== WELCOME TO MEDIFLOW ======')
            print('1. New patient')
            print('2. Returning patient')
            print('0. Exit')

            choice = input('Choose: ')

            if choice == '1':
                patient_id = self.patients.register()

                if patient_id is not None:
                    self.patient_menu(patient_id)

            elif choice == '2':
                patient_id = self.patients.login()

                if patient_id is not None:
                    self.patient_menu(patient_id)

            elif choice == '0':
                print('Goodbye!')
                break

            else:
                print('Invalid choice.')


if __name__ == '__main__':
    app = MediFlow()
    app.run()
