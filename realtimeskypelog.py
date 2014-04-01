import Skype4Py 
import time
import signal
import sqlite3

class SkypeHandler:

    def __init__(self):
        self.client = self.get_client()
        self.client.Attach()
        self.DB = False
        try:
            open('temp.db')
            self.db = sqlite3.connect('temp.db', check_same_thread=False)
            self.cursor = self.db.cursor()
            self.DB = True
        except Exception as e:
            print e
            print 'Database connect failed, write to stdout!'

    def get_client(self):
        """ Reveice Skype4Py.Skype instance
        *** Maybe launch Skype if not launched?
        """
        skype = Skype4Py.Skype(Events=self)

        if not skype.Client.IsRunning:
            skype.Client.Start()

        return skype

    def MessageStatus(self, msg, status):
        """ Skype event handler """
        if (len(msg.Chat.Members) > 2): #chat room
            label = msg.Chat.Topic
            handle = msg.ChatName
            icon = None
        else: #individual chat
            label = msg.FromDisplayName
            handle = msg.FromHandle

        nick = msg.FromHandle
        name = msg.FromDisplayName
        #print status
        if status == Skype4Py.skype.cmsReceived:
            if self.DB:
                self.cursor.execute('''INSERT INTO messages(msg_id, name, topic,
                                    nick, handle, body) VALUES(?,?,?,?,?,?)''',
                                    (msg.Id, name, label, nick, handle, msg.Body))
                self.db.commit()
            else:
                print handle, nick, '('+name+')', msg.Body
        elif status == Skype4Py.skype.cmsSent:
            if self.DB:
                self.cursor.execute('''INSERT INTO messages(msg_id, name, topic, 
                                    nick, handle, body) VALUES(?,?,?,?,?,?)''', 
                                    (msg.Id, name, label, nick, handle, msg.Body))
                self.db.commit()
            else:
                print handle, nick, '('+name+')', msg.Body
        elif status == Skype4Py.skype.cmsUnknown:
            if self.DB:
                self.cursor.execute('''INSERT INTO messages(msg_id, name, topic,
                                    nick, handle, body) VALUES(?,?,?,?,?,?)''',
                                    (msg.Id, name, label, nick, handle, msg.Body))
                self.db.commit()
            else:
                print handle, nick, '('+name+')', msg.Body
    def MessageHistory(self, Username):
        print Username

    def handle_unread_messages(self):
        for msg in self.client.MissedMessages:
            self.MessageStatus(msg, msg.Status)

    # gtk timeout callback
    def attach_client(self):
        """ tries to attach API to client """
        self.client.Attach()

    def add_msg():
        print AA 

if __name__ == '__main__':
    SkypeHandler()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    while True:
        time.sleep(1000)
