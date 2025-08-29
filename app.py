import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# === Your details (edit these 3 lines only) ===
FULL_NAME = "ankita tiwary"    # full name in lowercase, spaces allowed
DOB_DDMMYYYY = "21112002"      # ddmmyyyy (no separators)
EMAIL = "ankita@example.com"
ROLL_NUMBER = "ABCD123"
# =============================================

def build_user_id() -> str:
    """user_id = full_name_ddmmyyyy (name as lowercase with underscores)."""
    name_norm = FULL_NAME.strip().lower().replace(" ", "_")
    return f"{name_norm}_{DOB_DDMMYYYY}"

def alternating_caps_reversed(letters: str) -> str:
    """
    Take all alphabetic letters (already concatenated),
    reverse them, then apply alternating caps starting Upper.
    """
    rev = letters[::-1]
    out = []
    for i, ch in enumerate(rev):
        out.append(ch.upper() if i % 2 == 0 else ch.lower())
    return "".join(out)

@app.route("/bfhl", methods=["POST"])
def bfhl_post():
    try:
        body = request.get_json(silent=True) or {}
        data = body.get("data", [])

        if not isinstance(data, list):
            return jsonify({"is_success": False, "error": "Invalid payload: 'data' must be an array."}), 400

        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0
        alpha_concat = ""

        for item in data:
            s = str(item).strip()
            if not s:
                continue

            if s.isdigit():                 # numbers (only digits)
                n = int(s)
                (even_numbers if n % 2 == 0 else odd_numbers).append(s)  # keep strings
                total_sum += n
            elif s.isalpha():               # alphabets only
                alphabets.append(s.upper())  # store uppercase version
                alpha_concat += s            # keep original letters for concat logic
            else:                           # everything else = special characters
                special_characters.append(s)

        concat_string = alternating_caps_reversed(alpha_concat)

        resp = {
            "is_success": True,
            "user_id": build_user_id(),
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,                 # strings
            "even_numbers": even_numbers,               # strings
            "alphabets": alphabets,                     # uppercase words
            "special_characters": special_characters,
            "sum": str(total_sum),                      # sum as string
            "concat_string": concat_string
        }
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 500

# (Optional) GET /bfhl endpoint some tests expect
@app.get("/bfhl")
def bfhl_get():
    return jsonify({"operation_code": 1}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
