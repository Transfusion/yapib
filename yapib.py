from ircutils import bot, start_all
import time, tinyurl, platform, os, re, httplib, urllib, shlex, urllib2
from untinyurl import untiny

class yapib(bot.SimpleBot):
    def __init__(self, nick):
        bot.SimpleBot.__init__(self, nick)
        self.nick = "yapib"
        self.real_name = "http://github.com/Transfusion/yapib"
        self.user = "bot"
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
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]
	
        def getcpu():
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
                
        def paste_code(to):
            request = urllib2.Request(
            'http://dpaste.de/api/',
            urllib.urlencode([('content', to)]),
            )
            response = urllib2.urlopen(request)
            return response.read()[1:-1]

            
        if event.message.startswith("!ping"):
            self.send_message(event.target, str("PONG"))
            
        if event.message.startswith("!untiny"):
            to = untiny(str(params[0]))
            self.send_message(event.target, "Untinied: "+str(to))
            
        if event.message.startswith("!system"):
            self.send_message(event.target, str(platform.uname()))
            
        #if event.message.find("http") >=0 :
        #    u = re.search("(?P<url>https?://[^\s]+)", event.message).group("url")
        #    if len(str(u))<21 or \
        #       event.message.find("!tiny") >=0 or \
        #       event.message.find("!untiny") >=0 or \
        #       u == None:
        #        pass
        #    else:
        #        to = tinyurl.create_one(u)
        #        self.send_message(event.target, str(to))
        # Uncomment this section for automatic Tiny'ing

        admin_hostmask = ['trivialand/master/transfusion', 'gateway/tor-sasl/kaira']
        # change the above to your hostmask(s).
        ns_password = "blahpassword"

        if event.message.startswith("!cpu"):
            self.send_message(event.target, str(getcpu()))
            
        if event.message.startswith("!time"):
            self.send_message(event.target, str(time.ctime()))

        if (event.message.startswith("!tiny")) and \
           (str(params[0]).startswith("www.")):
              to = tinyurl.create_one("http://"+str(params[0]))
              self.send_message(event.target, str(to))
        elif (event.message.startswith("!tiny")):
            to = tinyurl.create_one(str(params[0]))
            self.send_message(event.target, str(to))
        else: pass
        
        if event.message.startswith("!join"):
            t = shlex.split(event.message)
            item = t[1] #[!join, #blahchannel, blahkey], #blahchannel is item no 1.
            try: key = t[2]
            except IndexError:
                key = "aaa"
            if str(event.host) in admin_hostmask:
                self.join_channel(item, key)
            else: pass

        if event.message.startswith("!part"):
            if params[0] in self.channels:
                if str(event.host) in admin_hostmask:
                    self.part_channel(params[0], "Parting.")
                else: pass

        if event.message.startswith("!identify"):
            if str(event.host) in admin_hostmask:
                self.identify(ns_password)
            else: pass

        if event.message.startswith("!quit"):
            if str(event.host) in admin_hostmask:
                self.disconnect("Disconnecting.")
            else: pass

        if event.message.startswith("!paste"):
            t = shlex.split(event.message)
            u = t[1].replace(']\[', '\n')
            # ]\[ is newline.
            self.send_message(event.target, paste_code(u))




if __name__ == "__main__":
    instance = yapib("yapib")

    instance.connect("irc.freenode.com", channel=["##Transfusion", "#yapib"])

    start_all()
