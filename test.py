import streamlit as st
import requests
import os

# =============================================
# API CONFIGURATION
# =============================================
# Replace the API_URL and API_KEY with your actual endpoint details.
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your Groq API key

def generate_response(prompt, max_tokens=1000, temperature=0.7):
    """
    Function to interact with the Groq Llama model.
    It sends the given prompt to the API endpoint and returns the response text.
    """
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

# =============================================
# STREAMLIT APPLICATION - AI Travel Planner
# =============================================
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")
st.title("🌍 AI Travel Planner - AI/ML Internship Assignment")

st.markdown("This application guides travelers by first refining user inputs, then suggesting activities and finally generating a personalized day-by-day itinerary.")

# -------------------------------
# STEP 1: User Context Input
# -------------------------------
st.header("Step 1: Enter Your Travel Details")
starting_location = st.text_input("Starting Location", placeholder="Enter your starting city or airport")
destination = st.text_input("Destination", placeholder="Where are you traveling to?")
trip_duration = st.number_input("Trip Duration (in days)", min_value=1, max_value=30, step=1)
budget = st.selectbox("Budget", options=["Budget", "Moderate", "Luxury"])
trip_purpose = st.text_input("Purpose of Trip", placeholder="e.g., leisure, business, adventure")
preferences = st.multiselect("Interests/Preferences", ["Nature", "Adventure", "History", "Food", "Culture", "Relaxation", "Shopping", "Nightlife"])
dietary_restrictions = st.text_input("Dietary Restrictions", placeholder="e.g., vegetarian, vegan, none")
mobility_concerns = st.selectbox("Mobility Concerns", ["None", "Limited walking", "Wheelchair accessible"])
accommodation = st.selectbox("Accommodation Preference", ["Budget", "Moderate", "Luxury"])
flex_input = st.text_input("Flexible Trip Description", placeholder="Enter a vague trip idea, e.g., 'I want a mix of famous and offbeat places'")

# Variable to hold activity suggestions for later use
activity_suggestions = ""

# -------------------------------
# STEP 2: Build Your Prompt System
# -------------------------------

# 2a. Input Refinement
if st.button("Refine Inputs"):
    with st.spinner("Refining your inputs..."):
        # System and User Prompt for Input Refinement
        refine_prompt = f"""
You are an AI travel assistant. Given the following user inputs:
- Starting Location: {starting_location}
- Destination: {destination}
- Trip Duration: {trip_duration} days
- Budget: {budget}
- Purpose: {trip_purpose}
- Interests/Preferences: {', '.join(preferences) if preferences else 'None'}
- Dietary Restrictions: {dietary_restrictions if dietary_restrictions else 'None'}
- Mobility Concerns: {mobility_concerns}
- Accommodation Preference: {accommodation}
- Flexible Trip Description: {flex_input if flex_input else 'None'}

Please refine and consolidate these inputs into a clear, precise travel plan request. 
Include clarifying questions or details if any input seems vague.
Return the refined details in a structured, bullet-point format.
"""
        refined_details = generate_response(refine_prompt)
        st.success("Refined Trip Details:")
        st.text_area("Refined Details", value=refined_details, height=200)

# 2b. Activity Suggestions
if st.button("Get Activity Suggestions"):
    with st.spinner("Generating activity suggestions..."):
        # System and User Prompt for Activity Suggestions
        suggestions_prompt = f"""
Based on the following refined travel plan:
- Starting Location: {starting_location}
- Destination: {destination}
- Trip Duration: {trip_duration} days
- Budget: {budget}
- Purpose: {trip_purpose}
- Interests/Preferences: {', '.join(preferences) if preferences else 'None'}
- Dietary Restrictions: {dietary_restrictions if dietary_restrictions else 'None'}
- Mobility Concerns: {mobility_concerns}
- Accommodation Preference: {accommodation}
- Flexible Trip Description: {flex_input if flex_input else 'None'}

Generate a list of up-to-date activity suggestions and top attractions for the destination. 
Include both famous landmarks and hidden gems that match the traveler's preferences.
Provide the list with brief descriptions for each suggestion.
"""
        activity_suggestions = generate_response(suggestions_prompt)
        st.success("Activity Suggestions:")
        st.text_area("Suggestions", value=activity_suggestions, height=200)

# 2c. Detailed Itinerary Generation
if st.button("Plan My Trip"):
    with st.spinner("Generating your detailed itinerary..."):
        # System and User Prompt for Itinerary
        itinerary_prompt = f"""
Based on the following travel plan:
- Starting Location: {starting_location}
- Destination: {destination}
- Trip Duration: {trip_duration} days
- Budget: {budget}
- Purpose: {trip_purpose}
- Interests/Preferences: {', '.join(preferences) if preferences else 'None'}
- Dietary Restrictions: {dietary_restrictions if dietary_restrictions else 'None'}
- Mobility Concerns: {mobility_concerns}
- Accommodation Preference: {accommodation}
- Activity Suggestions: {activity_suggestions if activity_suggestions else 'Not provided'}

Generate a detailed day-by-day itinerary for this trip. 
For each day, include:
• Sightseeing plans with timings
• Meal recommendations
• Activity scheduling based on the user's preferences
Present the itinerary in a clear, structured format with each day labeled.
"""
        itinerary = generate_response(itinerary_prompt)
        st.success("Your Detailed Itinerary:")
        st.text_area("Itinerary", value=itinerary, height=300)

# =============================================
# FOOTER & DOCUMENTATION
# =============================================
st.markdown("---")
st.markdown("### About This Application")
st.markdown("""
This AI-powered travel planner was built as part of an AI/ML Internship Assignment.  
**Prompt System Documentation:**  
- **Input Refinement Prompt:** Refines and consolidates user inputs to handle any vague details.  
- **Activity Suggestions Prompt:** Uses the refined details to generate a list of attractions and activities that match the user’s preferences.  
- **Detailed Itinerary Prompt:** Chains the refined inputs and activity suggestions to generate a personalized, day-by-day travel itinerary.  

The application also supports flexible input formats and clarifies incomplete inputs by prompting for refinements.  
For live testing, this app is hosted on Streamlit.
""")
st.markdown("Cheers,\nDevarajan S")
