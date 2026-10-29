from data_manager import DataManager
from actions.appointment import AppointmentSystem
from recommendation import RecommendationSystem
from navigation import NavigationSystem


class MediFlowTests:
    # Checks core data, booking rules and navigation.

    def __init__(self):
        self.data = DataManager()
        self.appointments = AppointmentSystem(self.data)
        self.recommendations = RecommendationSystem(self.data, self.appointments)
        self.navigation = NavigationSystem(self.data, self.appointments)

    def test_data(self):
        assert self.data.is_ready()
        assert len(self.data.patients) > 0
        assert len(self.data.doctors) > 0
        assert len(self.data.departments) > 0
        assert len(self.data.schedules) > 0

        print('Data loading: Passed')

    def test_find_record(self):
        records = [
            {'id': 1, 'name': 'Tom'},
            {'id': 2, 'name': 'Alice'}
        ]

        assert self.data.find_record(records, 1)['name'] == 'Tom'
        assert self.data.find_record(records, 99) is None

        print('Record search: Passed')

    def test_departments(self):
        choices = self.recommendations.get_departments()

        assert len(choices) > 0

        for department in choices:
            found = False

            for doctor in self.data.doctors:
                if doctor['department_id'] == department['id']:
                    found = True

            assert found

        print('Department selection: Passed')

    def test_sorting(self):
        sessions = [
            {'doctor': {'fee': 100}},
            {'doctor': {'fee': 30}},
            {'doctor': {'fee': 80}}
        ]

        result = self.recommendations.sort_by_fee(sessions)

        assert result[0]['doctor']['fee'] == 30
        assert result[1]['doctor']['fee'] == 80
        assert result[2]['doctor']['fee'] == 100

        print('Doctor sorting: Passed')

    def test_capacity(self):
        schedule = {
            'id': 1,
            'appointment_limit': 2
        }

        test_bookings = [
            {'schedule_id': 1, 'status': 1},
            {'schedule_id': 1, 'status': 3}
        ]

        original = self.data.appointments

        try:
            self.data.appointments = test_bookings

            assert self.appointments.remaining(schedule) == 1

            test_bookings[1]['status'] = 1

            assert self.appointments.remaining(schedule) == 0

        finally:
            self.data.appointments = original

        print('Appointment capacity: Passed')

    def test_conflict(self):
        schedule = {
            'schedule_date': '2026-11-10',
            'start_time': '09:00',
            'end_time': '12:00'
        }

        test_bookings = [
            {
                'patient_id': 100,
                'visit_date': '2026-11-10',
                'start_time': '09:00',
                'end_time': '12:00',
                'status': 1
            }
        ]

        original = self.data.appointments

        try:
            self.data.appointments = test_bookings

            assert self.appointments.conflict(100, schedule)
            assert not self.appointments.conflict(101, schedule)

            schedule['start_time'] = '12:00'
            schedule['end_time'] = '15:00'

            assert not self.appointments.conflict(100, schedule)

            test_bookings[0]['status'] = 3

            schedule['start_time'] = '09:00'
            schedule['end_time'] = '12:00'

            assert not self.appointments.conflict(100, schedule)

        finally:
            self.data.appointments = original

        print('Appointment conflicts: Passed')

    def test_recursion(self):
        path = self.navigation.department_path(5)

        assert path == ['Surgery', 'Orthopaedics']

        root_path = self.navigation.department_path(4)
        assert root_path == ['Surgery']

        missing_path = self.navigation.department_path(999)
        assert missing_path == []

        print('Recursive department paths: Passed')

    def run(self):
        if not self.data.is_ready():
            print('Tests cannot start. Hospital data is missing.')
            return

        self.test_data()
        self.test_find_record()
        self.test_departments()
        self.test_sorting()
        self.test_capacity()
        self.test_conflict()
        self.test_recursion()

        print('\nAll tests passed!')


if __name__ == '__main__':
    tests = MediFlowTests()
    tests.run()
