from services.payment_logic import generate_reminder

def test_generate_reminder():
    prompt = generate_reminder("Tushar", 5000, "2025-08-05")
    assert "₹5000" in prompt and "Tushar" in prompt and "2025-08-05" in prompt
