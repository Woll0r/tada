from yapsy.IPlugin import IPlugin
import zipfile
from pprint import pformat


class GajimBackend(IPlugin):
    pack = None
    emoticons = ""
        
    def build(self, pack):
        self.pack = pack
        print "[Gajim] Building emoticons.py..."
        self.buildemoticons()
        print "[Gajim] Building zip..."
        self.makeZip()

    def buildemoticons(self):
        self.emoticons = "emoticons = "
        self.emoticons += pformat({emote.filename: emote.shortcuts for emote in self.pack.emotelist})

    def makeZip(self):
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-gajim.zip", 'w')
        outzip.writestr(self.pack.name+"-gajim/emoticons.py", self.emoticons)
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-gajim/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()