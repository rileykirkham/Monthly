from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def last_day_of_month(any_day):
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

# Returns list of events for this month.
def callEvents(service, selectedDate):
	firstOfMonth = datetime.datetime(selectedDate.year, selectedDate.month, 1).isoformat() + 'Z'# 'Z' indicates UTC time
	lastOfMonth = last_day_of_month(firstOfMonth).isoformat() + 'Z'# 'Z' indicates UTC time
	return service.events().list(calendarId='primary', timeMin= firstOfMonth,
                                        timeMax = lastOfMonth,
                                        singleEvents=True, 
                                        orderBy='startTime').execute()

def incMonth(selectedDate):
	# If December, move to next year
	if(selectedDate.month == 12):
		newYear = selectedDate.year + 1
		newMonth = 1
	else:
		newYear = selectedDate.year
		newMonth = selectedDate.month + 1
	return selectedDate.replace(year = newYear, month = newMonth)
		
def decMonth(selectedDate):
	# If January, move to prev year
	if(selectedDate.month == 1):
		newYear = selectedDate.year - 1
		newMonth = 12
	else:
		newYear = selectedDate.year
		newMonth = selectedDate.month - 1
	return selectedDate.replace(year = newYear, month = newMonth)


def main():
   # Returns a list of user's events for the current month.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    currentDate = datetime.datetime.utcnow()
    selectedDate = currentDate

    # TODO -- Add in calls for next month/previous month
    '''
	if(IncButtonPressed):
		selectedDate = incMonth(selectedDate)
	if(decButtonPressed):
		selectedDate = decMonth(selectedDate)
    '''


    print("Getting events in " + selectedDate.strftime("%B"))
    
    events_result = callEvents(service, selectedDate)
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()