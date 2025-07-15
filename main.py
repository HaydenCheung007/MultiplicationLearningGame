import os, sys
if sys.__stdout__ is None or sys.__stderr__ is None:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.core.window import Window
Window.size = (800,600)
import kivy
from kivy.app import App
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
import random
from random import shuffle
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from functools import partial
from kivy.core.audio import SoundLoader

#audio
bc_audio = SoundLoader.load('assets/audio/challenge.mp3')
bc_audio.play()
bc_audio.volume = 0.5
bc_audio.loop = True
#json store
mulStore = JsonStore('mulNum.json')
#checks if it has already been stored
if mulStore.exists('check') == False:
    #stores value 10 for all 100 facts
    for i in range(1,11):
        for j in range(1,11):
            mulStore[f"{i}x{j}"] = {"num": 10}
            mulStore["check"] = {"exist": True}
#print(mulStore.get("4x4")["num"])
#.kv design file
Builder.load_file('assets/Colors.kv')
#Design classes
class backgroundColor(Widget):
    pass

class layoutColor(BoxLayout):
    pass

#main page#####################
class startScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='horizontal', spacing=10)
        #modify label
        lbl = backgroundColor()
        lbl.add_widget(Label(text="This is a multiplication learning game with two \n game modes: Challenge and Concept."
        "\nIn the Challenge mode, you face a series of\n timed multiplication problems,"
        "\nwhile the Concept mode helps you practice\n specific multiplication facts at your own pace."
        "\n You can track your progress and see your \nperformance in the Management page,"
        "\nwhere you can review your strengths\n and areas to improve.",markup=True, size_hint=(0.6, 1), pos=(230, 300), font_size=25))
        btn = Button(text="Start When you are ready!", size_hint=(0.4, 1), font_name='assets/icons/minecraft.ttf', on_release=self.switch_page)
        layout.add_widget(lbl)
        layout.add_widget(btn)
        self.add_widget(layout)


    def switch_page(self, instance):
        #Switch to Navigation Screen
        self.manager.current = "Nav"
###############################
class NavScreen(Screen):
    #Navigation screen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #The overall layout
        layout = BoxLayout(orientation='vertical')
        #top layout
        menu_layout = BoxLayout(size_hint=(1,0.1))
        #tabs
        volume = Button(text="", size_hint=(None, 1), width=100, background_normal='assets/icons/volume.png',
                        background_down = 'assets/icons/volume-down.png', on_release=self.openVol)

        menu_btn2 = Button(text="?", size_hint=(None, 1), width=100,font_size=30, font_name='assets/icons/minecraft.ttf', on_release=self.switch_Help)
        #Child layout
        content_layout = layoutColor(orientation='horizontal', size_hint=(1, 0.9), padding=[25, 25, 25, 25])
        concept_nav = Button(text="Concept\n\nlearn concept\nthrough \nmultiplication\ngrid", size_hint=(None, None), width=250,background_normal = '',
                              background_color=(0.57,0.80,0.24,1), height=450,
                              font_size=30,font_name='assets/icons/minecraft.ttf', on_release=self.switch_Mul)
        challenge_nav = Button(text="Challenge\n\ntime limited\ntest\n \n ", size_hint=(None, None), background_normal = '',
                              background_color=(0.33,0.65,0.28,1),font_name='assets/icons/minecraft.ttf',
                               font_size=30, width=250, height=450, on_release=self.switch_Clg)
        manage_nav = Button(text="Management\n\nlearn your\nmultiplication\nweaknesses\n ", size_hint=(None, None), background_normal = '',
                              background_color=(0.30,0.58,0.30,1),font_name='assets/icons/minecraft.ttf',
                              font_size=30,width=250, height=450, on_release=self.switch_Man)
        #button widgets
        content_layout.add_widget(concept_nav)
        content_layout.add_widget(challenge_nav)
        content_layout.add_widget(manage_nav)
        menu_layout.add_widget(volume)
        menu_layout.add_widget(menu_btn2)
        #layout
        self.add_widget(layout)
        #menu and content within layout
        layout.add_widget(menu_layout)
        layout.add_widget(content_layout)


    def switch_Help(self, instance):
        #Switch to Start Screen (Instructions)
        self.manager.current = "Start"
    
    def switch_Mul(self, instance):

        self.manager.current = "Table"
    
    def switch_Clg(self, instance):

        self.manager.current = "Challenge"

    def switch_Man(self, instance):
        self.manager.current = "Management"
    
    #a volume popup
    def openVol(self, instance):
        self.vLayout = FloatLayout()
        self.VolDis = Label(text=f"Volume\n{round(bc_audio.volume*10)}", pos=(340,200), size_hint=(None,None),
                            size=(70,70),halign="center", font_name='assets/icons/minecraft.ttf',
                              markup=True)
        self.vLayout.add_widget(self.VolDis)
        self.incVol = Button(text="+", on_release=self.IncreaseVol, pos=(270,200), size_hint=(None,None),
                            size=(70,70))
        self.vLayout.add_widget(self.incVol)
        self.decVol = Button(text="-", on_release=self.DecreaseVol, pos=(410,200), size_hint=(None,None),
                            size=(70,70))
        self.vLayout.add_widget(self.decVol)

        self.vol = Popup(title="Volume", content=self.vLayout,
            size_hint=(0.5,0.5), title_color=(1,1,1,1),
              title_size=50, title_font="Roboto-Bold")
        self.vol.open()

    def IncreaseVol(self, instance):
        #make sure volume between 1 and 0
        if bc_audio.volume <= 0.9:
            bc_audio.volume += 0.1
            #output
            self.VolDis.text = f"Volume\n{round(bc_audio.volume*10)}"

    def DecreaseVol(self, instance):
        #make sure volume between 1 and 0
        if bc_audio.volume >= 0.1:
            bc_audio.volume -= 0.1
            #output
            self.VolDis.text = f"Volume\n{round(bc_audio.volume*10)}"
##############################:####
class AcornObject(Image):
    def __init__(self, **kwargs):
        super(AcornObject, self).__init__(source='assets/icons/acorn.png', fit_mode="contain", **kwargs)
    #make acorns bigger
    def larger(self):
        Animation.stop_all(self) #reset the animation of acorn to default
        anima = Animation(size=(60,60),opacity=1, duration=0.1) + Animation(size=(50, 50), duration=0.08)
        anima.start(self)
    #make opacity/2 and smaller
    def return_org(self):
        Animation.stop_all(self) #reset the animation of acorn to default
        anima = Animation(size=(45, 45), opacity=0.5,duration=0.1) 
        anima.start(self)

class MulTable(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()  # 10x10 Layout
        bg_image = Image(source='assets/icons/bg3.jpg', fit_mode="cover")
        self.layout.add_widget(bg_image)
        #multiplication fact display box
        self.info_box = Label(text='', font_size=40, pos=(270,150))
        self.layout.add_widget(self.info_box)
        #return button
        Nav_btn = Button(text = "back", size_hint=(None, None), width=50, height=50,
                            pos=(750,550),background_color=(0.5,0.4,0,1),
                            background_normal = '',font_name='assets/icons/minecraft.ttf', on_release=self.switch_Nav)
        self.layout.bind(on_touch_down=self.show_multiplication)
        self.layout.bind(on_touch_move=self.show_multiplication)
        #test button
        self.test = Button(text="test", size_hint=(None,None), size=(100,50), pos=(600,550),font_name='assets/icons/minecraft.ttf',
         on_release=self.circulateTest )
        self.layout.add_widget(self.test)
        #grid modifications
        boxSize = 40
        gridLftPad = 0
        gridBtmPad = -20
        spacing = 10
        self.all = []
        for i in range(1,11):
            row = []
            for j in range(1,11):
                Acorn = AcornObject(size_hint=(None, None), size = (45,45),pos=((j)*(boxSize+spacing)+gridLftPad,
                                                                                (11-i)*(boxSize+spacing)+gridBtmPad), opacity=0.5)
                self.layout.add_widget(Acorn)
                Acorn.active = False
                Acorn.bind(on_touch_down=self.show_multiplication)
                row.append(Acorn)
            self.all.append(row)
        #1-10 horizontal
        for i in range(1,11):
            horLabel= Label(text=f"{i}",font_size=40,pos=((i*(boxSize+spacing)+gridLftPad-7.7*(boxSize+spacing),250)))
            self.layout.add_widget(horLabel)
        #1-10 vertical
        count = 10
        for i in range(1,11):
            VertLabel= Label(text=f"{count}",font_size=40,pos=(-7.5*(boxSize+spacing)+gridLftPad,i*(boxSize+spacing)+-6*(boxSize+spacing)))
            count = count - 1
            self.layout.add_widget(VertLabel)
        self.layout.add_widget(Nav_btn)
        self.add_widget(self.layout)
       # self.all[2][2].larger()

        #for test button
        self.circulate = True

    def switch_Nav(self, instance):

        self.manager.current = "Nav"        

    

    def show_multiplication(self, instance, touch):
        # Update the information box text when an acorn is tapped
        boxW = 50
        #print(touch.x,touch.y)
        myX = int((touch.x+7)//boxW)
        myY = int(10.5-(touch.y-22)//boxW)
        #print(myX,myY)
        #print(touch.y)
        #it updates the animation on the acorns
        for i in range(0,10):
            for j in range(0,10):
                if myX <= 10:
                    if j+1 <= myX and i+1 <= myY:
                        if  not self.all[i][j].active:
                            self.all[i][j].larger()
                            self.all[i][j].active = True
                    else:
                        if self.all[i][j].active == True:
                            self.all[i][j].return_org()
                            self.all[i][j].active = False
        #updates the value of the info box
        if 1 <= myX <= 10 and 1 <= myY <= 10:
            self.info_box.text = f"{myX} X {myY} = {myX * myY}"


    def conceptTest(self,instance):
        #remove info box
        self.layout.remove_widget(self.info_box)
        #display fact
        self.display = Label(text="", font_size=20, pos=(270,150),halign="left", markup=True)
        self.layout.add_widget(self.display)
        #show result
        self.result = Label(text="", font_size=20, pos=(270,200), markup=True)
        self.layout.add_widget(self.result)
        #generate random question
        self.randomFact()
        self.next = Button(text="next",size_hint=(None,None), size=(100,100), pos=(700,300),
                            on_release=self.nextFact)
        self.layout.add_widget(self.next)
        self.confirm = Button(text="confirm", size_hint=(None,None), size=(100,100), pos=(550,300),font_name='assets/icons/minecraft.ttf',
                              on_release=self.checkFact)
        self.layout.add_widget(self.confirm)

    #generate and display a random fact
    def randomFact(self):
        self.mainQ = [f"{x} x {y}" for x in range(1,11) for y in range(1,11)]
        self.subQ = self.mainQ
        self.n = random.randint(0,len(self.subQ)-1)
        self.display.text = f"can you collect ( {self.subQ[self.n]} )\n acorns for the squirrel?"

    #method for the next button
    def nextFact(self,instance):
        self.result.text = ""
        self.randomFact()
    #to validate the answer
    def checkFact(self, instance):
        x, y = self.subQ[self.n].split("x")
        x = int(x)
        y = int(y)
        if self.info_box.text == f"{x} X {y} = {x * y}" or self.info_box.text == f"{y} X {x} = {x * y}":
            self.result.text = f"correct! \n{x} X {y} = {x * y}"
        else:
            self.result.text = "incorrect try again ..."
    #a circulating test button
    def circulateTest(self, instance):
        if self.circulate == True:
            self.test.text = "close test"
            self.conceptTest(instance)
            self.circulate = False
        else:
            self.test.text = "test"
            self.close()
            self.circulate = True
    #close test
    def close(self):
        self.layout.add_widget(self.info_box)
        self.layout.remove_widget(self.next)
        self.layout.remove_widget(self.display)
        self.layout.remove_widget(self.result)
        self.layout.remove_widget(self.confirm)
        
        
###################################
class Challenge(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        start = False

        self.Clayout = FloatLayout()
        self.add_widget(self.Clayout)
        #background img
        bg_image = Image(source='assets/icons/background-challenge.jpeg', fit_mode="cover")
        self.Clayout.add_widget(bg_image)
        #tree img
        self.tree = Image(source='assets/icons/tree.png', size_hint=(None,None), size=(400,800), pos=(450,-100))
        self.Clayout.add_widget(self.tree)
        #menu button
        self.myMenu = Button(text="", on_release=self.Menu, pos=(725,540), size_hint=(None,None), size=(75,60),
                             background_normal ="assets/icons/settings.png", background_down="assets/icons/settings-down.png")
        self.add_widget(self.myMenu)
        #label for counting 3 2 1
        self.tto = Label(text="", font_size=50, color=(1,1,1,1))
        self.add_widget(self.tto)
        #creating a object of the numpad
        self.numpad = numPad(pos=(300,100))
        self.Clayout.add_widget(self.numpad)
        #replay button
        self.replay = Button(text="Replay", pos=(450, 70), size_hint=(None, None),font_size=30, size=(150, 80),
                background_normal ="assets/icons/submitButton.png", background_down ="assets/icons/submitButton.png",
                font_name='assets/icons/minecraft.ttf', on_release=self.replayGame)
        self.quit = Button(text="Quit", pos=(190, 70), size_hint=(None, None),font_size=30, size=(150, 80),
                background_normal ="assets/icons/submitButton.png",background_down ="assets/icons/submitButton.png",
                font_name='assets/icons/minecraft.ttf', on_release=self.gameReset)
        #controller
        #self.c = Controller()
        #self.Clayout.add_widget(self.c)
        #submit button
        self.submit = Button(text="Submit", pos=(450, 150), size_hint=(None, None),font_size=30, size=(150, 80),
                             background_normal ="assets/icons/submitButton.png",background_down ="assets/icons/submitButton.png",font_name='assets/icons/minecraft.ttf')
        self.submit.bind(on_release=self.submit_click)
        self.Clayout.add_widget(self.submit)
        #just a barrier button to prevent players to interact with the game before the countdown
        self.barrier = Button(text="", size_hint=(1,1), opacity=0.9)
        self.barrier.disabled = True
        self.Clayout.add_widget(self.barrier)
        #click to start the game
        self.start = Button(text="Tap to start", size_hint=(1,1), font_size=50, color=(1,1,1,1), opacity=0.9, font_name='assets/icons/minecraft.ttf')
        self.Clayout.add_widget(self.start)
        self.results = Label(text=f"", size_hint=(1,1), pos=(-59,50), font_size=30, color=(1,1,1,1), line_height=1, halign="left", markup = True, font_name='assets/icons/minecraft.ttf')
        self.start.bind(on_release=self.gameStart)   
        self.time = 3
        store = JsonStore('hello.json')     

    def switch_Nav(self, instance):

        self.manager.current = "Nav" 


    def gameStart(self, instance): 
        #print("pressed")
        self.start.text= ""
        self.start.disabled = True
        self.barrier.disabled = False
        self.start_clock()
        self.tto.text = str(self.time)

    def gameReset(self, instance):

        #reset numpad
        self.numpad.input_box.text = ""
        #just a barrier button to prevent players to interact with the game before the countdown
        self.Clayout.remove_widget(self.barrier)
        self.Clayout.add_widget(self.barrier)
        self.barrier.disabled = True
        #click to start the game
        self.Clayout.remove_widget(self.start)
        self.Clayout.add_widget(self.start)
        self.start.text = "start"
        self.start.disabled = False
        #reset 321 timer
        self.time = 3
        #reset text in tto
        self.tto.text = ""
        #stop 321 timer
        Clock.unschedule(self.clockCount)
        #reset controller variables
        try:
            self.Clayout.remove_widget(self.c)
            self.Clayout.remove_widget(self.results)
            self.Clayout.remove_widget(self.ab_image)
            self.remove_widget(self.replay)
            self.remove_widget(self.quit)
        except:
            pass
         
        self.switch_Nav(instance)

    def replayGame(self, instance):

        #reset numpad
        self.numpad.input_box.text = ""
        #just a barrier button to prevent players to interact with the game before the countdown
        self.Clayout.remove_widget(self.barrier)
        self.Clayout.add_widget(self.barrier)
        self.barrier.disabled = True
        #click to start the game
        self.Clayout.remove_widget(self.start)
        self.Clayout.add_widget(self.start)
        self.start.text = "start"
        self.start.disabled = False
        #reset 321 timer
        self.time = 3
        #reset text in tto
        self.tto.text = ""
        #stop 321 timer
        Clock.unschedule(self.clockCount)
        #reset controller variables
        try:
            self.Clayout.remove_widget(self.c)
            self.Clayout.remove_widget(self.results)
            self.Clayout.remove_widget(self.ab_image)
            self.remove_widget(self.replay)
            self.remove_widget(self.quit)
        except:
            pass

    def clockCount(self, dt):
        self.time = self.time - 1
        self.tto.text= f"{self.time}"
        if self.time == 0:
            Clock.unschedule(self.clockCount)
            self.tto.text= ""
            self.Clayout.remove_widget(self.barrier)
            self.Clayout.remove_widget(self.start)
           # self.time = 3
            #controller
            self.c = Controller()
            self.Clayout.add_widget(self.c)

    def start_clock(self):
        Clock.schedule_interval(self.clockCount,1)

    def submit_click(self,instance):
        value = self.numpad.input_box.text
        #if value isnt blank
        if value != "":
            # after the last question, show the results table
            if self.c.question_count == 0:
                #print("@@@@")
                self.c.check_answer(value)
                self.results_display()
                Clock.unschedule(self.c.updateTimer)
            else:
                self.c.check_answer(value)
                self.c.newQ()
                self.numpad.input_box.text=""


    def results_display(self):
        #background image
        self.ab_image = Image(source='assets/icons/Results.jpeg', fit_mode="cover")
        self.Clayout.add_widget(self.ab_image)
        #results label
        self.Clayout.add_widget(self.results)
        self.results.text = f"You have achieved {self.c.score} out of 10!"
        #replay button
        self.add_widget(self.replay)
        self.add_widget(self.quit)
        #output all wrong answered questions
        for i in range(len(self.c.wrongAns)):
            if i == 0:
                self.results.text += f"\n please improve on:\n{self.c.wrongAns[i]}  = {self.c.CorrectAns[i]}"
            else:
                self.results.text += f"\n{self.c.wrongAns[i]} = {self.c.CorrectAns[i]}"

    def Menu(self, instance):
        #stop the timer if exist
        try:
            Clock.unschedule(self.c.updateTimer)
        except:
            pass
        #add all the buttons and a layout
        self.mLayout = FloatLayout()
        self.outline = Label(text="Paused . . .", font_size=49, color=(0.3,0.7,0.6,1), pos=(-245,300), bold=True)
        self.mLayout.add_widget(self.outline)
        self.resume = Button(text="resume", on_release=self.Resume, size_hint=(None,None),
                              size=(200,70), pos=(100,450), font_name='assets/icons/minecraft.ttf')
        self.mLayout.add_widget(self.resume)
        self.back = Button(text="Quit", on_release=self.Quit, pos=(100,345), size_hint=(None,None),
                            size=(200,70), font_name='assets/icons/minecraft.ttf')
        self.mLayout.add_widget(self.back)
        #volume
        self.VolDis = Label(text=f"Volume\n{round(bc_audio.volume*10)}", pos=(170,240), size_hint=(None,None),
                            size=(70,70), markup=True, halign='center', font_name='assets/icons/minecraft.ttf')
        self.mLayout.add_widget(self.VolDis)
        self.incVol = Button(text="+", on_release=self.IncreaseVol, pos=(100,240), size_hint=(None,None),
                            size=(70,70))
        self.mLayout.add_widget(self.incVol)
        self.decVol = Button(text="-", on_release=self.DecreaseVol, pos=(240,240), size_hint=(None,None),
                            size=(70,70))
        self.mLayout.add_widget(self.decVol)
        #popup design
        self.menu_popup = Popup(title="Paused . . .", content=self.mLayout, background="assets/icons/Menu.jpeg"
            , size_hint=(1,1), separator_height=0, auto_dismiss=False, title_color=(1,1,1,1),
              title_size=50, title_font="Roboto-Bold")
        #open the popup
        self.menu_popup.open()

    def Resume(self, instance):
        try:
            if self.c.Current_Question != 0: 
                Clock.schedule_interval(self.c.updateTimer, 1)
        except:
            pass
        self.menu_popup.dismiss()
    
    def Quit(self, instance):
        #remove popup
        self.menu_popup.dismiss()
        #call gameReset
        self.gameReset(instance)

    def IncreaseVol(self, instance):
        print(bc_audio.volume)
        if bc_audio.volume <= 0.9:
            bc_audio.volume += 0.1

            self.VolDis.text = f"Volume\n{round(bc_audio.volume*10)}"

    def DecreaseVol(self, instance):
        if bc_audio.volume >= 0.1:
            bc_audio.volume -= 0.1
            self.VolDis.text = f"Volume\n{round(bc_audio.volume*10)}"

        


class numPad(FloatLayout):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cal_img = Image(source="assets/numpad/Calculator2.png",size_hint=(None,None),size=(700,1200),pos=(-100,-280))
        self.add_widget(cal_img)
        boxSize = 80
        spacing = 10
        self.input_box = TextInput(text="", size_hint=(None, None),font_size=40, size=(240, 80), pos=(130,440))
        self.add_widget(self.input_box)       
        left = 120
        top = 300
        count = 1
        #buttons added to the numpad 1-9
        for i in range(1,10):
            n = Image(source=f'assets/numpad/num{i}.png', size_hint=(None,None), size=(80,80),pos=(((i-1)%3)*boxSize+spacing+left,(i-1)//3*80+500-top))
            n.bind(on_touch_down=self.on_num_click)
            n.number = i
            self.add_widget(n)
            count = count + 1
        #extra buttons
        self.remove = Image(source=f'assets/numpad/numback.png', size_hint=(None,None), size=(80,80), pos=(210,120))
        self.add_widget(self.remove)
        self.remove.bind(on_touch_down=self.delete)
        self.zero = Image(source=f'assets/numpad/num0.png', size_hint=(None,None), size=(80,80), pos=(130,120))
        self.add_widget(self.zero)
        self.zero.bind(on_touch_down=self.on_num_click)
        self.zero.number = 0
        self.removeAll = Image(source=f'assets/numpad/bin.png', size_hint=(None,None), size=(80,80), pos=(290,120))
        self.removeAll.bind(on_touch_down=self.deleteAll)
        self.add_widget(self.removeAll)

         

    def on_num_click(self, i, touch):
        if i.collide_point(touch.x, touch.y):
           # print(f"Number {number}")
           self.input_box.text = self.input_box.text + str(i.number)
    
    def delete(self, i, touch):
        if i.collide_point(touch.x, touch.y):
            self.input_box.text = self.input_box.text[:-1]

    def deleteAll(self, i, touch):
        if i.collide_point(touch.x, touch.y):
            self.input_box.text = ""




class Controller(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.question_count = 10
        self.q = QGenerate()
        self.add_widget(self.q)
        #Squirrel img
        self.Sqr_image = Image(source='assets/icons/Sql-idle.png', size_hint=(None,None), size=(200,200), pos=(600,300))
        self.add_widget(self.Sqr_image)
        #timer
        self.countdownTimer = Label(text="e", pos=(150,240), font_size=50, color=(0,0,0,1))
        self.add_widget(self.countdownTimer)
        #results table
        self.results2 = Label(text=f"", size_hint=(1,1), pos=(-59,50), font_size=30, color=(1,1,1,1), line_height=1, halign="left", markup = True, font_name='assets/icons/minecraft.ttf')
        #stores wrong and corretly answered questions
        self.wrongAns = []
        self.CorrectAns = []
        self.timerC = 5  # Reset timer to 5 seconds
        #first question
        self.newQ()

    #generated a new question every 5 seconds (if submit button presses )
    def newQ(self):
        if self.question_count > 0:
            #gen question
            self.Current_Question = self.q.genQuestion()
            self.question_count -= 1
            self.timerC = 5
            self.countdownTimer.text = f"Time: {self.timerC}"
            #stop the timer before
            Clock.unschedule(self.updateTimer)
            #start the timer again
            Clock.schedule_interval(self.updateTimer, 1)

    
    def updateTimer(self, dt):
        if self.timerC > 0:
            self.timerC -= 1
            self.countdownTimer.text = f"Time: {self.timerC}"
        else:
            #the answer is considered wrong if not submited (timer = 0)
            num1 , num2 = self.q.questions.text.split('x')
            self.num1 = int(num1)
            self.num2 = int(num2)
            self.ans = self.num1 * self.num2
            self.Q = f"{self.num1}x{self.num2}"
            self.wrongAns.append(self.Q)
            self.CorrectAns.append(self.ans)
            #timer stops at timerC = 0
            Clock.unschedule(self.updateTimer)
            #print("next")
            #next question
            if self.question_count == 0:
                try:
                    challenge_screen = self.parent.parent #floatlayout --> Challenge so two parents
                    challenge_screen.results_display()
                except:
                    print("fail")
            else:
                self.newQ()

    def check_answer(self, value):
        #split the fact into two varibles to calculate a answer
        num1 , num2 = self.Current_Question.split('x')
        self.num1 = int(num1)
        self.num2 = int(num2)
        self.ans = self.num1 * self.num2
        #need to remake the question for json store since i stored it in a different format
        self.Q = f"{self.num1}x{self.num2}"
        if int(value) == self.ans:
            #print("correct")
            self.SqrAnimation(0)
            self.score += 1
            #check if max num before + 1
            if mulStore.get(self.Q)['num'] < 10: #directly access the value
                temp = mulStore.get(self.Q)['num'] + 1
                mulStore[self.Q] = {"num": temp}
                #print(mulStore.get(self.Q))
                #print("hi")
        else:
            self.wrongAns.append(self.Q)
            self.CorrectAns.append(self.ans)
            #print("incorrect")
            #check if min num before -1
            if mulStore.get(self.Q)['num'] > 0: #directly access the value
                temp = mulStore.get(self.Q)['num'] - 1
                mulStore[self.Q] = {"num": temp}
                #print(mulStore.get(self.Q))
                #print("hi")



    def SqrAnimation(self, dt):
        #change image
        self.Sqr_image.source = 'assets/icons/Sql-Celebrate.png'
        #revert after 0.7 seconds
        Clock.schedule_once(self.change, 0.7)
    
    def change(self, dt):
        self.Sqr_image.source='assets/icons/Sql-idle.png'    


class QGenerate(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_image = Image(source='assets/icons/questionBox.png', pos=(160,140))
        self.add_widget(self.box_image)
        #label for displaying question
        self.questions = Label(text="", font_size=50, color=(1,1,1,1), pos=(145,145))
        self.add_widget(self.questions)
        #all the questions
        self.mainQ = [f"{x} x {y}" for x in range(1,11) for y in range(1,11)]
        self.subQ = self.mainQ
        global gloQueue
        self.tempQ = gloQueue.copy()
        for i in range(len(self.tempQ)):
            if self.tempQ[i] in self.subQ:
                self.subQ.remove(self.tempQ[i])
        self.finalQueue = []
        self.finalQueue += self.tempQ
        while len(self.finalQueue) < 10:
            val = random.randint(0,len(self.subQ)-1)
            self.finalQueue.append(self.subQ[val])
            #print(self.finalQueue)


    def genQuestion(self):
        #used to check if self.final Queue is empty 
        if len(self.finalQueue) == 0:
            return(None)
        #choose random index within range
        queueVal = random.randint(0,len(self.finalQueue)-1)
        self.Current_Question = self.finalQueue[queueVal]
        self.questions.text = self.finalQueue[queueVal]
        #remove the item from the queue
        #print(self.finalQueue)
        self.finalQueue.pop(queueVal)
        #print(self.finalQueue)
        return self.Current_Question
        
    


##########################################

gloQueue = []
class Management(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.MfloatLayout = FloatLayout()
        self.add_widget(self.MfloatLayout)
        #background image
        bg_image = Image(source='assets/icons/background-challenge.jpeg', fit_mode="cover")
        self.MfloatLayout.add_widget(bg_image)
        #hint
        hint = Button(text="?", pos=(700,550), size_hint=(None, None), width=50,
                       height=50, font_size=30, font_name='assets/icons/minecraft.ttf', on_release=self.hint)
        self.MfloatLayout.add_widget(hint)
        #queue box 
        writeQ = Label(text="Queue", color=(0,0,0,1), pos=(230,240), font_size=30, font_name='assets/icons/minecraft.ttf')
        self.MfloatLayout.add_widget(writeQ)
        q_image = Image(source='assets/icons/queueBox2.png', size_hint=(None,None), size=(200,500), pos=(530,35))
        self.MfloatLayout.add_widget(q_image)
        #return button
        self.back = Button(text="back", size_hint=(None, None), width=50, height=50,
                            pos=(750,550),background_color=(0.5,0.4,0,1),
                            background_normal = '', font_name='assets/icons/minecraft.ttf', on_release=self.switch_Nav)
        self.MfloatLayout.add_widget(self.back)
        #resets progress
        self.pReset = Button(text="Progress\nReset", size_hint=(None, None), width=80, height=50,
                    pos=(0,550),background_color=(0.5,0.4,0,1),
                    background_normal = '', font_name='assets/icons/minecraft.ttf', markup=True, on_release=self.areYouSure)
        self.MfloatLayout.add_widget(self.pReset)
        #display queue
        self.Mqueue = Label(text="", size_hint=(None, None), size=(200,600),pos=(600,-100),
                             font_size=25, text_size=(200,600), color=(0,0,0,1),valign="top",line_height=1.5, markup=True)
        self.add_widget(self.Mqueue)
        #delete item from queue
        self.delete = Button(text="delete", size_hint=(None, None), width=100, height=50,
                              pos=(700,400),background_color=(0.5,0.4,0,1),background_normal = '', font_name='assets/icons/minecraft.ttf',
                                on_release=self.dequeue)
        self.MfloatLayout.add_widget(self.delete)
        #delete all
        self.deleteAll = Button(text="delete all", size_hint=(None, None), width=100, height=50,
                                 pos=(700,330),background_color=(0.5,0.4,0,1),background_normal = '', font_name='assets/icons/minecraft.ttf',
                                   on_release=self.dequeueAll)
        self.MfloatLayout.add_widget(self.deleteAll)
        #set up grid
        self.callGrid(None)
        
    def areYouSure(self, instance):
        layout = FloatLayout()
        #confirm deletion
        self.confirm = Button(text="confirm", pos=(450, 200), size_hint=(None, None),font_size=30, size=(150, 80),
                background_normal ="assets/icons/submitButton.png", background_down ="assets/icons/submitButtonDown.png",
                font_name='assets/icons/minecraft.ttf', on_release=self.progReset)
        layout.add_widget(self.confirm)
        #disable button for 3 seconds after popup
        self.confirm.disabled = True
        Clock.schedule_once(self.disableFalse, 1)
        #shows text
        text = Label(text="Are You Sure?\nyour current progress\nwill be deleted",
                      color=(1,1,1,1), pos=(140,230), font_size=30, font_name='assets/icons/minecraft.ttf')
        layout.add_widget(text)

        self.r = Popup(title="", content=layout,
            size_hint=(0.6,0.4), title_color=(1,1,1,1),
              title_size=10, title_font="assets/icons/minecraft.ttf")
        self.r.open()

    def progReset(self, instance):
        #set every fact value to 10
        for i in range(1,11):
            for j in range(1,11):
                mulStore[f"{i}x{j}"] = {"num": 10}
        self.resetMan(instance)
        self.confirm.disabled = True
        Clock.schedule_once(self.disableFalse, 1)
    def disableFalse(self, instance):
        self.confirm.disabled = False

    def resetMan(self, instance):
        self.gFloatLayout.clear_widgets()
        #print("all reseted")
        self.callGrid(None)

    def callGrid(self, instance):
        self.gFloatLayout = FloatLayout()
        self.add_widget(self.gFloatLayout)
        #10x10grid for holding multiplication facts
        boxSize = 40
        gridLftPad = 10
        gridBtmPad = -20
        spacing = 10
        self.all = []
        for i in range(1,11):
            row = []
            for j in range(1,11):
                #reformat for different purpose
                self.mulFacts = f"{i}x{j}"
                self.mulFacts2 = f"{i} x {j}"
                #adding buttons
                self.mulFactsBtn = Button(text="",size_hint=(None, None), size = (45,45),pos=((j)*(boxSize+spacing)+gridLftPad,
                                                   (11-i)*(boxSize+spacing)+gridBtmPad),color=(0, 0, 0, 1),background_normal = '',
                                                    on_release=partial(self.queue, fact=self.mulFacts2)) #partial stores the value of the fact when it is created initially
                self.mulFactsBtn.text = f"{i} x {j}"
                self.gFloatLayout.add_widget(self.mulFactsBtn)
                self.colourChange(self.mulFactsBtn, self.mulFacts)

            self.all.append(row)
    
    #add items to the queue
    def queue(self, instance, fact):
        global gloQueue
        #not exceeding queue length and no repeat
        if len(gloQueue) < 10 and fact not in gloQueue:
            gloQueue.append(fact)
            self.Mqueue.text = "\n".join(gloQueue)
            #print(gloQueue)
    
    def dequeue(self, instance):
        global gloQueue
        #find index of last element
        n = len(gloQueue) - 1
        #make sure the queue is not empty
        if len(gloQueue) > 0:
            gloQueue.pop(n)
            self.Mqueue.text = "\n".join(gloQueue)

    def dequeueAll(self, instance):
        global gloQueue
        gloQueue = []
        self.Mqueue.text = "\n".join(gloQueue)

    def on_enter(self, **kwargs):
        self.gFloatLayout.clear_widgets()
        self.callGrid(None)

    def colourChange(self, instance, fact):
        #stores the num as colour green
        g = mulStore.get(fact)["num"] / 10
        #when num decreases (variable g) red increases when g = 10 r = 0
        r = 1 - g
        instance.background_color = (r,g,0,1)
    
    def hint(self, instance):
        self.hLayout = FloatLayout()
        writeQ = Label(text="In the 10x10 grid, each box represents a multiplication fact.\nA green box indicates a strong accuracy ratio,"
                    " \nwhile a red box signals a lower accuracy ratio\n\nyou can queue up the next facts in the challenge\n"
                    "by clicking on the facts",
                      color=(1,1,1,1), pos=(100,200), font_size=20, markup=True)
        self.hLayout.add_widget(writeQ)

        self.h = Popup(title="", content=self.hLayout,
            size_hint=(0.75,0.75), title_color=(1,1,1,1),
              title_size=10, title_font="Roboto-Bold")
        self.h.open()

    def switch_Nav(self, instance):

        self.manager.current = "Nav" 


class MulGame(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(startScreen (name="Start"))
        sm.add_widget(NavScreen (name="Nav"))
        sm.add_widget(MulTable (name="Table"))
        sm.add_widget(Challenge (name="Challenge"))
        sm.add_widget(Management (name="Management"))
        return sm


if __name__ == "__main__":
    MulGame().run()