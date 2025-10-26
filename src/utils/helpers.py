def format_date(date):
    """Format a date object into a string."""
    return date.strftime("%Y-%m-%d")

def calculate_due_date(assignment):
    """Calculate the due date for an assignment based on its creation date and duration."""
    return assignment.creation_date + timedelta(days=assignment.duration)

def validate_user_input(input_data):
    """Validate user input for various forms."""
    if not input_data:
        raise ValueError("Input cannot be empty.")
    return True

def generate_unique_id():
    """Generate a unique identifier for new users or assignments."""
    import uuid
    return str(uuid.uuid4())