import streamlit as st

# Basic Streamlit setup
st.title("HealthCare Buddy")
st.write("Welcome to the AI-powered HealthCare Buddy! How can I assist you today?")

# User input for health symptoms
user_input = st.text_input("Describe your symptoms:")

# Placeholder for the chatbot response
if user_input:
    st.write("Analyzing your symptoms...")
    # Here, we will add the response logic later
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample knowledge base of conditions and treatments
knowledge_base = {
    "headache": "Persistent headaches can be caused by tension, dehydration, or sinus issues.",
    "sore throat": "A sore throat and cough can be symptoms of a cold, flu, or allergies.",
    "muscle soreness": "For muscle soreness, consider rest, hydration, and applying ice to reduce inflammation."
}


# Basic function to match symptoms
def analyze_symptoms(user_symptom):
    # Convert user input and knowledge base into embeddings
    user_embedding = model.encode(user_symptom)
    best_match = None
    best_score = -1

    # Compare user input with each condition in the knowledge base
    for condition, advice in knowledge_base.items():
        condition_embedding = model.encode(condition)
        similarity = util.pytorch_cos_sim(user_embedding, condition_embedding).item()

        if similarity > best_score:
            best_match = advice
            best_score = similarity

    return best_match


# Update Streamlit app to use symptom analysis
if user_input:
    response = analyze_symptoms(user_input)
    if response:
        st.write(f"HealthCare Buddy's advice: {response}")
    else:
        st.write("Sorry, I couldn't find relevant information.")
