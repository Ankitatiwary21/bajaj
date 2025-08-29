import os
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # optional if frontend served separately

# Serve frontend
app = Flask(__name__, static_folder="frontend", template_folder="frontend")
CORS(app)

# === User info (edit these) ===
FULL_NAME = "ankita tiwary"
DOB_DDMMYYYY = "21112002"
EMAIL = "ankita@example.com"
ROLL_NUMBER = "ABCD123"
# ==============================

def build_user_id() -> str:
    name_norm = FULL_NAME.strip().lower().replace(" ", "_")
    return f"{name_norm}_{DOB_DDMMYYYY}"

def alternating_caps_reversed(letters: str) -> str:
    rev = letters[::-1]
    out = []
    for i, ch in enumerate(rev):
        out.append(ch.upper() if i % 2 == 0 else ch.lower())
    return "".join(out)

# 🔹 Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Existing POST API (/bfhl)
@app.route("/bfhl", methods=["POST"])
def bfhl_post():
    try:
        body = request.get_json(silent=True) or {}
        data = body.get("data", [])
        if not isinstance(data, list):
            return jsonify({"is_success": False, "error": "Invalid payload: 'data' must be an array."}), 400

        even_numbers, odd_numbers, alphabets, special_characters = [], [], [], []
        total_sum, alpha_concat = 0, ""

        for item in data:
            s = str(item).strip()
            if not s:
                continue
            if s.isdigit():
                n = int(s)
                (even_numbers if n % 2 == 0 else odd_numbers).append(s)
                total_sum += n
            elif s.isalpha():
                alphabets.append(s.upper())
                alpha_concat += s
            else:
                special_characters.append(s)

        concat_string = alternating_caps_reversed(alpha_concat)

        resp = {
            "is_success": True,
            "user_id": build_user_id(),
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string
        }
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 500

# 🔹 Optional GET
@app.get("/bfhl")
def bfhl_get():
    return jsonify({"operation_code": 1}), 200

# 🔹 New POST API (/predict) for image captioning
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400

        # Decode base64 image
        image_b64 = data['image'].split(",")[-1]
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(BytesIO(image_bytes))

        # TODO: Replace with your image captioning model
        caption = "This is a dummy caption for testing."

        return jsonify({"caption": caption})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
