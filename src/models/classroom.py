class Classroom:
    def __init__(self, class_name):
        self.class_name = class_name
        self.students = []
        self.assignments = []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def get_assignments(self):
        return self.assignments

    def get_students(self):
        return self.students