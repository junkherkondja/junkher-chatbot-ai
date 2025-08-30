import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# 🔑 Connect to OpenAI securely (from environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# --- Accounting functions ---
def current_ratio(current_assets, current_liabilities):
    return round(current_assets / current_liabilities, 2)

def debt_to_equity(total_liabilities, shareholders_equity):
    return round(total_liabilities / shareholders_equity, 2)

def return_on_assets(net_income, total_assets):
    return round((net_income / total_assets) * 100, 2)

def gross_profit_margin(gross_profit, revenue):
    return round((gross_profit / revenue) * 100, 2)

# --- AI Chat Function ---
def accounting_bot(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Junkher Chatbot AI, a professional accounting tutor and assistant. You explain accounting concepts step by step and solve financial ratios clearly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data["message"]

    if user_input.startswith("calc"):
        parts = user_input.split()
        try:
            if parts[1] == "current_ratio":
                result = current_ratio(float(parts[2]), float(parts[3]))
                reply = f"📊 Current Ratio = {result}"
            elif parts[1] == "debt_to_equity":
                result = debt_to_equity(float(parts[2]), float(parts[3]))
                reply = f"📊 Debt-to-Equity Ratio = {result}"
            elif parts[1] == "roa":
                result = return_on_assets(float(parts[2]), float(parts[3]))
                reply = f"📊 Return on Assets (%) = {result}"
            elif parts[1] == "gpm":
                result = gross_profit_margin(float(parts[2]), float(parts[3]))
                reply = f"📊 Gross Profit Margin (%) = {result}"
            else:
                reply = "⚠️ Unknown calculation. Try: current_ratio, debt_to_equity, roa, gpm"
        except:
            reply = "⚠️ Error in calculation. Example: calc current_ratio 50000 25000"
    else:
        reply = accounting_bot(user_input)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
