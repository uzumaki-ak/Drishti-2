import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

# Read Firebase config from environment variables
firebase_config = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")

# Configure the API
genai.configure(api_key=api_key)

# Load scene context data from Firestore based on scenario ID
def load_scene_context(scenario_id="scenario_1") -> str:
    try:
        doc = db.collection("scene_contexts").document(scenario_id).get()
        if not doc.exists:
            raise ValueError(f"{scenario_id} not found in Firestore.")

        context_json = doc.to_dict()

        context_str = (
            f"Scene at {context_json.get('location', 'unknown')} on {context_json.get('timestamp', 'unknown')}:\n"
            f"{context_json.get('summary', 'No summary provided.')}\n"
            f"Sentiment: {context_json.get('sentiment', 'neutral')}, "
            f"Tags: {', '.join(context_json.get('tags', []))}\n"
            f"People present: {context_json.get('scene_stats', {}).get('total_people', 'unknown')}, "
            f"Flow direction: {context_json.get('scene_stats', {}).get('flow_direction', 'unclear')}\n"
        )

        anomalies = context_json.get("anomalies", [])
        if anomalies:
            context_str += f"Anomalies: {anomalies[0].get('description', 'Unclear anomaly')}\n"

        lost_items = context_json.get("lost_and_found", {}).get("items", [])
        if lost_items:
            context_str += f"Lost item: {lost_items[0].get('description', 'Unclear lost item')}\n"

        recommendations = context_json.get("recommendations", [])
        if recommendations:
            context_str += (
                f"Recommendation: {recommendations[0].get('action', 'No action')} "
                f"(Reason: {recommendations[0].get('justification', 'No reason')})\n"
            )

        return context_str.strip()

    except Exception:
        return (
            "This is a public scene monitoring system. Analyze crowd behavior, detect anomalies, "
            "and recommend safety actions based on any known or observable conditions."
        )

# Save new scene context to Firestore
def save_scene_context(context_data: dict, scenario_id="current") -> str:
    try:
        db.collection("scene_contexts").document(scenario_id).set(context_data)
        return "Scene context saved successfully."
    except Exception as e:
        return f"Error saving context: {str(e)}"

# Initialize LLM with scenario context
def init_llm_agent(scenario_id="scenario_1", model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    context = load_scene_context(scenario_id)
    return model, chat, context

# Send a message using the LLM with context
def send_llm_message(chat, context, user_message: str) -> str:
    try:
        prompt = (
            "You are an emergency response AI assistant for crowd and anomaly monitoring.\n"
            "Use the provided scene data to recommend urgent and actionable responses.\n"
            "Be specific. Do not repeat the question. Do not say 'based on current event data'.\n\n"
            f"{context}\n\n"
            f"User Query: {user_message}"
        )
        print("------ FULL PROMPT TO GEMINI ------")
        print(prompt)
        print("-----------------------------------")
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Reset chat history
def reset_llm_chat(model):
    return model.start_chat(history=[])

# Standalone test mode
if __name__ == "__main__":
    model, chat, context = init_llm_agent()
    print("\nChat with Gemini! (type 'exit' to quit, 'clear' to reset chat history)\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.strip().lower() == "clear":
            chat = reset_llm_chat(model)
            print("Chat history cleared.")
            continue

        answer = send_llm_message(chat, context, user_input)
        print(f"Gemini: {answer}")
