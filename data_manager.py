import json


class DataManager:
    # Manages hospital data and file operations.

    def __init__(self):
        self.patients = self.load_data('patients.json')
        self.doctors = self.load_data('doctors.json')
        self.departments = self.load_data('departments.json')
        self.teams = self.load_data('teams.json')
        self.schedules = self.load_data('schedules.json')
        self.appointments = self.load_data('appointments.json')

    def load_data(self, filename):
        try:
            with open('hospital_data/' + filename, 'r') as file:
                return json.load(file)

        except FileNotFoundError:
            print('File not found:', filename)
            return None

        except json.JSONDecodeError:
            print('Invalid JSON data:', filename)
            return None

        except OSError:
            print('Cannot read file:', filename)
            return None

    def save_data(self, filename, data):
        if data is None:
            return False

        try:
            with open('hospital_data/' + filename, 'w') as file:
                json.dump(data, file, indent=4)
            return True

        except (OSError, TypeError, ValueError):
            print('Cannot save file:', filename)
            return False

    def find_record(self, records, record_id):
        if records is None:
            return None

        for record in records:
            if record['id'] == record_id:
                return record

        return None

    def save_patients(self):
        return self.save_data('patients.json', self.patients)

    def save_appointments(self):
        return self.save_data('appointments.json', self.appointments)

    def is_ready(self):
        datasets = [
            self.patients,
            self.doctors,
            self.departments,
            self.teams,
            self.schedules,
            self.appointments
        ]

        for data in datasets:
            if not isinstance(data, list):
                return False

        return True
