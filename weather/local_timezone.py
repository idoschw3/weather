import streamlit as st
from streamlit.components.v1 import html
from datetime import datetime
import pytz


def get_user_timezone():
    # JavaScript code to get timezone
    timezone_js = """
    <script>
    // Get timezone info
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const offset = new Date().getTimezoneOffset();

    // Format offset as +HH:MM or -HH:MM
    const offsetHours = Math.abs(Math.floor(offset / 60));
    const offsetMinutes = Math.abs(offset % 60);
    const offsetSign = offset > 0 ? '-' : '+';
    const formattedOffset = `${offsetSign}${offsetHours.toString().padStart(2, '0')}:${offsetMinutes.toString().padStart(2, '0')}`;

    // Send data back to Streamlit
    window.parent.postMessage({
        type: 'timezone_info',
        timezone: timezone,
        offset: formattedOffset
    }, '*');
    </script>
    """

    # Create a container for timezone info
    timezone_container = st.empty()

    # JavaScript callback handler
    handle_js = """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'timezone_info') {
            // Send to Streamlit
            const data = {
                timezone: event.data.timezone,
                offset: event.data.offset
            };
            // Store the data in Streamlit's session_state
            setComponentValue(data);
        }
    });
    </script>
    """

    # Combine JavaScript code
    component = html(timezone_js + handle_js, height=0)

    return component


def main():
    st.title("Timezone Detector")

    # Get timezone component
    timezone_info = get_user_timezone()

    if timezone_info:
        st.write(f"Your timezone: {timezone_info['timezone']}")
        st.write(f"UTC offset: {timezone_info['offset']}")


if __name__ == "__main__":
    main()