def generate_reminder(name, amount, due_date):
    return f"""
    Act as a smart payment assistant. Generate a polite yet firm reminder for {name} 
    to pay ₹{amount} by {due_date}. Use professional but human-friendly tone.
    """
