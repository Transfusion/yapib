import shlex
import string
from utils import bot, start_all
import cleverbot
import random
import re
class yapib(bot.SimpleBot):
    def __init__(self, nick):
        bot.SimpleBot.__init__(self, nick)
        self.nick = nick
        self.admin_hostmask = ['trivialand/master/transfusion', 'mib-85BC6D60.node2.hpc.tw', '56B4E1D5.9295F7CB.AC422EE5.IP']
        self.real_name = "Based on https://github.com/Transfusion/yapib/"
        self.ns_password = "blahblahblah"
        self.user = "genius"
        self.mycb=cleverbot.Session()
        self.direct1=cleverbot.Session()
        self.chance = 0
        self["any"].add_handler(self.print_line)
        self.verbose = False
    def print_line(self, client, event):
        kwds = {
        "cmd": event.command,
        "src": event.source,
        "tgt": event.target,
        "params": event.params
        }
        print "[{cmd}] s={src!r} t={tgt!r} p={params}".format(**kwds)
    
    
    def on_channel_message(self, event):
        global admin_hostmask
        global ns_password
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]
        
        def cleverbotify(strang):
            out = strang.translate(string.maketrans("",""), string.punctuation)
            if out.rstrip('?:!.,;').find(self.nick)+9 == len(out.rstrip('?:!.,;')):
                strang = re.sub(self.nick,"",strang,count=1)
            elif out.find(self.nick+" ") == 0:
                strang = strang[10:]
            elif out.find(" "+self.nick+" ") !=0:
                strang = re.sub(self.nick,"you",strang,count=1)
            return strang
   

        if event.message.startswith(self.nick + ":"):
                msg=event.message
                to=msg.strip(self.nick+":")
                self.send_message(event.target, str(event.source)+": "+str(self.direct1.Ask(to)))

        elif self.nick in event.message:
            gt = cleverbotify(event.message)
            self.send_message(event.target, self.mycb.Ask(gt))

        elif len(event.message) !=0:
            x = random.randint(0,10)
            print str(x)+" chancethistime"
            if x <=self.chance:
                gt = cleverbotify(event.message)
                self.send_message(event.target, self.mycb.Ask(gt))
        else: pass


    def on_private_message(self, event):
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]
        if event.message.startswith("!say") and str(event.host) in self.admin_hostmask:
            t = shlex.split(event.message)
            self.send_message(str(t[1]), ' '.join(params[1:]))
        
        if event.message.startswith("!chance") and str(event.host) in self.admin_hostmask:
            
            tx = event.message.split()
            rx = tx[0].upper()
            params = tx[1:]
            
            self.chance = int(params[0])
            print str(self.chance)+" set to"

        if event.message.startswith("!join") and str(event.host) in self.admin_hostmask:
            t = shlex.split(event.message)
            item = t[1] #[!join, #blahchannel, blahkey], #blahchannel is item no 1.
            try: key = t[2]
            except IndexError:
                key = "aaa"

            self.join_channel(item, key)
        else: pass

        if event.message.startswith("!nick") and str(event.host) in self.admin_hostmask:
            self.set_nickname(str(params[0]))
        else: pass

        if event.message.startswith("!part") and params[0] in self.channels and str(event.host) in self.admin_hostmask:
            self.part_channel(params[0], "Parting.")
        else: pass
        if event.message.startswith("!identify") and str(event.host) in self.admin_hostmask:
            self.identify(ns_password)
        else: pass
        if event.message.startswith("!quit") and str(event.host) in self.admin_hostmask:
            self.disconnect("Disconnecting.")
        else: pass

    def on_ctcp_action(self, event):
        convert_first_to_generator = (str(w) for w in event.params)
        mesg = ''.join(convert_first_to_generator)
        print "CTCP : "+mesg
        def cleverbotify(strang):
            out = strang.translate(string.maketrans("",""), string.punctuation)
            if out.rstrip('?:!.,;').find(self.nick)+len(self.nick) == len(out.rstrip('?:!.,;')):
                strang = re.sub(self.nick,"",strang,count=1) # Strip nick if nick at end.
            elif out.find(self.nick+" ") == 0:
                strang = strang[len(nick)+1:] #Strip nick if at beginning.
            elif out.find(" "+self.nick+" ") !=0:
                strang = re.sub(self.nick,"you",strang,count=1) #Replace with you if in middle.
            return strang
        if len(event.params) !=0:
            x = random.randint(0,10)
            print str(x)+" chancethistime"+" action"
            if x <=self.chance:
                gx = self.mycb.Ask("*"+str(cleverbotify(mesg))+"*")
                if gx[0] == "*" and gx[len(gx)-2:len(gx)-1] == "*.":
                    self.send_action(event.target, gx[1:-2]+".")
                else: self.send_message(event.target, gx)

        if self.nick in mesg:
#            self.send_action(event.target, self.mycb.Ask("*"+str(cleverbotify(mesg))+"*")[1:-2]+".")
            gx = self.mycb.Ask("*"+str(cleverbotify(mesg))+"*")
            print gx
            if gx[0] == "*" and gx[len(gx)-2:len(gx)-1] == "*.":
                self.send_action(event.target, gx[1:-2]+".")
            else: self.send_message(event.target, gx)

        else: pass

if __name__ == "__main__":
    instance = yapib("CleveringBot")
    instance.connect("irc.example.com", channel=["#blahblah"])


    start_all()

