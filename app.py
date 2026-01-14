from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app, origins="*")

# Load API key securely from environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.json
        user_input = data.get("input")
        mode = data.get("mode")

        if not user_input or not mode:
            return jsonify({"error": "Input or mode missing"}), 400

        if mode == "phishing":
            prompt = f"""
You are a cybersecurity expert.

Analyze the following message or link.

Give output in this exact format:

Verdict: Safe / Suspicious / Phishing

Why:
- Point 1 (simple)
- Point 2 (simple)
- Point 3 (simple)

Tip:
(1-line safety advice)

Keep it short, clean, and easy to read.

Message: {user_input}
"""

        elif mode == "internship":
            prompt = f"""
You are a cybersecurity and career safety expert.

Analyze this internship or job message.

Give output in this exact format:

Verdict: Legit / Suspicious / Fake

Red Flags:
- Point 1
- Point 2
- Point 3

Advice:
(1-line safety advice)

Keep it short, clean, and easy to read.

Message: {user_input}
"""

        elif mode == "password":
            prompt = f"""
You are a cybersecurity expert.

Analyze this password.

Give output in this exact format:

Strength: Weak / Medium / Strong

Why:
- Reason 1
- Reason 2

Improve by:
- Tip 1
- Tip 2

Keep it short and simple.

Password: {user_input}
"""

        else:
            return jsonify({"error": "Invalid mode"}), 400

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )

        result_text = response.candidates[0].content.parts[0].text

        return jsonify({"result": result_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
