import shlex
import string
from utils import bot, start_all
import cleverbot
import random
import re
class yapib(bot.SimpleBot):
    admin_hostmask = ['trivialand/master/transfusion', 'mib-85BC6D60.node2.hpc.tw']
    ns_password = "blahblahblah"
    mycb=cleverbot.Session()
    direct1=cleverbot.Session()
    chance = 0
    def __init__(self, nick):
        bot.SimpleBot.__init__(self, nick)
        self.nick = nick
        self.real_name = "Based on https://github.com/Transfusion/yapib/"
        self.user = "genius"
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
        if event.message.startswith("!join"):
            t = shlex.split(event.message)
            item = t[1] #[!join, #blahchannel, blahkey], #blahchannel is item no 1.
            try: key = t[2]
            except IndexError:
                key = "aaa"
            if str(event.host) in yapib.admin_hostmask:
                self.join_channel(item, key)
            else: pass

    if event.message.startswith("!nick") and str(event.host) in yapib.admin_hostmask:
            self.set_nickname(str(params[0]))
        else: pass

        if event.message.startswith("!part"):
            if params[0] in self.channels:
                if str(event.host) in yapib.admin_hostmask:
                    self.part_channel(params[0], "Parting.")
                else: pass
        if event.message.startswith("!identify"):
            if str(event.host) in yapib.admin_hostmask:
                self.identify(ns_password)
            else: pass
        if event.message.startswith("!quit"):
            if str(event.host) in yapib.admin_hostmask:
                self.disconnect("Disconnecting.")
            else: pass

        if event.message.startswith(self.nick + ":"):
                msg=event.message
                to=msg.strip(self.nick+":")
                self.send_message(event.target, str(event.source)+": "+str(direct1.Ask(to)))

        elif self.nick in event.message:
            gt = cleverbotify(event.message)
            self.send_message(event.target, yapib.mycb.Ask(gt))

        elif len(event.message) !=0:
            x = random.randint(0,10)
            print str(x)+" chancethistime"
            if x <=yapib.chance:
                gt = cleverbotify(event.message)
                self.send_message(event.target, yapib.mycb.Ask(gt))
        else: pass


    def on_private_message(self, event):
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]
        if event.message.startswith("!say") and str(event.host) in yapib.admin_hostmask:
            t = shlex.split(event.message)
            self.send_message(str(t[1]), ' '.join(params[1:]))
        
        if event.message.startswith("!chance") and str(event.host) in yapib.admin_hostmask:
            
            tx = event.message.split()
            rx = tx[0].upper()
            params = tx[1:]
            
            yapib.chance = int(params[0])
            print str(yapib.chance)+" set to"

    def on_ctcp_action(self, event):
        
        def cleverbotify(strang):
            out = strang.translate(string.maketrans("",""), string.punctuation)
            if out.rstrip('?:!.,;').find(self.nick)+9 == len(out.rstrip('?:!.,;')):
                strang = re.sub(self.nick,"",strang,count=1)
            elif out.find(self.nick+" ") == 0:
                strang = strang[10:]
            elif out.find(" "+self.nick+" ") !=0:
                strang = re.sub(self.nick,"you",strang,count=1)
            return strang
        if len(event.params) !=0:
            x = random.randint(0,10)
            print str(x)+" chancethistime"+" action"
            if x <=yapib.chance:
                convert_first_to_generator = (str(w) for w in event.params)
                u = ''.join(convert_first_to_generator)
                self.send_action(event.target, yapib.mycb.Ask("*"+str(cleverbotify(u))+"*")[1:-2]+".")
        else: pass

if __name__ == "__main__":
    instance = yapib("CleveringBot")
    instance.connect("irc.example.com", channel=["#example"])


    start_all()


