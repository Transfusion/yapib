from ircutils import bot, start_all
import time, tinyurl, platform, os, subprocess, re, httplib, urllib
from untinyurl import untiny

class HelloBot(bot.SimpleBot):
                
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

        if event.message.startswith("!ping"):
            self.send_message(event.target, str("PONG"))
        if event.message.startswith("!untiny"):
            to = untiny(str(params[0]))
            self.send_message(event.target, "Untinied: "+str(to))
        if event.message.startswith("!system"):
            self.send_message(event.target, str(platform.uname()))
        if event.message.find("http://") and event.message.find("tiny") >=0:
            pass
        else:
            u = re.search("(?P<url>https?://[^\s]+)", event.message).group("url")
            if u.find("tinyurl"):
                pass
            if len(u)<21:
                pass
            else:
                to = tinyurl.create_one(u)
            self.send_message(event.target, str(to))
        if event.message.startswith("!cpu"):
            self.send_message(event.target, str(getcpu()))
        if event.message.startswith("!time"):
            self.send_message(event.target, str(time.ctime()))

        if (event.message.startswith("!tiny")) and (str(params[0]).startswith("www.")):
            to = tinyurl.create_one("http://"+str(params[0]))
            self.send_message(event.target, str(to))
        elif (event.message.startswith("!tiny")):
            to = tinyurl.create_one(str(params[0]))
            self.send_message(event.target, str(to))
        else: pass


if __name__ == "__main__":
    hello_bot = HelloBot("TinyurlBot")

    hello_bot.connect("irc.freenode.com", channel="[#botwar, #music]")

    start_all()
