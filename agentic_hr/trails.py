import os
import pandas as pd
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI


# 1. Configuration
my_key = "AIzaSyDx8TFLvEhQgrmcUht4MWz6ManGoZpTg0g" 

# Set this for the system/CrewAI to find
os.environ["GOOGLE_API_KEY"] = my_key
os.environ["GEMINI_API_KEY"] = my_key

# Now initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    verbose=True,   
    temperature=0.5,
    google_api_key=my_key
)
# 2. Data Logic
def load_hr_data():
    try:
        df = pd.read_csv('employees.csv') 
        today = datetime.now().strftime('%m-%d')
        
        df['Date_of_Birth'] = df['Date_of_Birth'].astype(str)
        df['Join_Date'] = df['Join_Date'].astype(str)
        
        bday_people = df[df['Date_of_Birth'].str.contains(today)]
        new_hires = df[df['Join_Date'].str.contains(today)]
        
        return {
            "birthdays": bday_people.to_dict(orient='records'),
            "onboardings": new_hires.to_dict(orient='records')
        }
    except FileNotFoundError:
        return {"birthdays": [], "onboardings": []}

daily_data = load_hr_data()

# 3. Define the Agents
hr_monitor = Agent(
    role='HR Data Coordinator',
    goal='Accurately identify employees celebrating milestones today.',
    backstory='You are detail-oriented. You extract names and roles from raw data.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

comms_specialist = Agent(
    role='Internal Communications Specialist',
    goal='Write personalized, warm, and professional emails for internal announcements.',
    backstory='You turn dry HR data into heart-felt messages that boost company morale.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 4. Define the Tasks
extraction_task = Task(
    description=(
        f"Analyze this structured data: {daily_data}. "
        "List every person having a birthday or starting their first day today. "
        "If the data is empty, explicitly state 'No events today'."
    ),
    expected_output="A list of names and their specific event type (Birthday or New Hire).",
    agent=hr_monitor
)

writing_task = Task(
    description=(
        "Based on the list provided by the HR Coordinator, draft personalized emails. "
        "For birthdays: Wish them a great year. For new hires: Welcome them to the team. "
        "Include the subject line and email body for each."
    ),
    expected_output="A professional document containing all formatted email drafts.",
    agent=comms_specialist,
    context=[extraction_task] # This links the output of the first task to the second
)

# 5. Assemble the Crew
hr_crew = Crew(
    agents=[hr_monitor, comms_specialist],
    tasks=[extraction_task, writing_task],
    process=Process.sequential
)

result = hr_crew.kickoff()

print("\n\n########################")
print("## FINAL EMAIL DRAFTS ##")
print("########################\n")
print(result)