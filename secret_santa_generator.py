import smtplib

fromaddr = "vcchao93@gmail.com"
toaddrs = ["victorchao666@gmail.com"]

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
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	print "Successfully sent email"
except smtplib.SMTPException:
	print "Error: unable to send email"