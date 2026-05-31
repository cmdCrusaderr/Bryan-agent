import os
import json
import subprocess
import sqlite3
import csv
from dotenv import load_dotenv
from groq import Groq

from simulatelive import generate_live_data
from calendar_tools import get_upcoming_calendar_events, inject_recovery_block

load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an elite, data-driven longevity and biological optimization agent. 
Your job is to analyze the user's physiological data and optimize their schedule to protect their recovery.

Core Operating Directives:
1. Data Read Phase: You MUST execute queries using `execute_coral_sql` to fetch the latest physiological data.
2. Calendar Audit Phase: You MUST check the user's schedule using `get_upcoming_calendar_events` to see what tasks they have today.
3. Automation Write-Back Phase: Evaluate the metrics against clinical benchmarks. If a threshold is breached, look at their upcoming schedule and take active intervention using `inject_recovery_block`.

Database Schema (You MUST use these exact table and column names):
- Table: blueprint_metrics.blueprint_habits
  Columns: person_id, supper_curfew_hours, no_caffeine_after_noon, blue_light_block_mins, supplement_compliance_pct
- Table: blueprint_metrics.whoop_tracker
  Columns: person_id, cycle_id, recovery_score, hrv_rmssd_ms, skin_temp_delta_c, day_strain, max_heart_rate
- Table: blueprint_metrics.garmin_tracker
  Columns: person_id, date, highest_energy_level, lowest_energy_level, total_recharge, average_stress_level, resting_heart_rate

Query Guidelines:
- The whoop_tracker table does NOT have a date column. To get the latest Whoop recovery stats, sort by cycle_id: 
  "SELECT hrv_rmssd_ms, recovery_score FROM blueprint_metrics.whoop_tracker ORDER BY cycle_id DESC LIMIT 1;"
- To get the latest Garmin stats:
  "SELECT average_stress_level, date FROM blueprint_metrics.garmin_tracker ORDER BY date DESC LIMIT 1;"

Clinical Benchmarks & Calendar Automation Rules:
- HRV < 45ms (CRITICAL RECOVERY FAILURE): If you see heavy cognitive or physical events on the calendar, insert a 60-minute non-negotiable "Critical Recovery Rest Block" ahead of them using `inject_recovery_block`. Use the current date from the garmin data and an appropriate daytime hour for the block.
- Average Stress > 65 units (SYSTEMIC AUTONOMIC OVERLOAD): Look at the schedule. Insert a 30-minute "Autonomic Reset (NSDR/Meditation)" block immediately to mitigate stress.
- If metrics are optimal or moderate, do not inject any recovery blocks. Simply provide your summary analysis.

Output Format:
Respond ONLY with two sections:
[Diagnosis]: A sharp, data-backed assessment citing specific metrics retrieved via your tool.
[Intervention]: One specific behavioral change for tonight, clearly detailing any automated Google Calendar blocks you injected.
"""

def execute_coral_sql(query: str) -> str:
    """
    DEMO BYPASS: Intercepts the SQL query and executes it against an in-memory 
    database loaded with the fresh CSVs to bypass Coral's caching.
    """
    print(f"\n[Agent Tool Call] Executing SQL (Live File Bypass):\n{query}\n")
    try:
        # Strip the schema prefix so SQLite can read the raw table names
        clean_query = query.replace("blueprint_metrics.", "")
        
        # Spin up a hyper-fast RAM database
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # 1. Load fresh Garmin Data
        cursor.execute("CREATE TABLE garmin_tracker (person_id, date, highest_energy_level, lowest_energy_level, total_recharge, average_stress_level, resting_heart_rate)")
        with open("garmin_tracker.csv", "r") as f:
            cursor.executemany("INSERT INTO garmin_tracker VALUES (?,?,?,?,?,?,?)", list(csv.reader(f))[1:])
            
        # 2. Load fresh Whoop Data
        cursor.execute("CREATE TABLE whoop_tracker (person_id, cycle_id, recovery_score, hrv_rmssd_ms, skin_temp_delta_c, day_strain, max_heart_rate)")
        with open("whoop_tracker.csv", "r") as f:
            cursor.executemany("INSERT INTO whoop_tracker VALUES (?,?,?,?,?,?,?)", list(csv.reader(f))[1:])
            
        # Execute the AI's Query
        cursor.execute(clean_query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return json.dumps(results)
    
    except Exception as e:
        # Fallback to the real Coral CLI if the local bypass fails
        try:
            result = subprocess.run(
                ["coral", "sql", query, "--format", "json"],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as err:
            return f"Error executing query: {err.stderr}"


# --- GROQ TOOL SCHEMAS & MAPPING ---
available_functions = {
    "execute_coral_sql": execute_coral_sql,
    "get_upcoming_calendar_events": get_upcoming_calendar_events,
    "inject_recovery_block": inject_recovery_block,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_coral_sql",
            "description": "Executes a raw SQL query against the local Coral data layer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute. Tables: blueprint_habits, whoop_tracker, garmin_tracker"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_upcoming_calendar_events",
            "description": "Fetches the user's scheduled Google Calendar events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_window_hours": {
                        "type": "integer",
                        "description": "Hours into the future to fetch events for. Default to 12."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "inject_recovery_block",
            "description": "Creates a new event on the Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the calendar event."
                    },
                    "start_time_iso": {
                        "type": "string",
                        "description": "Start time in strict ISO format: YYYY-MM-DDTHH:MM:SS"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Duration of the event in minutes."
                    }
                },
                "required": ["title", "start_time_iso", "duration_minutes"]
            }
        }
    }
]

def run_biohacking_agent(user_message: str):
    print("Initiating morning wearable telemetry sync...")
    generate_live_data()
    print("Wearable data successfully generated.\n")
    
    print("Agent execution loop initiated...\n")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    # The Tool Execution Loop (Allows LLM to reason, call tools, read results, and repeat)
    MAX_ITERATIONS = 5
    for attempt in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # If the LLM didn't call a tool, it means it generated the final text answer
        if not tool_calls:
            print("\n" + "="*40)
            print("FINAL PROTOCOL OUTPUT")
            print("=" * 40)
            print(response_message.content)
            break
            
        # If tools were called, append the assistant's request to memory
        messages.append(response_message)
        
        # Execute every tool requested
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            function_response = function_to_call(**function_args)
            
            # Feed the tool's output back to the LLM
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY is not set in your environment.")
        
    test_prompt = "Run my health diagnostic dashboard. I am feeling completely exhausted today and want to check if my calendar aligns with my recovery needs."
    run_biohacking_agent(test_prompt)