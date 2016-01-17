from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import subprocess

class TutorialApp(App):        
    def build(self):
        global sr
        global cr
        global ba
        cr=' '
        sr=' '
        ba=' '
        
        f = FloatLayout()
        l = Label(text="Cointegration Simulation",
                  font_size=36,size_hint=(.6, .1),
                pos_hint={'x':.2, 'y':.90})
        
        self.textinput1 = TextInput(text='',hint_text='Stock 1',size_hint=(.3, .06),
                pos_hint={'x':.35, 'y':.83}, multiline=False,font_size=18)
        
        self.textinput2 = TextInput(text='',hint_text='Stock 2',size_hint=(.3, .06),
                        pos_hint={'x':.35, 'y':.76},font_size=17)        
        
        textoutput = TextInput(text="Cointegration Result: "+cr+"\nR Squared Residual: "+sr+"\nBid/Ask Spread: "+ba,size_hint=(.6, .14),
                                pos_hint={'x':.20, 'y':.05}, font_size=17) 
        
        def callback(instance):
            f = open('stock.txt', 'w')
            f.write(self.textinput1.text+'\n'+self.textinput2.text)
            subprocess.Popen("yahoowebfinancescraper.py 1", shell=True) 
            
            print("The stocks <%s> and <%s> are being tested."%(self.textinput1.text,self.textinput2.text))
            im = CoreImage("image.png")
            
        btn = Button(text='Execute',size_hint=(.26, .08), pos_hint={'x':.23, 'y':.23}, font_size=25)
        btn.bind(on_press=callback) 
        
        def callback2(instance):
            subprocess.Popen("main.py 1", shell=True)              
        btn2 = Button(text='New',size_hint=(.26, .08), pos_hint={'x':.51, 'y':.23}, font_size=25)
        btn2.bind(on_press=callback2)        

        f.add_widget(l)
        f.add_widget(self.textinput1)
        f.add_widget(self.textinput2)
        f.add_widget(textoutput)
        f.add_widget(btn)
        f.add_widget(btn2)
        return f 

if __name__ == "__main__":
    TutorialApp().run()