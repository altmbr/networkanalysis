import os
import csv
import datetime
from datetime import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    # Prompt user for date range
    start_date_str = "2010-12-01"
    end_date_str = "2025-01-05"

    try:
        start_datetime = dt.strptime(start_date_str, "%Y-%m-%d")
        end_datetime = dt.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("Please enter valid date formats (YYYY-MM-DD).")
        return

    # Convert to RFC3339 format by appending time and converting to ISO 8601 if needed.
    # We'll collect all events from the start of the selected day to the end of that end_date.
    time_min = start_datetime.isoformat() + 'Z'
    # Add one day to end_date to include all events on that date as well
    time_max = (end_datetime + datetime.timedelta(days=1)).isoformat() + 'Z'

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save thce credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Specify the Calendar ID
    calendar_id = 'INSERTEMAIL@gmail.com'

    # Collect events with pagination
    all_events = []
    page_token = None

    while True:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            pageToken=page_token  # Use the token from the previous iteration
        ).execute()

        events = events_result.get('items', [])
        all_events.extend(events)

        page_token = events_result.get('nextPageToken')  # Retrieve token for the next page
        if not page_token:
            # No more pages
            break

    # Prepare CSV
    with open('calendar_events.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Description', 'Start', 'End', 'Attendees']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        if not all_events:
            print("No events found in this range.")
        else:
            for event in all_events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                summary = event.get('summary', '(No Title)')
                description = event.get('description', '')
                attendees = []
                if 'attendees' in event:
                    for attendee in event['attendees']:
                        attendees.append(attendee.get('email', ''))

                writer.writerow({
                    'Title': summary,
                    'Description': description,
                    'Start': start,
                    'End': end,
                    'Attendees': ', '.join(attendees)
                })

    print("CSV file 'calendar_events.csv' has been created with the events data.")

if __name__ == '__main__':
    main() 