import urbandict
from ircutils import bot, start_all
import time, tinyurl, platform, os, re, httplib, urllib, shlex, urllib2, urlparse, datetime, subprocess
from pygoogle import pygoogle
from bs4 import BeautifulSoup
from untinyurl import untiny
import gdata.youtube
import gdata.youtube.service

class yapib(bot.SimpleBot):
    def __init__(self, nick):
        bot.SimpleBot.__init__(self, nick)
        self.nick = nick
        self.gresults = 4
        self.ns_password = "blahpassword"
        self.admin_hostmask = ['trivialand/master/transfusion', 'gateway/tor-sasl/kaira', '56B4E1D5.9295F7CB.AC422EE5.IP']
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

        def video_id(value):
            url_data = urlparse.urlparse(value)
            query = urlparse.parse_qs(url_data.query)
            try :
                video = query["v"][0]
            except KeyError:
                video = "null"
            return video
	
        def getcpu():
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub( ".*model name.*:", "", line,1)
                
        def runProcess(exe):    
            p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while(True):
              retcode = p.poll() #returns None while subprocess is running
              line = p.stdout.readline()
              yield line
              if(retcode is not None):
                break

        def xstr(s):
            if s is None:
                return 'null'
            return str(s)
                
        def paste_code(to):
            request = urllib2.Request(
            'http://dpaste.de/api/',
            urllib.urlencode([('content', to)]),
            )
            response = urllib2.urlopen(request)
            return response.read()[1:-1]

        def ud(term, count):
            lent = []
            jatx = []
            dict1 = urbandict.define(term)
            if count > len(dict1):
                return("Less results pl0x kk")
            else:
                for x in range(0, count, 1):
                    for i in dict1[x].keys():
                        if not(i.startswith("word")):
                            jatx.append("\x02"+i.upper()+"\x02 : "+dict1[x][i])

            return jatx

            
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

        
        # change the above to your hostmask(s).

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

        if event.message.startswith("!help"):
            self.send_message(event.source, "\x034!time\x03"+" : Current date and time")
            self.send_message(event.source, "\x034!cpuinfo\x03"+" : CPU model")
            self.send_message(event.source, "\x034!system\x03"+" : uname -r")
            self.send_message(event.source, "\x034!g asian cheekbone lifting\x03"+" : Google. 3 results only so I don't get throttled by Google.")
            self.send_message(event.source, "\x034!ud idiot 1\x03"+" : Urban Dictionary. The number at the end is the number of results.")
            self.send_message(event.source, "\x034!yinfo http://www.youtube.com/watch?v=kkFXuOkp0Bo\x03"+" : Get stats of YouTube video")
            self.send_message(event.source, "\x034!untiny http://bit.ly/GATQhW\x03"+" : Works on most any URL tiny program that redirects to the target site. So you don't accidentalled shock site.")
            self.send_message(event.source, "\x034!tiny http://forum.ubuntu.org.cn/viewtopic.php?f=163&t=227944&sid=448c3f58bf4a4116a5d05ff61aec8e23\x03"+" : TinyUrl.")
            self.send_message(event.source, "\x034!title http://wiki.mibbit.com/index.php/Assign_a_channel_bot\x03"+" : Gets URL Title. So you don't accidental NSFW in public place.")
            self.send_message(event.source, "\x034!paste \"My face is very ugly, dear Diary.]/[Please help me get better-looking face.]/[I am broke.\"\x03"+" : Pastes to dpaste.de and ]/[ is the newline character")
            self.send_message(event.source, "\x034!tracert cia.gov\x03"+" : Traceroute, supports hostnames and IPs. no IPv6.")

        if event.message.startswith("!g"):
            gs = pygoogle(str(params[0:]))
            gs.pages = 1
            self.send_message(event.target, "Found "+"\x02"+str(gs.get_result_count())+"\x02"+" Results"+" - \x02\x0310G\x03\x034o\x03\x037o\x0310g\x03\x039l\x03\x034e\x03\x02")
            try:
                searchresults = gs.search()
                for i in searchresults.keys():
                    self.send_message(event.target, i.encode("utf-8")+" "+searchresults[i].encode('utf8'))
            except TypeError:
                self.send_message(event.target, "Result could not be fetched.")

        if event.message.startswith("!title"):
            try:
                response = urllib2.urlopen(str(params[0]))
            except ValueError:
                response = urllib2.urlopen("http://transfusion.bshellz.net/jgarzik.html")
            except urllib2.URLError:
                response = urllib2.urlopen("http://transfusion.bshellz.net/mdienak.html")
            html = response.read()
            soup = BeautifulSoup(html)
            try:
                self.send_message(event.target, soup.html.head.title.contents[0].encode('utf8'))
            except AttributeError:
                self.send_message(event.target, "Could not get title/No title")

        if event.message.startswith("!noresults"):
            u = self.gresults
            try:
                self.gresults = int(params[0])
            except TypeError:
                self.send_message = (event.target, "Not an integer")
            if self.gresults > 6:
                self.send_message = (event.target, "Please don't be an ...... 7 is the limit.".encode('utf8'))

        if event.message.startswith("!tracert"):
            tracelist = []
            for line in runProcess(['traceroute', str(params[0])]):
                tracelist.append(line)
            url = "http://checkip.dyndns.org"
            request = urllib.urlopen(url).read()
            theIP = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)
            tracelist.append("Source IP: "+str(theIP[0]))
            hoplist = "\n".join(tracelist)
            self.send_message(event.target, paste_code(hoplist))

        if event.message.startswith("!ud"):
            th = shlex.split(event.message)
            try:
                int(th[2])
            except Exception, e:
                self.send_message(event.target, "Invalid number")
            for p in ud(th[1], int(th[2])):
                self.send_message(event.target, p.encode('utf8'))

        if event.message.startswith("!yinfo"):
            
            if video_id(str(params[0])) == "null":
                self.send_message(event.target, "not a youtube video")
            else:
                yt_service = gdata.youtube.service.YouTubeService()
                yt_service.ssl = False
                entry = yt_service.GetYouTubeVideoEntry(video_id=video_id(str(params[0])))
                try:
                    u = entry.rating.average
                except AttributeError:
                    u = "-"
                self.send_message(event.target, "\x02Title:\x02 "+\
                                  entry.media.title.text+" \x02Cat:\x02 "+\
                                  entry.media.category[0].text+" \x02Duration:\x02 "+\
                                  str(datetime.timedelta(seconds=int(entry.media.duration.seconds)))+" \x02Published On:\x02 "+\
                                  entry.published.text+" \x02Rating:\x02 "+\
                                  u+" out of 5")
        else: pass

        if event.message.startswith("!paste"):
            t = shlex.split(event.message)
            u = t[1].replace(']\[', '\n')
            # ]\[ is newline.
            self.send_message(event.target, paste_code(u))
            
    def on_private_message(self, event):
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]

        if event.message.startswith("!adminadd") and str(event.host) in self.admin_hostmask:
            self.admin_hostmask.append(str(params[0]))
        else: pass
                                       
        if event.message.startswith("!adminlist") and str(event.host) in self.admin_hostmask:
            no = 0
            for i in self.admin_hostmask:
                self.send_message(event.source, "\x02"+str(no)+"\x02"+" "+self.admin_hostmask[no])
                no += 1
        else: pass

        if event.message.startswith("!admindel") and str(event.host) in self.admin_hostmask:
            self.send_message(event.source, self.admin_hostmask[int(params[0])]+" deleted")
            del self.admin_hostmask[int(params[0])]
        else: pass

        if event.message.startswith("!say") and str(event.host) in self.admin_hostmask:
            t = shlex.split(event.message)
            self.send_message(str(t[1]), t[2].encode('utf8'))
        else: pass

        if event.message.startswith("!identify") and str(event.host) in self.admin_hostmask:
            self.identify(self.ns_password)
        else: pass

        if event.message.startswith("!chgpass") and str(event.host) in self.admin_hostmask:
            self.ns_password = str(params[0])
            self.send_message(event.source, "pass changed to"+str(params[0]))
        else: pass

        if event.message.startswith("!quit") and str(event.host) in self.admin_hostmask:
            self.disconnect("Disconnecting.")
        else: pass

        if event.message.startswith("!part") and str(event.host) in self.admin_hostmask and params[0] in self.channels:
            self.part_channel(params[0], "Parting.")
        else: pass

        if event.message.startswith("!join") and str(event.host) in self.admin_hostmask:
            t = shlex.split(event.message)
            item = t[1] #[!join, #blahchannel, blahkey], #blahchannel is item no 1.
            try: key = t[2]
            except IndexError:
                key = "aaa"
            self.join_channel(item, key)
        else: pass

        if event.message.startswith("!listchan") and str(event.host) in selfadmin_hostmask:
            no = 0
            for i in self.channels:
                self.send_message(event.source, "\x02"+str(no)+"\x02"+" "+self.channels[no])
                no += 1
        else: pass

if __name__ == "__main__":
    instance = yapib("yapib")

    instance.connect("irc.mibbit.net", channel=["#blahblah"])

    start_all()
