import streamlit as st
import requests
import os 

# Groq API details
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY") # Replace with your Groq API key

# Function to interact with Groq Llama model
def generate_response(prompt, max_tokens=1000, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# Application title
st.title("🌍 AI-Powered Travel Planner ")

# Step 1: Gather user inputs
st.header("Tell us about your trip")
destination = st.text_input("Where are you traveling to?")
duration = st.number_input("How many days?", min_value=1, max_value=30, step=1)
budget = st.selectbox("What is your budget?", ["Budget", "Moderate", "Luxury"])
interests = st.multiselect(
    "What are your interests?",
    ["Nature", "Adventure", "History", "Food", "Relaxation", "Culture"]
)
dietary_restrictions = st.text_input("Any dietary restrictions?")
mobility_concerns = st.selectbox(
    "Do you have any mobility concerns?",
    ["None", "Limited walking", "Wheelchair accessible"]
)

# Step 2: Confirm inputs and generate itinerary
if st.button("Plan My Trip"):
    with st.spinner("Generating your personalized itinerary..."):
        prompt = (
            f"Create a detailed travel itinerary for a {duration}-day trip to {destination}. "
            f"The budget is {budget.lower()}, and the traveler is interested in {', '.join(interests)}. "
            f"Consider dietary restrictions: {dietary_restrictions}, and mobility concerns: {mobility_concerns}. "
            f"Provide a detailed day-by-day plan including activities, restaurants, and timing."
        )
        itinerary = generate_response(prompt)

        # Display the output
        st.success("Here is your personalized itinerary!")
        st.text_area("Your Itinerary", value=itinerary, height=300)

# Flexible Inputs (Bonus Challenge)
st.header("Bonus Challenge")
flex_input = st.text_input("Enter a vague trip idea (e.g., 'I want a mix of famous and offbeat places').")
if st.button("Refine My Idea"):
    with st.spinner("Refining your trip idea..."):
        refine_prompt = (
            f"Refine the following vague input into a precise travel plan request: '{flex_input}'. "
            "Add necessary details such as destination, duration, budget, and interests."
        )
        refined_plan = generate_response(refine_prompt)

        # Display refined result
        st.success("Here's a refined trip request!")
        st.write(refined_plan)

# Footer
st.markdown("---")
st.markdown("Powered by [Groq Llama](https://groq.com) and Streamlit 🚀")
