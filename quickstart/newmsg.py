from __future__ import print_function
from apiclient import errors
import pickle
import os.path
import httplib2
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import email
import base64
import json
import re


from quickstart.detector import *


def main456():

	#r=requests.get("https://www.googleapis.com/gmail/v1/users/userId/messages")
	#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
	SCOPES= ['https://mail.google.com']
	user_id = "bhanushalianj@gmail.com"


	creds = None
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
			'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	#GMAIL = build('gmail','v1',http=creds.authorize(Http()))
	#threads = GMAIL.users().threads.list(userId='me').execute().get('threads',[])
	#service = build('gmail', 'v1', http=creds.authorize(Http())#credentials=creds)
	service = build('gmail', 'v1', credentials=creds)
	results = service.users().labels().list(userId='me').execute()
	labels = results.get('labels', [])
	#messageheader= service.users().messages().get(userId="me", id=emails["id"], format="full", metadataHeaders=None).execute()

		# Call the Gmail API
		#results = service.users().labels().list(userId='me').execute()
		#labels = results.get('labels', [])

	def ListMessagesMatchingQuery(service, user_id,query=''):
		try:
			response = service.users().messages().list(userId=user_id,q=query).execute()
			messages = []
			if 'messages' in response:
				messages.extend(response['messages'])
			while 'nextPageToken' in response:
				page_token = response['nextPageToken']
				response = service.users().messages().list(userId=user_id,q=query,pageToken=page_token).execute()

				messages.extend(response['messages'])

			return messages
		except errors.HttpError as error:
			print ('An error occured: %s' % error)

	def ListMessagesWithLabels(service,user_id,label_ids=[]):
		try:
			response = service.users().messages().list(userId=user_id,labelIds=label_ids).execute()

			messages = []
			if 'messages' in response:
				messages.extend(response['messages'])

			while 'nextPageToken' in response:
				page_token = response['nextPageToken']
				response = service.users().messages().list(userId=user_id,labelIds=label_ids,pageToken=page_token).execute()

				messages.extend(response['messages'])

			return messages
		except errors.HttpError as error:
			print ('An error occured: %s' % error)

	def GetMessage(service, user_id, msg_id):
		try:
			message=service.users().messages().get(userId=user_id,id=msg_id,format='raw').execute()
			"""
			#m=email.encoders_encode_base64(message['raw'])
			msg_str = base64.urlsafe_b64decode(message['raw'])
			b= email.message_from_string(msg_str)
			body=""
			
			if b.is_multipart:
				for part in b.walk():
					ctype=part.get_content_type()
					cdispo=str(part.get('Content-Disposition'))
					
					if cdispo == 'text/plain' and attachment not in cdispo:
						body = part.get_payload(decode=True)
						break
			else:
				body=b.get_payload(decode=True)
			"""
			return message
		except errors.HttpError as error:
			print("an error is occures %s"% error)

	def GetMimeMessage(service, user_id, msg_id):



		try:
			message = service.users().messages().get(userId=user_id,id=msg_id,format='raw').execute()
			#print('Message snippet: %s' % message['snippet'])
			msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
			mime_msg = email.message_from_bytes(msg_str)
			messageMainType = mime_msg.get_content_maintype()
			if messageMainType == 'multipart':
				for part in messageMainType:
					if part.get_content_maintype() == 'text':
						return part.get_payload(decode=True)
				return " "
			elif messageMainType == 'text':
				return mime_msg.get_payload(decode=True)
			#return mime_msg


		except errors.HttpError as error:
			print ('An error occurred: %s' % error)



	matchedmessage = ListMessagesMatchingQuery(service,user_id,query='')
	labeledmessage = ListMessagesWithLabels(service,user_id,label_ids=[])

	#msg_id="1707d50a9a060b39"
	j=0
	dict=[]
	spam_dic=[]
	ham_id=1
	spam_id=1
	for inboxmessage in matchedmessage:

		msg_id=inboxmessage['id']
		getmessage = GetMessage(service, user_id, msg_id)
		messageheader= service.users().messages().get(userId="me", id=msg_id, format="full", metadataHeaders=None).execute()
		headers=messageheader["payload"]["headers"]
		#file=messageheader["payload"]["parts"]["headers"]
		subject= [i['value'] for i in headers if i["name"] == "Subject"]
		from_=[i['value'] for i in headers if i["name"]=="From"]
		#attachment=[i['value'] for i in file if i["name"] == "Content-Disposition"]
		#print('Message Id: %s' % inboxmessage['id'])
		#print('From: %s'% from_)
		#print('Subject: %s '% subject)
		#print('Message snippet: %s' % getmessage['snippet'])
		#print('Lable Id: %s ' % getmessage['labelIds'])
		#msgid=int(msg_id)
		msgid=msg_id
		FromToString = ''.join(map(str,from_))
		FromToString = re.sub('<.*?>', '', FromToString)
		SubjectToString = ''.join(map(str,subject))
		snippet=getmessage['snippet']
		check_lable=detect(snippet)
		getmessage['labelIds'].append(check_lable)
		#print('Lable Id: %s ' % getmessage['labelIds'])

		for x in getmessage['labelIds']:
			if x == 'Not Spam' :
				#print("this is ham")
				dict.append({
					"id":ham_id,
					"msg_id":msgid,
					"isImportant":False,
					"picture":"https//api.androidhive.info/json/google.png",
					"from":FromToString,
					"subject":SubjectToString,
					"message":getmessage['snippet'],
					"timestamp":"10:30 AM",
					"isRead":False
				})
				ham_id+=1

			elif x == 'Spam!' :
				#print("this is spam")
				spam_dic.append({
					"id":spam_id,
					"msg_id":msgid,
					"isImportant":False,
					"picture":"https//api.androidhive.info/json/google.png",
					"from":FromToString,
					"subject":SubjectToString,
					"message":getmessage['snippet'],
					"timestamp":"10:30 AM",
					"isRead":False
				})
				spam_id+=1
		"""
		dict.append({
			"id":msgid,
			"isImportant":False,
			"picture":"https//api.androidhive.info/json/google.png",
			"from":FromToString,
			"subject":SubjectToString,
			"message":getmessage['snippet'],
			"timestamp":"10:30 AM",
			"isRead":False
		})
		"""
		j_object=json.dumps(dict,indent=4)
		spamj_object=json.dumps(spam_dic,indent=4)
		#print(j_object)

		with open ("person.json","w") as fp:
			fp.write(j_object)
			fp.close()
		"""
		#file_path = "https://spam-message-detection.000webhostapp.com/file.json"
		resp = requests.post("https://spam-message-detection.000webhostapp.com/file.json",json=spamj_object)
		"""
		with open ("spam_person.json","w") as spamfp:
			spamfp.write(spamj_object)
			spamfp.close()




		#print('%s'%attachment)
		#if attachment:
		#	print('%s' % attachment)
		#print("\n\n")

		j+=1
		if j == 10:
			break

	#getmessage = GetMessage(service, user_id, msg_id)

	#for getmessages in getmessage:'1707de2791bb8d2d','1707d50a9a060b39',
	#print(getmessage)


if __name__ == '__main456__':
	main456()
