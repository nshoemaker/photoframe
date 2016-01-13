import email
import imaplib
from Credentials import Credentials

class GmailConnection:

	def __init__(self, credential):
		self.credential = credential

	def login(self):
		try:
			imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
			typ, accountDetails = imapSession.login(self.credential.username, self.credential.password)
			if typ != 'OK':
				raise imaplib.IMAP4.error("Could not login to the email account.")
		except:
			raise imaplib.IMAP4.error("Could not login to the email account.")