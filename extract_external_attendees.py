import csv
import openai
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

def get_company_info_from_domain(domain: str) -> (str, str):
    """
    Turn a domain into a readable company name, plus return a website URL.
    """
    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that extracts a human-readable company name from a domain. "
                "Provide only the short company name, with normal spacing, no punctuation or extra text.\n"
                "Examples:\n"
                "'water.ventures' -> 'Water Ventures'\n"
                "'alaskacapital.com' -> 'Alaska Capital'"
            )
        },
        {
            "role": "user",
            "content": domain
        }
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=prompt_messages,
            max_tokens=40,
            temperature=0.0
        )
        company_name_raw = response.choices[0].message.content.strip()
        if not company_name_raw:
            company_name_raw = domain.split('.')[0].title()
    except Exception:
        company_name_raw = domain.split('.')[0].title()

    website = f"https://{domain}/"
    return company_name_raw, website

def get_name_from_email(email: str) -> (str, str, str):
    """
    Extract first/last name from an email. Return (first_name, last_name, full_name).
    Use 'NA' if unknown.
    """
    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that extracts names from email addresses. "
                "Return exactly three values separated by '|': first_name|last_name|full_name\n"
                "Use 'NA' when a component cannot be determined with confidence.\n"
                "Examples:\n"
                "jeff@xadvisors.com -> Jeff|NA|NA\n"
                "sam.altman@openai.com -> Sam|Altman|Sam Altman\n"
            )
        },
        {
            "role": "user",
            "content": email
        }
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=prompt_messages,
            max_tokens=60,
            temperature=0.0
        )
        result = response.choices[0].message.content.strip()
        parts = result.split('|')
        if len(parts) != 3:
            return "NA", "NA", "NA"
        return parts[0].strip(), parts[1].strip(), parts[2].strip()
    except Exception:
        return "NA", "NA", "NA"

def main():
    # Set of internal emails to skip
    internal_emails = {
        "email1@gmail.com",
        "emaile2@gmail.com"
    }

    external_info = {}

    # Read all rows first so we can show progress
    with open("calendar_events.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)  # convert reader to a list
        total_rows = len(rows)

    # Now iterate again, showing progress
    with open("calendar_events.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):
            print(f"Processing row {i} of {total_rows}...")

            end_date_str = row.get("End", "")
            try:
                dt_obj = datetime.fromisoformat(end_date_str.replace("Z", ""))
                end_date_formatted = dt_obj.date().isoformat()
            except ValueError:
                continue

            attendees_str = row.get("Attendees", "")
            attendees_list = [a.strip() for a in attendees_str.split(",") if a.strip()]

            for email in attendees_list:
                email_lower = email.lower()
                if email_lower in internal_emails:
                    continue

                if email_lower not in external_info:
                    domain_part = email_lower.split("@")[-1]
                    company_name, website = get_company_info_from_domain(domain_part)

                    first_name, last_name, full_name = get_name_from_email(email_lower)

                    external_info[email_lower] = {
                        "date": end_date_formatted,
                        "company": company_name,
                        "website": website,
                        "first_name": first_name,
                        "last_name": last_name,
                        "full_name": full_name,
                        "meeting_count": 1  # Start the count at 1
                    }
                else:
                    # Update the last meeting date if the new one is later
                    existing_date_str = external_info[email_lower]["date"]
                    if end_date_formatted > existing_date_str:
                        external_info[email_lower]["date"] = end_date_formatted

                    # Increment the meeting count
                    external_info[email_lower]["meeting_count"] += 1

    # Write the results to a new CSV
    with open("external_attendees.csv", mode="w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "Email",
            "FirstName",
            "LastName",
            "FullName",
            "LastMeetingDate",
            "CompanyName",
            "Website",
            "MeetingCount"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for email, data in external_info.items():
            row_data = {
                "Email": email,
                "FirstName": data["first_name"],
                "LastName": data["last_name"],
                "FullName": data["full_name"],
                "LastMeetingDate": data["date"],
                "CompanyName": data["company"],
                "Website": data["website"],
                "MeetingCount": data["meeting_count"]
            }
            
            writer.writerow(row_data)

    print("Done! External attendee data (including meeting counts) has been written to 'external_attendees.csv'.")

if __name__ == "__main__":
    main() 