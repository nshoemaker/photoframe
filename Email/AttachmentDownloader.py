from Credentials import Credentials
from GmailConnection import GmailConnection
import thread
import os
import time
import io
from PIL import Image

class AttachmentDownloader:
    LAST_UID_FILE = "meta.txt"

    def __init__(self, credentials, pollingInterval, attachmentsDirectory, screenSize):
        self.screenSize = screenSize
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
                for uid in messageIds:
                    atts = self.emailConnection.getAttachmentsFromMessage(uid, ["png", "jpg", "jpeg", "gif"])
                    for att in atts:
                        fileName = att.get_filename()
                        filePath = os.path.join(self.attachmentsDirectory, uid + "_" + fileName)
                        img = Image.open(io.BytesIO(att.get_payload(decode=True)))
                        w, h = img.size
                        scale = max(float(self.screenSize[0]) / w, float(self.screenSize[1])/h)
                        img = img.resize((w*scale, h*scale), Image.ANTIALIAS)
                        img.save(filePath)
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