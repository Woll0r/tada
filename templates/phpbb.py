from yapsy.IPlugin import IPlugin
import jinja2
import zipfile


class phpBBBackend(IPlugin):
    pack = None
    smiliepak = ""
        
    def build(self, pack):
        self.pack = pack
        print "[phpBB] Building pak file..."
        self.buildicondef()
        print "[phpBB] Building zip..."
        self.makeZip()

    def buildicondef(self):
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True
        )

        phpBBTemplate = env.from_string(self.template)
        self.smiliepak = phpBBTemplate.render(Emotes=self.pack)

    def makeZip(self):
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-phpBB.zip", 'w')
        outzip.writestr(self.pack.name+"-phpBB/Pony.pak", self.smiliepak)
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-phpBB/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()


    template = \
"""{% for emote in Emotes.emotelist %}
    {% for shortcut in emote.shortcuts %}
'{{ emote.filename}}', '{{ emote.width }}', '{{ emote.height }}', '0', '{{ emote.filename }}', '{{ shortcut }}',
    {% endfor %}
{% endfor %}"""