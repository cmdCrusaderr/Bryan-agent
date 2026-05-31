import datetime
from calendar_tools import inject_recovery_block

def seed_demo_schedule():
    # Dynamically calculate today's date and the current hour
    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_hour = now.hour
    
    print(f"Seeding today's ({today_str}) testing schedule into Google Calendar over the next 12 hours...")
    
    # We define relative offsets (in hours) from the current time to space them out naturally
    tasks = [
        {
            "title": "🏃‍♂️ Morning Run & Base Cardio" if current_hour < 12 else "🏃‍♂️ Evening Run & Base Cardio",
            "hour_offset": 0,  # Starts immediately
            "duration_minutes": 45
        },
        {
            "title": "📚 Deep Work: Coding & Tech Study",
            "hour_offset": 2,  # Starts 2 hours from now
            "duration_minutes": 90
        },
        {
            "title": "🥦 Grocery Run & Meal Prep",
            "hour_offset": 5,  # Starts 5 hours from now
            "duration_minutes": 45
        },
        {
            "title": "🏋️‍♂️ Hypertrophy & Calisthenics Training",
            "hour_offset": 7,  # Starts 7 hours from now
            "duration_minutes": 60
        },
        {
            "title": "📖 Reading Book & Script Review",
            "hour_offset": 10, # Starts 10 hours from now
            "duration_minutes": 45
        }
    ]
    
    for task in tasks:
        # Calculate the dynamic start time for each task based on the current time
        task_start_time = now + datetime.timedelta(hours=task["hour_offset"])
        start_time_iso = task_start_time.strftime("%Y-%m-%dT%H:%M:00")
        
        try:
            inject_recovery_block(
                title=task["title"],
                start_time_iso=start_time_iso,
                duration_minutes=task["duration_minutes"]
            )
            print(f"Successfully injected: {task['title']} at {task_start_time.strftime('%I:%M %p')}")
        except Exception as e:
            print(f"Failed to inject {task['title']}: {e}")

if __name__ == "__main__":
    seed_demo_schedule()