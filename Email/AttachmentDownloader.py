from Credentials import Credentials
from GmailConnection import GmailConnection
from threading import *
import os
import time
import io
from PIL import Image
from PIL.ExifTags import TAGS

class AttachmentDownloader:
    LAST_UID_FILE = "meta.txt"

    def __init__(self, credentials, attachmentsDirectory, screenSize):
        self.screenSize = screenSize
        self.emailConnection = GmailConnection(credentials)
        self.lastUid = -1
        self.attachmentsDirectory = attachmentsDirectory
        if not os.path.exists(attachmentsDirectory):
            os.mkdir(attachmentsDirectory)
        self.thread = Thread(target=self.run)
        self.event = Event()
        self.event.clear()
        self.done = False
        self.thread.start()

    def close(self):
        self.done = True
        self.event.set()

    def join(self):        
        self.thread.join()

    def _ready(self, args):
        self.event.set()

    def run(self):
        try:
            while True:
                messageIds = []
                try:
                    messageIds = self.emailConnection.getMessagesSinceUID(self.getNextUid())
                except Exception, e:
                    print e

            
                for uid in messageIds:
                    msgImgs = {}
                    try:
                        atts = self.emailConnection.getAttachmentsFromMessage(uid, ["png", "jpg", "jpeg", "gif"])
                    except Exception, e:
                        print e
                        continue
                    for att in atts:
                        try:
                            fileName = att.get_filename()
                            filePath = os.path.join(self.attachmentsDirectory, uid + "_" + fileName)
                            img = Image.open(io.BytesIO(att.get_payload(decode=True)))
                            tmpName = fileName.lower()
                            if tmpName.endswith(('.jpg', '.jpeg')):
				exif = img._getexif()
                                if exif:
                                    orientation = exif.get(274, 1)
                                    rotations = {1:0, 2:0, 3:180, 4:180, 5:270, 6:270, 7:90, 8:90}
                                    img = img.rotate(rotations[orientation], expand=True)
                                else:
                                    print fileName + " has no exif"
                            w, h = img.size
                            scale = min(float(self.screenSize[0]) / w, float(self.screenSize[1])/h)
                            img = img.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
                            msgImgs[filePath] = img
                        except Exception, e:
                            print e
                    try:
                        for filename in msgImgs:
                            msgImgs[filename].save(filename)
                    except Exception, e:
                        print e
                    self.setLastUid(uid)
            

                self.emailConnection.waitForMessage(self.event, self._ready)
                if self.done:
                    return
        except Exception, e:
            print e

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
