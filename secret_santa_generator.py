"""
	secret_santa_generator.py

	Last edited by: Victor Chao
	Last edited on: 2/7/16	
"""

import copy
from collections import defaultdict
import random
import smtplib
import sys

"""
prompt for and get information the generator needs
from standard input

:rtype organizer_info: tuple
:rtype price_limit: str
:rtype filename: str
"""
def promptForOrganizerInfo():
	name = raw_input("Thank you for using the Secret Santa Generator.\nWhat is your name?\n")
	email = raw_input("What is your email address?\n")
	filename = raw_input("What is the name of the file containing information about the participants?\n")
	price_limit = raw_input("What is the maximum expenditure limit on a present?\n")
	organizer_info = (name, email)
	return organizer_info, price_limit, filename

"""
parse input file line by line to create a list of participants

:type filename: str
:rtype participant_list: list
"""
def createParticipantList(filename):
	participant_list = list()
	txt_file = open(filename, "r")
	for line in txt_file:
		# strip the newline character, store (name, email)
		participant_list.append(tuple(line[:-1].split(", ")))
	return participant_list

"""
check whether the list of participants has duplicates

:type li: list
:rtype : bool
"""
def listHasDuplicates(li):
	return len(li) != len(set(li))

"""
randomly pairs each participant with a gift receiver

:type participant_list: list
:rtype participant_pairs: dict
"""
def pairParticipants(participant_list):
	giver_list = participant_list
	receiver_list = copy.deepcopy(giver_list)
	participant_pairs = defaultdict(lambda:tuple())
	for giver in giver_list:
		receiver = None
		# loop until a gift receiver that is not identical
		# to the gift giver is selected
		while True:
			# randomly select a gift receiver from list
			index = random.randrange(0, len(receiver_list))
			if receiver_list[index] != giver:
				receiver = receiver_list.pop(index)
				break
		# special case when the one receiver left in list is identical
		# to the last giver
		if len(receiver_list) == 1 and giver_list[-1] == receiver_list[-1]:
			last_giver = giver_list[-1]
			# swap the last receiver with the second to the last receiver
			last_receiver = receiver
			receiver = receiver_list[-1]
			participant_pairs[giver] = receiver
			participant_pairs[last_giver] = last_receiver
			break
		else:
			participant_pairs[giver] = receiver
	return participant_pairs

"""
connect to GMail SMTP server to send out notifications to participants

:type organizer: str
:type price_limit: str
:type participant_pairs: dict
"""
def sendMailsToParticipants(organizer, price_limit, participant_pairs):
	username = "SecretSantaGenerator01"
	password = "[PASSWORD]" # not listed for security reasons
	try:
		server = smtplib.SMTP("smtp.gmail.com:587")
		server.ehlo()
		server.starttls()
		server.login(username, password)
		print "Successfully connected to SMTP server"
	except smtplib.SMTPException:
		print "Error: unable to connect to SMTP server"
	for giver, receiver in participant_pairs.iteritems():
		sendMail(server, organizer, price_limit, giver, receiver)
	server.quit()

"""
sends out notification email to a gift giver about their
corresponding receiver

:type server: SMTP
:type organizer: str
:type price_limit: str
:type giver: str
:type receiver: str
"""
def sendMail(server, organizer, price_limit, giver, receiver):
	from_addr = organizer[1]
	to_addrs = giver[1]
	subject = "Secret Santa Notification"
	body = """Dear %s,\n\nThank you for signing up to participate \
in a Secret Santa organized by %s. You've been assigned %s, and the \
maximum expenditure limit on a present is $%s. Please contact \
%s if you have any questions.\n\nBest,\nSecret Santa Generator
	""" % (giver[0], organizer[0], receiver[0], price_limit, organizer[0])
	message = """From: %s <%s>\nTo: %s <%s>\nSubject: %s\n\n%s
	""" % (organizer[0], organizer[1], giver[0], giver[1], subject, body)
	try:
		server.sendmail(from_addr, to_addrs, message)
		print "Successfully sent email"
	except smtplib.SMTPException:
		print "Error: unable to send email"

def main():
	organizer, price_limit, filename = promptForOrganizerInfo()
	participant_list = createParticipantList(filename)
	if listHasDuplicates(participant_list):
		print "The list of participants has duplicates.\n"
		sys.exit()
	participant_pairs = pairParticipants(participant_list)
	sendMailsToParticipants(organizer, price_limit, participant_pairs)

if __name__ == "__main__": 
    main()
