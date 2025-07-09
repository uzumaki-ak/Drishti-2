from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import init_llm_agent, send_llm_message, reset_llm_chat

app = Flask(__name__)
CORS(app)  # Allows requests from your React frontend

# Default initialization
model, chat, context = init_llm_agent()

@app.route("/api/chat", methods=["POST"])
def chat_route():
    global model, chat, context

    data = request.get_json()
    user_message = data.get("message", "")
    scenario_id = data.get("scenario_id", "scenario_1")

    # Load context for the given scenario
    model, chat, context = init_llm_agent(scenario_id)
    response_text = send_llm_message(chat, context, user_message)
    return jsonify({"response": response_text})

@app.route("/api/reset", methods=["POST"])
def reset_route():
    global chat
    chat = reset_llm_chat(model)
    return jsonify({"status": "Chat reset successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
