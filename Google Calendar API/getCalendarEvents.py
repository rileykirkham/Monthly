from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Returns list of events for the next 4 weeks
def callEvents(service, selectedDate):

	# Starts search on previous Sunday. Ends search after 4 weeks
	dayOfWeek = selectedDate.isoweekday()
	start = selectedDate - datetime.timedelta(days = dayOfWeek)
	end = (start + datetime.timedelta(weeks = 4)).isoformat() + 'Z'

	# print("Starting at ", start, " ending at ", end)

	# Rewriting firstOfMonth to be in iso format
	start = start.isoformat() + 'Z'
	return service.events().list(calendarId='primary', timeMin= start,
										timeMax = end,
										singleEvents=True, 
										orderBy='startTime').execute()

# Move search target forward by 2 weeks
def incDate(selectedDate):
	return selectedDate + datetime.timedelta(weeks = 2)

# Move search target backward by 2 weeks
def decDate(selectedDate):
	return selectedDate - datetime.timedelta(weeks = 2)


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

	# Call the Calendar API with current date equal to today's date at midnight
	currentDate = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	selectedDate = currentDate

	# TODO -- Add in calls for next month/previous month
	'''
	if(IncButtonPressed):
		selectedDate = incDate(selectedDate)
		events_result = callEvents(service, selectedDate)

	if(decButtonPressed):
		selectedDate = decDate(selectedDate)
		events_result = callEvents(service, selectedDate)

	'''

	events_result = callEvents(service, selectedDate)
	events = events_result.get('items', [])
	if not events:
		print('No upcoming events found.')
	f = open("./../CalendarLog.txt","w")
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		# Write found events to log file. Log file will be found in this file's parent folder
		f.write(start[0:10]  + " " + start[10:] + " " +event['summary'] + "\n")
		# print(start[0:10]  + " " + start[10:] + " " +event['summary'])


if __name__ == '__main__':
	main()