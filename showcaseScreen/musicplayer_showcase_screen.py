from audioop import add
from calendar import isleap
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.base import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock
import handlers.comHandler
import math
import handlers.csv_parsers
import time
Builder.load_file('./ui/connectionPU.kv')

comHandler = handlers.comHandler.Com()
cvr = handlers.csv_parsers.CsvRead()

class ConnectionPU(Popup):
    pass


class LoginWindow(MDScreen):
    def connect(self):
        global address
        self.url = self.ids.url.text
        self.containsPort = False
        for self.letter in self.url:
            if self.letter == ":":
                self.containsPort = True
            else:
                pass
        self.connectionurl = ""
        if self.url[:8] != "https://" and  self.url[:7] != "http://" and self.url[len(self.url) - 1:] == "/" and not self.containsPort and len(self.url) > 2:
            self.connectionurl = f"http://{self.url[:len(self.url) - 1]}:8000"
            if comHandler.connect(self.connectionurl):
                address = self.connectionurl
                screen_manager.current = "ShowcaseScreen"
            else:
                ConnectionPU().open()
        elif self.url[:8] != "https://" and self.url[:7] != "http://" and self.url[len(self.url) - 1:] != "/" and not self.containsPort and len(self.url) > 2:
            self.connectionurl = f"http://{self.url}:8000"
            if comHandler.connect(self.connectionurl):
                address = self.connectionurl
                screen_manager.current = "ShowcaseScreen"
            else:
                ConnectionPU().open()
        else:
            ConnectionPU().open()        


class ShowcaseScreen(MDScreen):
    def beginUpdating(self):
        global address
        Clock.schedule_interval(self.updateScreen, 1)
        self.lastsongpos = 200
        self.__current = comHandler.getcurrentsong(address)
        self.__upcoming = comHandler.getupcomingsongs(address)
        self.songlength = comHandler.getsonglength(address)
        self.songpos = comHandler.getsongpos(address)
        self.ids.current_song.text = self.__current
        self.ids.upcoming_songs.text = self.__upcoming
        self.ids.progressbars.value = float(self.songpos / float(self.songlength) * 100)
        self.isplaying = False
        self.averagedelatation = 0
        self.passcount = 0
        Clock.schedule_interval(self.updateProgressbar, 0.1)

    def updateScreen(self, dmp):
        Window.fullscreen = comHandler.checkiffullscreen(address)
        self.status = comHandler.checkgo(address)
        if self.status == "playing":
            self.isplaying = True
        elif self.status == "paused":
            self.isplaying = False
        elif self.status == "stopped":
            Window.fullscreen = False
            screen_manager.current = "Login"
        else:
            print("ERROR in Status. Please check connection!")
        Window.maximize()
        self.__windowsize = Window._get_size()
        self.__windowsize_x = self.__windowsize[0]
        self.__windowsize_y = self.__windowsize[1]
        self.__text_size = round(math.sqrt(((self.__windowsize_x + self.__windowsize_y) / 2)), 0)
        self.ids.current_song.font_size = self.__text_size + 5
        self.ids.upcoming_songs.font_size = self.__text_size - 5
        self.ids.titleinfo.font_size = self.__text_size * 2.2
        self.ids.upcoming_ind.font_size = self.__text_size + 10
        self.__doupdateUI = comHandler.getuiupdate(address)
        if self.__doupdateUI:
            self.songpos = comHandler.getsongpos(address)
            self.__current = comHandler.getcurrentsong(address)
            self.__upcoming = comHandler.getupcomingsongs(address)
            self.songlength = comHandler.getsonglength(address)
            print(self.songlength)
            self.ids.progressbars.value = float(self.songpos / float(self.songlength) * 100)
            self.ids.current_song.text = self.__current
            self.ids.upcoming_songs.text = self.__upcoming

    def updateProgressbar(self, dmp):
        if self.isplaying:
            self.__songdisplay = float(self.songpos / float(self.songlength) * 100)
            self.songpos += 0.1
            self.ids.progressbars.value = self.__songdisplay


class MusicPlayerShowcaseScreen(MDApp):
    global screen_manager
    screen_manager = ScreenManager()
    
    def build(self):
        self.title = "MusicPlayer Showcase Screen"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Gray"
        screen_manager.add_widget(Builder.load_file("./ui/mainui.kv"))
        screen_manager.add_widget(Builder.load_file('./ui/showcase.kv'))
        return screen_manager

MusicPlayerShowcaseScreen().run()
