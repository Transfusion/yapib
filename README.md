yapib
=====

Yet another (terribly designed, monolithic) python IRC bot that depends on http://dev.guardedcode.com/projects/ircutils/

Dependencies: 
http://pypi.python.org/pypi/TinyUrl/
http://pypi.python.org/pypi/untinyurl
https://github.com/mouuff/Google-Translate-API/blob/master/gtranslate.py
http://code.google.com/p/pygoogle/
https://developers.google.com/youtube/2.0/developers_guide_protocol The obsolete v2.0 YouTube API
https://github.com/novel/py-urbandict
https://pypi.python.org/pypi/beautifulsoup4

Commands: 
!time : Current date and time
!cpuinfo : CPU model
!system : uname -r
!g example query : Google, 4 results. Supports UTF-8 languages.
!ud idiot 1 : Urban Dictionary. The number at the end is the number of results.
!yinfo http://www.youtube.com/watch?v=kkFXuOkp0Bo : Get stats of YouTube video
!untiny http://bit.ly/GATQhW : Works on most any URL tiny program that redirects to the target site.
!tiny http://forum.ubuntu.org.cn/viewtopic.php?f=163&t=227944&sid=448c3f58bf4a4116a5d05ff61aec8e23 : TinyURL.
!title http://wiki.mibbit.com/index.php/Assign_a_channel_bot : Gets URL Title.
!paste "Lorem Ipsum is simply dummy text of the printing]/[and typesetting industry. Lorem Ipsum has been the industry's standard]/[dummy text ever since the 1500s." : Pastes to dpaste.de and ]/[ is the newline character.
!tracert google.com : Traceroute, supports hostnames and IPs. no IPv6 yet.
!trans 'Ты действительно любишь меня' en ru : Google Translate. Enclose your text in either single or double quotes. 
  List of languages & abbrevation: http://code.google.com/p/python-google-translator/ ; this isn't the library being used tho.
!wp http://en.wikipedia.org/wiki/Manga : supports UTF-8 links. !g example site:wikipedia.org will return wikipedia links.

cleverbot.py
=====
A simple bot that allows users to talk to http://www.cleverbot.com via IRC through http://code.google.com/p/pycleverbot/ 's API.
Will respond if its name is mentioned 100% of the time. Uses random.randint() which can be set to respond x% of the time in normal chat.
