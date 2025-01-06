# Calendar Conversation Tracker

## Overview

The **Calendar Conversation Tracker** is a Python-based tool designed to help you monitor and analyze your interactions with external contacts over a specified period. By scraping your Google Calendar events and leveraging OpenAI's gpt-4o, this project extracts detailed information about your external attendees, including their names and company details. The final output is a comprehensive CSV file that provides insights into your networking activities.

## Features

- **Google Calendar Integration**: Scrapes calendar events within a defined date range.
- **External Attendee Extraction**: Identifies and processes external attendees from calendar events.
- **Data Enrichment with GPT-4**: Uses OpenAI's GPT-4 to extract and format names and company information from email addresses.
- **CSV Output**: Generates `calendar_events.csv` and `external_attendees.csv` for easy data analysis.

## Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.7+** installed on your machine.
- **Google Cloud Platform (GCP) Account**: To access Google Calendar API.
- **OpenAI API Key**: For processing attendee information with GPT-4.

## Scrape GCal Meetings Data

1. **Clone the Repository**

   ```
   git clone https://github.com/yourusername/calendar-conversation-tracker.git
   cd calendar-conversation-tracker

2. **Install Required Python Libraries**

    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai python-dotenv

3. **Google Calendar Scraping Setup**

	a. **Create a Google Cloud Project**

	1.	Navigate to the [Google Cloud Console] (https://console.cloud.google.com/).
	2.	Click on Select a project and then New Project
	3.	Enter a project name and click Create.
	4.	Once the project is created, go to APIs & Services > Library.
	5.	Search for Google Calendar API and click Enable.

	b. **Create OAuth 2.0 Credentials**

  	1.	In the APIs & Services section, navigate to Credentials.
	2.	Click Create Credentials > OAuth client ID.
	3.	If prompted, configure the OAuth consent screen by providing the necessary details.
	4.	Select Desktop App as the application type and click Create.
	5.	Download the credentials.json file and place it in the project root directory.

4. Fetch Calendar Events

	Run the fetch_calendar_events.py script to scrape your Google Calendar events.

	    ```
	
	    python fetch_calendar_events.py

	Steps:
	
	• Date Range Configuration: By default, the script is set to scrape events from 2010-12-01 to 2025-01-05. Modify the start_date_str and 		end_date_str variables in the script as needed.
	• Authentication: The first time you run the script, a browser window will prompt you to authorize access to your Google Calendar. This will 		generate a token.json file for future authentications.
	• Output: The script generates a calendar_events.csv file containing details of your calendar events.

## Extract Names, Company, # of Meetings

1. **OpenAI Integration**

	a. **Obtain Your OpenAI API Key**

		• Sign up or log in to your [OpenAI account], (https://platform.openai.com/signup/).
		• Navigate to the API section and generate a new API key.

	b. **Configure Environment Variables**

		• Create a .env file in the project root directory.
		• Add your OpenAI API key to the .env file:

    	```

    	OPENAI_API_KEY="your-openai-api-key-here"
 
2. Configure Internal Emails

	In the extract_external_attendees.py script, there’s a set of internal emails used to filter out your own or internal contacts. Update this list 	to include any additional internal emails you want to exclude.

4. Extract External Attendees

	Run the extract_external_attendees.py script to process the scraped calendar events and extract external attendee information.

	    ```
	
	    python extract_external_attendees.py

	Steps:

	• Environment Variables: Ensure your .env file contains the correct OPENAI_API_KEY.
	• Processing: The script reads from calendar_events.csv, filters out internal emails, and uses GPT-4 to extract names and company information.
	• Output: The script generates an external_attendees.csv file with enriched attendee details.

 
    
