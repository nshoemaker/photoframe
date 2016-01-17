import email
import imaplib2 as imaplib
from Credentials import Credentials
import os
from threading import *
import thread

class GmailConnection:

    def __init__(self, credential):
        self.credential = credential
        self.imapSession = None

    def _login(self):
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
            self._login()
            typ, data = self.imapSession.uid("SEARCH", "UID", bytearray(str(uid) + ":*"))
            if typ != 'OK':
                raise imaplib.IMAP4.error("Could not retrieve new messages.")
            allIds = data[0].split()
            if len(allIds) != 0 and int(allIds[0]) < uid:
                return allIds[1:]
            return allIds
        except imaplib.IMAP4.error:
            raise
        except Exception, e:
            raise imaplib.IMAP4.error("Could not retrieve new messages.")
        finally:
            self._logout()

    def getAttachmentsFromMessage(self, uid, extensions=None):
        attachments = []
        try:
            self._login()
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
        except imaplib.IMAP4.error:
            raise
        except Exception, e:
            raise imaplib.IMAP4.error("Could not get attachment.")
        finally:
            self._logout()
        return attachments

    def waitForMessage(self, event, callback):
        try:
            self._login()
            self.imapSession.idle(callback=callback)
            event.wait()
            event.clear()
        except Exception, e:
            print e
        finally:
            self._logout()

    def _logout(self):
        try:
            self.imapSession.close()
            self.imapSession._logout()
        except:
            return
