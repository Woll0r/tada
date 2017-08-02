"""PHPBB plugin for Tada"""

import zipfile

import jinja2
from yapsy.IPlugin import IPlugin


class PhpBBBackend(IPlugin):
    """PHPBB plugin for Tada"""
    pack = None
    smiliepak = ""

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[phpBB] Building pak file...")
        self.buildicondef()
        print("[phpBB] Building zip...")
        self.makezip()

    def buildicondef(self):
        """Create the emote list to fill the config"""
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True
        )

        phpbbtemplate = env.from_string(self.template)
        self.smiliepak = phpbbtemplate.render(Emotes=self.pack)

    def makezip(self):
        """Create the emote zip file"""
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
