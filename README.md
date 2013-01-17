yapib
=====

Yet another python IRC bot that depends on http://dev.guardedcode.com/projects/ircutils/, starting out with TinyURL functionality(http://pypi.python.org/pypi/TinyUrl/), UntinyURL functionality(http://pypi.python.org/pypi/untinyurl).
!untiny [url], !tiny [url], and it will pick up URLs mid-sentence that are longer than 10 characters long, excluding http:// (Disabled by default now). 
!paste will make pastes to http://dpaste.org ( ]\[ is the newline character, and make sure to " " your paste content). 
It also has hostmask recognition, and can join and part channels if the person calling it has their hostmask in the list.
