yapib
=====

Yet another python IRC bot that depends on http://dev.guardedcode.com/projects/ircutils/, starting out with TinyURL functionality(http://pypi.python.org/pypi/TinyUrl/), UntinyURL functionality(http://pypi.python.org/pypi/untinyurl).
!untiny [url], !tiny [url], and it will pick up URLs mid-sentence that are longer than 10 characters long, excluding http:// (Disabled by default now).
!paste "content]\\\[of]\\\[this paste." will paste to http://dpaste.org . ]\\\[ is the newline character.
It has hostmask recognition functionality and will !join, !part, or !quit if the hostmask of the person issuing the command is in the list.

cleverbot.py
=====
A simple bot that allows users to talk to http://www.cleverbot.com via IRC through http://code.google.com/p/pycleverbot/ 's API.
