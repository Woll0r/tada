from yapsy.IPlugin import IPlugin
import zipfile
import json

class ConversationsBackend(IPlugin):
    pack = None

    def build(self, pack):
        self.pack = pack
        print "[Conversations] Building zip..."
        self.makeZip()

    def makeZip(self):
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-conversations.zip", 'w')
        aliases = {}
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, emote.filename)
                for shortcut in emote.shortcuts:
                    aliases[shortcut] = emote.filename
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.writestr("emoticons.json", json.dumps({"emotes": aliases}))
        outzip.close()
