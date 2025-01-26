
## Overview
This project is a personalized travel itinerary generator built using Streamlit and Groq's Llama 3.1 (8B) API. Users can input their travel preferences, and the system generates a detailed, day-by-day itinerary tailored to their needs. It also refines vague inputs into precise travel plans.

## Features
- Collects user preferences (destination, budget, interests, etc.).
- Generates detailed, personalized travel itineraries.
- Handles vague or incomplete inputs by refining them into actionable queries.
- Deployed using Streamlit for easy access.

## How It Works
1. The app gathers user inputs through a simple interface.
2. It sends the prompts to the Groq API using the Llama 3.1 model.
3. The API processes the input and generates a detailed travel plan.
4. Users receive a multi-day itinerary with activities, dining suggestions, and timing.

## Installation
To run the project locally:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your-repo-name
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run travel_planner_groq.py
   ```

## Hosted Application
The application is deployed and accessible online:
[Deployed App Link](https://testpy-tj9eg9lxqqf28gd6cdn65x.streamlit.app/)

## Files
- **`travel_planner_groq.py`**: Main application code.
- **`requirements.txt`**: Python dependencies for the project.
- **`prompts_documentation.pdf`**: Detailed prompts, inputs, and outputs documentation.

## Contact
For any questions or issues, feel free to contact:
- **Email**:**devarajan8.official@gmail.com**

---