import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.carousel import Carousel

# very important see documentation
kivy.require("1.11.1")

class MainElements(Widget):
    pass

class ModernwheelApp(App):

    def build(self):
        self.mainElements = MainElements()

        return self.mainElements


if __name__ == '__main__':
    ModernwheelApp().run()