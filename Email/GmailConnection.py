import email
import imaplib
from Credentials import Credentials
import os

class GmailConnection:

    def __init__(self, credential):
        self.credential = credential
        self.imapSession = None

    def login(self):
        try:
            self.imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
            typ, accountDetails = self.imapSession.login(self.credential.username, self.credential.password)
            if typ != 'OK':
                raise imaplib.IMAP4.error("Could not login to the email account.")
            self.imapSession.select('[Gmail]/All Mail')
        except:
            raise imaplib.IMAP4.error("Could not login to the email account.")

    def getMessagesSinceUID(self, uid):
        try:
            typ, data = self.imapSession.uid("SEARCH", "UID", str(uid) + ":*")
            if typ != 'OK':
                raise imaplib.IMAP4.error("Could not retrieve new messages.")
            return data[0].split()
        except:
            raise imaplib.IMAP4.error("Could not retrieve new messages.")

    def getAttachmentsFromMessage(self, uid, extensions=None):
        attachments = []
        try:
            typ, messageParts = self.imapSession.uid("FETCH", uid, '(RFC822)')
            if typ != 'OK':
                raise

            emailBody = messageParts[0][1]
            mail = email.message_from_string(emailBody)
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                fileName = part.get_filename()

                if bool(fileName):
                    extension = os.path.splitext(fileName)[1][1:].lower()
                    if extensions is None or extension in extensions:
                        attachments.append(part)
        except Exception, e:
            print e
            raise imaplib.IMAP4.error("Could not get attachment.")
        return attachments

    def logout(self):
        self.imapSession.close()
        self.imapSession.logout()