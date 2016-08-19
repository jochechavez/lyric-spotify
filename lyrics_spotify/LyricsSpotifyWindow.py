# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
import threading

logger = logging.getLogger('lyrics_spotify')


from lyrics_spotify_lib import Window

# See lyrics_spotify_lib.Window.py for more details about how this class works
class LyricsSpotifyWindow(Window):
    __gtype_name__ = "LyricsSpotifyWindow"
    t1Stop = 1

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(LyricsSpotifyWindow, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.
        import dbus, requests
        import time
        global t1Stop
        t1Stop = threading.Event()

        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus,
                "org.freedesktop.DBus.Properties")
        temp = {'title':'','artist':''}

        def check():
            while ( not t1Stop.is_set() ):
                # print 'repeat'
                metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
                title = metadata['xesam:title']
                artist = metadata['xesam:artist'][0]
                if(temp['title'] != title or temp['artist'] != artist):
                    temp['title'] = title
                    temp['artist'] = artist
                    url = "https://makeitpersonal.co/lyrics?artist="+artist+"&title="+title
                    song = requests.get(url).text
                    builder.widgets['label1'].set_text(song);
                    builder.widgets['label2'].set_text(artist+' - '+title);
                    # print song

                time.sleep(3);
                pass


        # Start check as a process
        t1 = threading.Thread(target=check)
        t1.start()

    def on_destroy(self, widget, data=None):
        super(LyricsSpotifyWindow, self).on_destroy(widget, data)
        global t1Stop
        t1Stop.set()
        print 'chao'
