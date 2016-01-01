import smtplib
from collections import defaultdict

def createParticipantList(filename):
	participant_list = list()
	txt_file = open(filename, "r")
	for line in txt_file:
		participant_list.append(tuple(line[:-1].split(", ")))
	return participant_list

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
	createParticipantList("participants.dat")

if __name__ == "__main__": 
    main()