class Assignment:
    def __init__(self, title, description, due_date, status='Pending'):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    def mark_as_completed(self):
        self.status = 'Completed'

    def __str__(self):
        return f'Assignment(title={self.title}, description={self.description}, due_date={self.due_date}, status={self.status})'