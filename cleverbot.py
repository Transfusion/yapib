from ircutils import bot, start_all
import cleverbot
class yapib(bot.SimpleBot):
    def __init__(self, nick):
        bot.SimpleBot.__init__(self, nick)
        self.nick = "CleveringBot"
        self.real_name = "Based on http://github.com/Transfusion/yapib"
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
        tx = event.message.split()
        rx = tx[0].upper()
        params = tx[1:]

        if event.message.startswith(self.nick + ":"):
                mycb=cleverbot.Session()
                msg=event.message
                to=msg.strip(self.nick+":")
                self.send_message(event.target, str(event.source)+": "+str(mycb.Ask(to)))
        else: pass


if __name__ == "__main__":
    instance = yapib("yapib")

    instance.connect("irc.freenode.net", channel=["#yapib"])

    start_all()
