"""Psi plugin for Tada"""

import zipfile

import jinja2
from yapsy.IPlugin import IPlugin


class PsiBackend(IPlugin):
    """Psi plugin for Tada"""
    pack = None
    icondef = ""

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Psi] Building icondef...")
        self.buildicondef()
        print("[Psi] Building zip...")
        self.makezip()

    def buildicondef(self):
        """Create the emote list to fill the config"""
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True
        )

        psitemplate = env.from_string(self.template)
        self.icondef = psitemplate.render(Emotes=self.pack)

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-psi.jisp", 'w')
        outzip.writestr(self.pack.filename+"-psi/icondef.xml", self.icondef)
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.filename+"-psi/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()


    template = \
"""<?xml version='1.0' encoding='UTF-8'?>
<icondef>
    <meta>
        <name>{{ Emotes.name }}</name>
        <description>{{ Emotes.desc }}</description>
        <author>{{ Emotes.author }}</author>
        <version>{{ Emotes.version }}</version>
    </meta>

    {% for file in Emotes.emotelist %}
    <icon>
        {% for shortcut in file.shortcuts %}
        <text>{{ shortcut }}</text>
        {% endfor %}
        <object mime='{{ file.filetype }}'>{{ file.filename }}</object>
    </icon>

    {% endfor %}
</icondef>"""
