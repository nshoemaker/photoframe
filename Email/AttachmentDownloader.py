from Credentials import Credentials
from GmailConnection import GmailConnection
import thread
import os
import time

class AttachmentDownloader:
    LAST_UID_FILE = "meta.txt"

    def __init__(self, credentials, pollingInterval, attachmentsDirectory):
        self.emailConnection = GmailConnection(credentials)
        self.pollingInterval = pollingInterval
        self.lastUid = -1
        self.attachmentsDirectory = attachmentsDirectory
        if not os.path.exists(attachmentsDirectory):
            os.mkdir(attachmentsDirectory)
        thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            messageIds = []
            try:
                messageIds = self.emailConnection.getMessagesSinceUID(self.getNextUid())
            except Exception, e:
                print e

            try:
                print messageIds
                for uid in messageIds:
                    print uid
                    atts = self.emailConnection.getAttachmentsFromMessage(uid, ["png", "jpg", "jpeg", "gif"])
                    for att in atts:
                        fileName = att.get_filename()
                        filePath = os.path.join(self.attachmentsDirectory, uid + "_" + fileName)
                        fp = open(filePath, 'wb')
                        fp.write(att.get_payload(decode=True))
                        fp.close()
                    self.setLastUid(uid)
            except Exception, e:
                print e

            time.sleep(self.pollingInterval)


    def setPollingInterval(self, interval):
        self.pollingInterval = interval

    def getpollingInterval(self):
        return self.pollingInterval

    def getNextUid(self):
        if self.lastUid == -1:
            if (os.path.isfile(AttachmentDownloader.LAST_UID_FILE)):
                fp = open(AttachmentDownloader.LAST_UID_FILE, 'r')
                self.lastUid = int(fp.readline())
                fp.close()
            else:
                self.lastUid = 0
        return self.lastUid + 1

    def setLastUid(self, num):
        self.lastUid = int(num)
        fp = open(AttachmentDownloader.LAST_UID_FILE, 'w')
        fp.write(str(num))
        fp.close()

ad = AttachmentDownloader(Credentials("build18.picframe", "Noraisgod!"), 1, "C:/Users/Clayton/Documents/photoframe/attachments")
time.sleep(30)

"""c = Credentials.readFromFile("../credentials.txt")
gc = GmailConnection(c)
gc.login()
ids = gc.getMessagesSinceUID(5)
detach_dir = '.'
if 'attachments2' not in os.listdir(detach_dir):
    os.mkdir('attachments2')
for curId in ids:
    parts = gc.getAttachmentsFromMessage(curId, ["png", "jpg", "jpeg", "gif"])
    for part in parts:
        fileName = part.get_filename()
        filePath = os.path.join(detach_dir, 'attachments2', fileName)
        if not os.path.isfile(filePath) :
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
gc.logout()"""