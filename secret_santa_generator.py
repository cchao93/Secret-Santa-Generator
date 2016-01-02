import smtplib
from collections import defaultdict
import copy
import random
import sys

def promptForOrganizerInfo():
	name = raw_input("Thank you for using the Secret Santa Generator.\nWhat is your name?\n")
	email = raw_input("What is your email address?\n")
	filename = raw_input("What is the name of the file containing information about the participants?\n")
	price_limit = raw_input("What is the maximum expenditure limit on a present?\n")
	organizer_info = (name, email)
	return organizer_info, price_limit, filename

def createParticipantList(filename):
	participant_list = list()
	txt_file = open(filename, "r")
	for line in txt_file:
		participant_list.append(tuple(line[:-1].split(", ")))
	return participant_list

def listHasDuplicates(li):
	return len(li) != len(set(li))

def pairParticipants(participant_list):
	giver_list = participant_list
	receiver_list = copy.deepcopy(giver_list)
	participant_pairs = defaultdict(lambda:tuple())

	for giver in giver_list:
		receiver = None
		while True:
			index = random.randrange(0, len(receiver_list))
			if receiver_list[index] != giver:
				receiver = receiver_list.pop(index)
				break
		if len(receiver_list) == 1 and giver_list[-1] == receiver_list[-1]:
			last_giver = giver_list[-1]
			last_receiver = receiver
			receiver = receiver_list[-1]
			participant_pairs[giver] = receiver
			participant_pairs[last_giver] = last_receiver
			break
		else:
			participant_pairs[giver] = receiver
	print participant_pairs
	return participant_pairs

def sendMailsToParticipants(organizer, price_limit, participant_pairs):
	username = "vcchao93"
	password = "victor15334c"
	try:
		server = smtplib.SMTP("smtp.gmail.com:587")
		#server.ehlo()
		server.starttls()
		server.login(username, password)
		print "Successfully connected to SMTP server"
	except smtplib.SMTPException:
		print "Error: unable to connect to SMTP server"
	for giver, receiver in participant_pairs.iteritems():
		sendMail(server, organizer, price_limit, giver, receiver)
	server.quit()

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