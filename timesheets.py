import requests
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pytz
import json

def to_unix_timestamp(date_obj):
    # Get the Europe/Lisbon timezone
    tz = pytz.timezone('Europe/Lisbon')

    # Localize the date to the specified timezone, assuming the time is at the start of the day
    localized_dt = tz.localize(datetime.combine(date_obj, datetime.min.time()), is_dst=None)  # Combine date with default time

    # Convert localized datetime to Unix timestamp in milliseconds
    unix_timestamp = int(localized_dt.timestamp() * 1000)  # Convert to milliseconds
    return unix_timestamp

# Daily button

def daily_post():

    # Get input data from the GUI
    duration = "15"
    description = "Daily"
    
    # Correctly parse the date selected from the calendar
    date_obj = datetime.today()
    date_obj += timedelta(days=1)
    timestamp = to_unix_timestamp(date_obj)  # Convert to Unix timestamp

    selected_tag = tag_var.get()  # Get the selected tag value from the dropdown
    
    # Data to send to YouTrack API
    data = {
        "duration": { "minutes": int(duration) },  # Example: 120 minutes (2 hours)
        "date": timestamp,  # Unix timestamp in milliseconds
        "text": description,  # Work description
        "issue": {
            "idReadable": "Weezie-282"  # Issue ID or key
        },
        "type": {
            "id": "66-7"  # Tag/type (e.g., "66-7" for "Meeting")
        }
    }

    return send_post_request(data)

def dev_meeting_post():

    # Get input data from the GUI
    duration = "60"
    description = "Dev Meeting"
    
    # Correctly parse the date selected from the calendar
    date_obj = datetime.today()
    date_obj += timedelta(days=1)
    timestamp = to_unix_timestamp(date_obj)  # Convert to Unix timestamp

    selected_tag = tag_var.get()  # Get the selected tag value from the dropdown
    
    # Data to send to YouTrack API
    data = {
        "duration": { "minutes": int(duration) },  # Example: 120 minutes (2 hours)
        "date": timestamp,  # Unix timestamp in milliseconds
        "text": description,  # Work description
        "issue": {
            "idReadable": "Weezie-282"  # Issue ID or key
        },
        "type": {
            "id": "66-7"  # Tag/type (e.g., "66-7" for "Meeting")
        }
    }

    return send_post_request(data)

def issue_post():

    # Get input data from the GUI
    duration = duration_input.get()
    description = description_input.get()
    selected_date = cal.get_date()  # Get the date from the calendar widget (mm/dd/yy format)
    
    # Correctly parse the date selected from the calendar
    date_obj = datetime.strptime(selected_date, "%m/%d/%y")  # Convert to datetime object
    date_obj += timedelta(days=1)
    timestamp = to_unix_timestamp(date_obj)  # Convert to Unix timestamp

    selected_tag = tag_var.get()  # Get the selected tag value from the dropdown
    
    # Data to send to YouTrack API
    data = {
        "duration": { "minutes": int(duration) },  # Example: 120 minutes (2 hours)
        "date": timestamp,  # Unix timestamp in milliseconds
        "text": description,  # Work description
        "issue": {
            "idReadable": "Weezie-282"  # Issue ID or key
        },
        "type": {
            "id": selected_tag  # Tag/type (e.g., "66-7" for "Meeting")
        }
    }

    return send_post_request(data)

# Define the function to send POST request to YouTrack
def send_post_request(data):
    url = "https://weezie.myjetbrains.com/api/issues/Weezie-282/timeTracking/workItems"  # Your YouTrack API endpoint
    headers = {
        "Authorization": "Bearer perm:c2FuZHJvLmFsdmVz.NTAtMzk=.cCdFEaLSjdquMTBse3z8WHgrF0f9Co",  # Replace with your API token
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:  # Successfully created
            messagebox.showinfo("Success", f"Time entry posted successfully!")
        else:
            messagebox.showerror("Error", f"Failed to post time entry. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



# Tkinter GUI
root = Tk()
root.title("YouTrack Time Entry")

# Label and input for duration (in minutes)
Label(root, text="Duration (minutes):").pack(pady=5)
duration_input = Entry(root)
duration_input.pack(pady=5)

# Label and input for description
Label(root, text="Description:").pack(pady=5)
description_input = Entry(root)
description_input.pack(pady=5)

# Label and calendar date picker
Label(root, text="Date:").pack(pady=5)
timezone = pytz.timezone('Africa/Abidjan')
cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
cal.pack(pady=10)

# Dropdown for tag/type (Meeting with value 66-7)
Label(root, text="Tag/Type:").pack(pady=5)
tag_var = StringVar(root)
tag_var.set("66-7")  # Default value for "Meeting"
options = {"Meeting": "66-7"}  # Tag options
tag_menu = OptionMenu(root, tag_var, *options.values())  # Only one option now, but can expand later
tag_menu.pack(pady=5)

# Post button
post_button = Button(root, text="Issue Time Track", command=issue_post, padx=20, pady=10)
post_button.pack(pady=10)

daily_button = Button(root, text="Daily Time Track", command=daily_post, padx=20, pady=10)
daily_button.pack(pady=10)

daily_button = Button(root, text="Dev Weekly", command=dev_meeting_post, padx=20, pady=10)
daily_button.pack(pady=10)

root.mainloop()
