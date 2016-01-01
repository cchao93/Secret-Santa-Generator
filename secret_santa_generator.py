import smtplib
from collections import defaultdict
import copy
import random

def createParticipantList(filename):
	participant_list = list()
	txt_file = open(filename, "r")
	for line in txt_file:
		participant_list.append(tuple(line[:-1].split(", ")))
	return participant_list

def pairParticipants(participant_list):
	giver_list = participant_list
	receiver_list = copy.deepcopy(giver_list)
	participant_pairs = defaultdict(lambda:tuple())

	for giver in giver_list:
		receiver = None
		while True:
			index = random.randrange(0, len(receiver_list))
			if receiver_list[index] != giver:
				receiver = receiver_list[index]
				receiver_list.remove(receiver)
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

def sendMails():
	from_addr = "vcchao93@gmail.com"
	to_addrs = ["victorchao666@gmail.com"]

	message = """From: Victor Chao <vcchao93@gmail.com>
	To: To Person <victorchao666@gmail.com>
	Subject: SMTP e-mail test

	This is a test e-mail message.
	"""

	username = "vcchao93"
	password = "PASSWORD"

	try:
		server = smtplib.SMTP("smtp.gmail.com:587")
		#server.ehlo()
		server.starttls()
		server.login(username, password)
		server.sendmail(from_addr, to_addrs, message)
		server.quit()
		print "Successfully sent email"
	except smtplib.SMTPException:
		print "Error: unable to send email"

def main():
	participant_list = createParticipantList("participants.dat")
	participant_pairs = pairParticipants(participant_list)

if __name__ == "__main__": 
    main()