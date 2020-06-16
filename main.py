import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.clock import Clock
from kivy.uix.button import Button

from random import randint
from time import sleep

# very important see documentation
kivy.require("1.11.1")

class MainElements(Widget):
    pass

class ModernwheelApp(App):

    def build(self):
        self.mainElements = MainElements()
        self.elements = readFromFile().build("dataFile.txt")
        self.btnResult = self.mainElements.ids['btnResult']
        self.btnResult.bind(on_press = self.buttonPress)
        Clock.schedule_once(self.pickRandom)
        return self.mainElements

    def pickRandom(self, *args):
        self.element_count = len(self.elements)
        self.current_pos = randint(0, self.element_count)
        self.clock_speed = 0.1
        self.animClock = Clock.schedule_interval(self.showAnim, self.clock_speed)

    def showAnim(self, *args):
        if self.current_pos + 1 <= self.element_count:
            self.btnResult.text = self.elements[self.current_pos - 1]
            self.current_pos = self.current_pos + 1
        else:
            self.current_pos = 0
            self.btnResult.text = self.elements[self.current_pos]

    def handleSlowing(self, *args):
        Clock.unschedule(self.animClock)
        self.clock_speed = self.clock_speed + 0.05
        if self.clock_speed <= .5:
            self.animClock = Clock.schedule_interval(self.showAnim, self.clock_speed)

    def buttonPress(self, *args):
        self.handleSlowing()
        self.slowingClock = Clock.schedule_interval(self.handleSlowing, 1)
    

class readFromFile:
    def build(self, filename):
        self.elements_list = []
        file = open(filename, "r")
        for line in file:
            self.elements_list.append(line)
        file.close()
        return self.elements_list


if __name__ == '__main__':
    ModernwheelApp().run()