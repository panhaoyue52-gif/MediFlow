from datetime import date


class AppointmentSystem:
    # Manages booking rules and appointment records.

    def __init__(self, data):
        self.data = data

    def remaining(self, schedule):
        used = 0

        for booking in self.data.appointments:
            if booking['schedule_id'] == schedule['id']:
                if booking['status'] != 3:
                    used += 1

        return schedule['appointment_limit'] - used

    def conflict(self, patient_id, schedule):
        for booking in self.data.appointments:
            if booking['patient_id'] == patient_id:
                if booking['status'] != 3:
                    if booking['visit_date'] == schedule['schedule_date']:
                        if booking['start_time'] < schedule['end_time']:
                            if booking['end_time'] > schedule['start_time']:
                                return True

        return False

    def available_sessions(self, department_id=0, team_id=0):
        sessions = []

        for schedule in self.data.schedules:
            if schedule['is_deleted'] != 0:
                continue

            if schedule['schedule_date'] < str(date.today()):
                continue

            if self.remaining(schedule) <= 0:
                continue

            doctor = self.data.find_record(
                self.data.doctors, schedule['doctor_id']
            )

            if doctor is None:
                continue

            if department_id != 0 and doctor['department_id'] != department_id:
                continue

            if team_id != 0 and doctor['team_id'] != team_id:
                continue

            sessions.append({
                'doctor': doctor,
                'schedule': schedule
            })

        return sessions

    def create_booking(self, patient_id, schedule_id):
        patient = self.data.find_record(self.data.patients, patient_id)
        schedule = self.data.find_record(self.data.schedules, schedule_id)

        if patient is None or schedule is None:
            print('Patient or appointment not found.')
            return None

        if schedule['is_deleted'] != 0:
            print('Appointment unavailable.')
            return None

        if schedule['schedule_date'] < str(date.today()):
            print('Appointment unavailable.')
            return None

        if self.remaining(schedule) <= 0:
            print('Appointment full.')
            return None

        if self.conflict(patient_id, schedule):
            print('You already have an appointment at this time.')
            return None

        doctor = self.data.find_record(self.data.doctors, schedule['doctor_id'])

        if doctor is None:
            print('Doctor not found.')
            return None

        booking_id = 1
        queue = 1

        for booking in self.data.appointments:
            if booking['id'] >= booking_id:
                booking_id = booking['id'] + 1

            if booking['schedule_id'] == schedule_id:
                if booking['queue_no'] >= queue:
                    queue = booking['queue_no'] + 1

        record = {
            'id': booking_id,
            'patient_id': patient_id,
            'patient_name': patient['name'],
            'doctor_id': doctor['id'],
            'doctor_name': doctor['name'],
            'dept_id': doctor['department_id'],
            'schedule_id': schedule_id,
            'visit_date': schedule['schedule_date'],
            'start_time': schedule['start_time'],
            'end_time': schedule['end_time'],
            'queue_no': queue,
            'status': 1,
            'is_deleted': 0
        }

        self.data.appointments.append(record)

        if self.data.save_appointments():
            return record

        self.data.appointments.remove(record)
        print('Booking could not be saved.')
        return None

    def patient_bookings(self, patient_id):
        bookings = []

        for booking in self.data.appointments:
            if booking['patient_id'] == patient_id:
                bookings.append(booking)

        return bookings

    def cancel_booking(self, patient_id, booking_id):
        for booking in self.data.appointments:
            if booking['id'] == booking_id:
                if booking['patient_id'] != patient_id:
                    break

                if booking['status'] != 1:
                    print('Cannot cancel this booking.')
                    return False

                if booking['visit_date'] < str(date.today()):
                    print('Cannot cancel this booking.')
                    return False

                old_status = booking['status']
                old_deleted = booking['is_deleted']

                booking['status'] = 3
                booking['is_deleted'] = 1

                if self.data.save_appointments():
                    return True

                booking['status'] = old_status
                booking['is_deleted'] = old_deleted
                print('Cancellation could not be saved.')
                return False

        print('Booking not found.')
        return False

    def complete_booking(self, patient_id, booking_id):
        for booking in self.data.appointments:
            if booking['id'] == booking_id:
                if booking['patient_id'] != patient_id:
                    break

                if booking['status'] not in [1, 2]:
                    print('No active booking found.')
                    return False

                old_status = booking['status']
                booking['status'] = 4

                if self.data.save_appointments():
                    return True

                booking['status'] = old_status
                print('Visit status could not be saved.')
                return False

        print('Booking not found.')
        return False
