"""Trillian plugin for Tada"""

import zipfile

import jinja2
from yapsy.IPlugin import IPlugin


class TrillianBackend(IPlugin):
    """Trillian plugin for Tada"""
    pack = None
    trillianzip = ""

    def build(self, pack):
        """Build the emote pack"""
        self.pack = pack
        print("[Trillian] Building xml file...")
        self.buildicondef()
        print("[Trillian] Building zip...")
        self.makezip()

    def buildicondef(self):
        """Create the emote list to fill the config"""
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True
        )

        trilliantemplate = env.from_string(self.template)
        self.trillianzip = trilliantemplate.render(Emotes=self.pack)

    def makezip(self):
        """Create the emote zip file"""
        outzip = zipfile.ZipFile(self.pack.output+"/"+self.pack.filename+"-trillian.zip", 'w')
        outzip.writestr(self.pack.name+"-trillian/main.xml", self.trillianzip)
        outzip.writestr(self.pack.name+"-trillian/desc.txt", self.pack.name + "\nemot")
        for emote in self.pack.emotelist:
            try:
                outzip.write(self.pack.path+"/"+emote.filename, self.pack.name+"-trillian/"+emote.filename)
            except OSError:
                # The underlying emote file isn't found
                # This throws varying errors, but are all OSError or subclasses
                pass
        outzip.close()


    template = \
"""{% for emote in Emotes.emotelist %}
<bitmap name="{{ emote.filename }}" file="../../stixe/plugins/{{ Emotes.name }}-trillian/{{ emote.filename }}" />
{% endfor %}
<prefs>
<control name="emoticons" type="emoticons">
<!-- Pones -->
<group text="Emotes" initial="1">
{% for emote in Emotes.emotelist %}
    {% for shortcut in emote.shortcuts %}
<emoticon text="{{ shortcut }}"><source name="{{ emote.filename}}" left="0" top="0" right="{{ emote.width }}" bottom="{{ emote.height }}" /></emoticon>
    {% endfor %}
{% endfor %}
</group>
<!-- Please include... --><!-- I totally have no idea what this does but it seems important -->
&Emoticon-Extensions;
&iniMenuItemColor;
&iniIconMenuItemSettings;
<settings name="Width" value="600"/>
<font name="section"                    source="ttfDefault"     type="&iniDefaultFontName;"     size="&iniDefaultFontSize;"     bold="1"/>
</control>
</prefs>
"""
