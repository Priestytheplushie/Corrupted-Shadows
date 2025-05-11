from pypresence import Presence
import time

start_time = int(time.time())

CLIENT_ID = "1370901239671296052"  # Replace with your Discord application's Client ID
rpc = Presence(CLIENT_ID)

def connect_to_discord():
    """Connect to Discord Rich Presence."""
    try:
        rpc.connect()
        print("Connected to Discord Rich Presence.")
    except Exception as e:
        print(f"Failed to connect to Discord: {e}")

from pypresence import Presence
import time

CLIENT_ID = "1370901239671296052"  # Replace with your Discord application's Client ID
rpc = Presence(CLIENT_ID)

def connect_to_discord():
    """Connect to Discord Rich Presence."""
    try:
        rpc.connect()
    except Exception as e:
        print(f"Failed to connect to Discord: {e}")

def update_presence(state, details, large_image="priesty", large_text="Corrupted Shadows"):
    """
    Update the Discord Rich Presence dynamically.

    Args:
        state (str): The current state of the player (e.g., "In the Tower").
        details (str): Additional details about the player's activity.
        large_image (str): The key for the large image asset in Discord.
        large_text (str): The text displayed when hovering over the large image.
    """
    try:
        rpc.update(
            details=state,  # Swapped because of custom logic
            state=details,  # Swapped because of custom logic
            large_image=large_image,
            large_text=large_text,
            start=start_time  # Use the global start time
        )
    except Exception as e:
        print(f"Failed to update Discord Rich Presence: {e}")

def disconnect_from_discord():
    """Disconnect from Discord Rich Presence."""
    try:
        rpc.close()
    except Exception as e:
        print(f"Failed to disconnect from Discord: {e}")

def disconnect_from_discord():
    """Disconnect from Discord Rich Presence."""
    try:
        rpc.close()
    except Exception as e:
        print(f"Failed to disconnect from Discord: {e}")