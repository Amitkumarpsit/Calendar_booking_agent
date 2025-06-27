# agent/agent.py
from utils.calendar_api import check_availability, book_event
from utils.utils import get_time_range, is_time_slot_available, create_event_summary, format_datetime_for_google
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_input(user_input):
    """Process user input and handle calendar booking"""
    logger.info(f"📝 User input received: {user_input}")

    # Parse time from user input
    try:
        start_time, end_time = get_time_range(user_input)
        logger.info(f"🕒 Parsed time range: {start_time}, {end_time}")
    except Exception as e:
        logger.error(f"❌ Time parsing error: {e}")
        return "⛔ Sorry, I couldn't understand the time you mentioned. Please try again with a more specific time like 'tomorrow at 3 PM' or 'Monday at 2 PM'."

    if start_time is None or end_time is None:
        logger.warning("❌ Time could not be parsed.")
        return "⛔ Sorry, I couldn't understand the time you mentioned. Please try again with a more specific time like 'tomorrow at 3 PM'."

    try:
        logger.info("🔎 Checking calendar availability...")
        events = check_availability(
            format_datetime_for_google(start_time), 
            format_datetime_for_google(end_time)
        )
        logger.info(f"📅 Calendar events fetched: {len(events)} events found")

        if is_time_slot_available(events, start_time, end_time):
            logger.info("✅ Slot available, booking now...")
            event = book_event(
                create_event_summary(),
                format_datetime_for_google(start_time),
                format_datetime_for_google(end_time)
            )
            logger.info("📌 Booking confirmed")
            return f"✅ Your meeting has been successfully booked for {start_time.strftime('%B %d, %Y at %I:%M %p')}!"
        else:
            logger.warning("❌ Slot not available.")
            return "⛔ Sorry, that time slot is not available. Please suggest another time."

    except Exception as e:
        logger.error(f"⚠️ Backend processing error: {e}")
        return f"⚠️ Server encountered an error: {str(e)}. Please try again later."


