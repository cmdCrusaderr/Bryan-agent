import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Handles Google Calendar authentication and returns the service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_upcoming_calendar_events(time_window_hours: int = 12) -> str:
    """
    Fetches the user's scheduled Google Calendar events for the upcoming hours.
    Returns a string summary containing event_id, title, and times.
    """
    print(f"\n[Agent Tool Call] Fetching calendar events for next {time_window_hours} hours...")
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        time_max = (datetime.datetime.utcnow() + datetime.timedelta(hours=time_window_hours)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary', timeMin=now, timeMax=time_max,
            maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."

        result_str = "Upcoming Events:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            result_str += f"- ID: {event['id']} | Title: {event['summary']} | Starts: {start}\n"
        return result_str
    except Exception as e:
        return f"Error fetching events: {str(e)}"

def inject_recovery_block(title: str, start_time_iso: str, duration_minutes: int) -> str:
    """
    Creates a new event on the calendar.
    Format for start_time_iso: YYYY-MM-DDTHH:MM:SS
    """
    print(f"\n[Agent Tool Call] Injecting Recovery Block: {title} at {start_time_iso}...")
    try:
        service = get_calendar_service()
        start_dt = datetime.datetime.fromisoformat(start_time_iso)
        end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': title,
            'description': 'Automated Biological Recovery Block injected by AI Agent.',
            'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'colorId': '11' 
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Success: Created event '{title}'. Link: {event.get('htmlLink')}"
    except Exception as e:
        return f"Error creating event: {str(e)}"