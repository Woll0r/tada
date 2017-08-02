"""Adium plugin for Tada"""

import zipfile

import jinja2
from yapsy.IPlugin import IPlugin


class AdiumBackend(IPlugin):
    """Adium plugin for Tada"""
    pack = None
    emotelist = ""

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Adium] Building emote list...")
        self.buildemotelist()
        print("[Adium] Building zip...")
        self.makezip()

    def buildemotelist(self):
        """Create the emote list to fill the config"""
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
        )

        adiumtemplate = env.from_string(self.template)
        self.emotelist = adiumtemplate.render(Emotes=self.pack)

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-adium.zip", 'w')
        outzip.writestr(self.pack.name+".AdiumEmoticonset/Emoticons.plist", self.emotelist)
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+".AdiumEmoticonset/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()

    template = \
"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AdiumSetVersion</key>
    <integer>1</integer>

    <key>Emoticons</key>
    <dict>

        {% for file in Emotes.emotelist %}
        <key>{{ file.filename }}</key>
        <dict>
            <key>Equivalents</key>
            <array>
                {% for shortcut in file.shortcuts %}
                <string>{{ shortcut }}</string>
                {% endfor %}
            </array>
            <key>Name</key>
            <string>{{ file.filename }}</string>
        </dict>
        {% endfor %}

    </dict>
</dict>
</plist>"""
