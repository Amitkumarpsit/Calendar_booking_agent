from googleapiclient.discovery import build

API_KEY = "AIzaSyDupBf7W7ZcaGhNtuuzD6MasHoQqQ2m31o"
CALENDAR_ID = 'your-public-calendar-id@group.calendar.google.com'

def get_calendar_service():
    """Create and return Google Calendar service object using API key (public read-only)"""
    service = build('calendar', 'v3', developerKey=API_KEY)
    return service

def check_availability(time_min, time_max):
    """Check calendar availability for given time range (public calendars only)"""
    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    except Exception as e:
        print(f"Error checking availability: {e}")
        raise
