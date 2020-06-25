import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.core.audio import Sound

from random import randint
from time import sleep

# very important see documentation
kivy.require("1.11.1")

class MainElements(Widget):
    pass

class ModernwheelApp(App):
    ############################################################################
    #initialising the class
    def build(self):
        self.mainElements = MainElements()

        #the sound that will be played when the wheel stopps
        self.soundFile = 'Warzone_Downed_Mate.wav'

        #an integer that saves that state for the button not beautiful but easy
        #0=ready to slow # 1=slowing # 2=ready to restart
        self.state = 0

        #getting the members out of the .txt file
        self.elements = readFromFile().build("dataFile.txt")

        #binding the widgets from the .kv file to their corresponding objects
        #in python
        self.btnResult = self.mainElements.ids['btnResult']
        self.btnResult.bind(on_press = self.buttonPress)

        #attributes
        self.clock_speed = 0.1

        #running the function that picks a random startnumber in the list
        Clock.schedule_once(self.pickRandom)
        return self.mainElements

    ############################################################################
    #picking a random startingpoint in the list and starting the animation
    def pickRandom(self, *args):
        self.element_count = len(self.elements)
        self.current_pos = randint(0, self.element_count)
        
        #scheduling the clock that changes the buttons text
        self.animClock = Clock.schedule_interval(self.showAnim, self.clock_speed)

    ############################################################################
    #changing the buttons text and while looping through the list. When we hit
    #the end, the list just starts again
    def showAnim(self, *args):
        if self.current_pos + 1 <= self.element_count:
            self.btnResult.text = self.elements[self.current_pos - 1]
            self.current_pos = self.current_pos + 1
        else:
            self.current_pos = 0
            self.btnResult.text = self.elements[self.current_pos]

    ############################################################################
    #slowing down the whole animation by just rescheduling the running clock, 
    #but with a slower speed. If it hits a threshhold, it stops completely
    def handleSlowing(self, *args):
        Clock.unschedule(self.animClock)
        self.clock_speed = self.clock_speed + 0.05
        if self.clock_speed <= .4:
            self.animClock = Clock.schedule_interval(self.showAnim, 
                                                            self.clock_speed)
        else:
            #playing the predefined sound
            sound = SoundLoader.load(self.soundFile)
            if sound:
                sound.volume = 1
                sound.play()
            #unscheduling thus it's no longer needed
            Clock.unschedule(self.slowingClock)
            self.state = 2

    ############################################################################
    #what happens when you press the button. Starts the whole slowing down 
    #process
    def buttonPress(self, *args):
        if self.state == 0:
            #starting the slowing process and redoing it in a given time
            self.slowingClock = Clock.schedule_interval(self.handleSlowing, .5)
            self.state = 1

        elif self.state == 1:
            pass

        elif self.state == 2:
            #resetting everything and starting fresh
            self.clock_speed = 0.1
            Clock.schedule_once(self.pickRandom)
            self.state = 0


    

class readFromFile:
    ############################################################################
    #reading the contents out of a text file into a list
    def build(self, filename):
        self.elements_list = []
        file = open(filename, "r")
        for line in file:
            self.elements_list.append(line)
        file.close()
        return self.elements_list


if __name__ == '__main__':
    ModernwheelApp().run()