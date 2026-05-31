# Bryan AI

## What is it about?
Bryan AI is an autonomous scheduling agent that monitors your physical recovery. Instead of relying on restricted wearable APIs, it acts locally to read your raw exported health data (like Whoop or Garmin stats). It analyzes your sleep, stress, and daily habits. If it detects that your nervous system is strained, it automatically connects to your Google Calendar and schedules a mandatory recovery block into an open time slot before your next heavy task.

## Tech Stack
* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **AI / LLM:** Groq API (Llama 3)
* **Data Layer:** SQLite (Simulating the Coral Data Layer for on-the-fly SQL joins across multiple local CSV files)
* **Integrations:** Google Calendar API

## Output
When you run the main agent script, it produces two distinct outputs:
1. **Terminal Analysis:** An AI-generated text summary explaining exactly how your recent lifestyle habits (e.g., screen time, sleep quality) are currently affecting your resting vitals (like HRV).
2. **Calendar Automation:** A physical "Autonomic Reset" event automatically booked into a free time slot on your live Google Calendar to ensure you recover.
<img width="1225" height="611" alt="Screenshot 2026-05-31 at 21 30 58" src="https://github.com/user-attachments/assets/be8d71c3-fefd-46e1-b682-548d66148977" />
