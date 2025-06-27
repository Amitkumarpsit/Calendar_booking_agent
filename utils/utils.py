# utils/utils.py
from datetime import datetime, timedelta
import pytz
import dateparser
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your timezone here
TIMEZONE = 'Asia/Kolkata'

def parse_datetime(user_input):
    """Parse natural language datetime expressions into datetime object"""
    try:
        # Configure dateparser settings
        # pyright: ignore[reportArgumentType]  <-- Suppress Pyright warning
        settings = {
            'TIMEZONE': TIMEZONE,
            'RETURN_AS_TIMEZONE_AWARE': True,
            'PREFER_DAY_OF_MONTH': 'first',
            'PREFER_DATES_FROM': 'future'
        }

        # pyright: ignore[reportArgumentType]
        dt = dateparser.parse(user_input, settings=settings)

        if dt:
            logger.info(f"✅ Parsed '{user_input}' to {dt}")
        else:
            logger.warning(f"❌ Could not parse '{user_input}'")

        return dt

    except Exception as e:
        logger.error(f"❌ Error parsing datetime '{user_input}': {e}")
        return None


def format_datetime_for_google(dt):
    """Format datetime object to RFC3339 format required by Google Calendar"""
    if dt is None:
        return None

    # Ensure timezone awareness
    if dt.tzinfo is None:
        tz = pytz.timezone(TIMEZONE)
        dt = tz.localize(dt)

    return dt.isoformat()


def get_time_range(user_input):
    """Extract start and end time from user input"""
    try:
        user_input = user_input.lower().strip()
        logger.info(f"🕒 Parsing time range from: '{user_input}'")

        # Handle "between X and Y" format
        if 'between' in user_input and ('and' in user_input or '-' in user_input):
            parts = user_input.split('between')[1].strip()

            # Split by 'and' or '-'
            if ' and ' in parts:
                time_parts = parts.split(' and ')
            elif '-' in parts:
                time_parts = parts.split('-')
            else:
                raise ValueError("Could not parse time range")

            start_str = time_parts[0].strip()
            end_str = time_parts[1].strip()

            start_time = parse_datetime(start_str)
            end_time = parse_datetime(end_str)

            # If end time doesn't have date, use start time's date
            if start_time and end_time and end_time.date() != start_time.date():
                if end_time.time() < start_time.time():
                    end_time = end_time.replace(
                        year=start_time.year,
                        month=start_time.month,
                        day=start_time.day
                    )

        # Handle single time mentions (default 1-hour duration)
        else:
            start_time = parse_datetime(user_input)
            if start_time:
                end_time = start_time + timedelta(hours=1)
            else:
                end_time = None

        # Validate parsed times
        if start_time and end_time:
            if end_time <= start_time:
                logger.warning("⚠️ End time is not after start time, adjusting...")
                end_time = start_time + timedelta(hours=1)

            logger.info(f"✅ Final time range: {start_time} to {end_time}")
            return start_time, end_time
        else:
            logger.warning("❌ Could not parse valid time range")
            return None, None

    except Exception as e:
        logger.error(f"❌ Error getting time range: {e}")
        return None, None


def is_time_slot_available(events, start_time, end_time):
    """Check if a time slot is free based on existing events"""
    try:
        logger.info(f"🔍 Checking availability for {start_time} to {end_time}")

        for event in events:
            # Get event times
            existing_start = event['start'].get('dateTime') or event['start'].get('date')
            existing_end = event['end'].get('dateTime') or event['end'].get('date')

            if existing_start and existing_end:
                # Parse existing event times
                if 'T' in existing_start:  # DateTime format
                    existing_start = datetime.fromisoformat(existing_start.replace('Z', '+00:00'))
                    existing_end = datetime.fromisoformat(existing_end.replace('Z', '+00:00'))
                else:  # Date format (all-day events)
                    existing_start = datetime.fromisoformat(existing_start + 'T00:00:00')
                    existing_end = datetime.fromisoformat(existing_end + 'T23:59:59')

                # Check for overlap
                if start_time < existing_end and end_time > existing_start:
                    logger.warning(f"❌ Conflict found with event: {event.get('summary', 'Untitled')}")
                    return False

        logger.info("✅ Time slot is available")
        return True

    except Exception as e:
        logger.error(f"❌ Error checking availability: {e}")
        return False


def create_event_summary(user_name="User", purpose="Meeting"):
    """Generate a basic event summary"""
    timestamp = datetime.now().strftime("%m/%d")
    return f"{purpose} - {timestamp}"
