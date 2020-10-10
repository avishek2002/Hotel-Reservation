import kivy
import tkinter as tk
from kivy.app import App
from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
#from kivy.uix.layout import Layout
from kivy.graphics import Color,Rectangle
#from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen 
#from kivy.lang import Builder


#connector to mysql and the database part
def mysql():

    '''
    /usr/local/mysql/bin/mysql -u root -p
    '''
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002')
    cursor = mycon.cursor()
    cursor.execute('show databases;')
    databases = cursor.fetchall()
    state = 'hotel_management' in databases
    print(state)
    if state == bool("False") :
        print(state)
        cursor.execute('create database if not exists hotel_management;')
        cursor.execute('use hotel_management;')
        cursor.execute('create table member_info(member_id varchar(10) primary key not null);')
        cursor.execute('alter table member_info add(phonenumber varchar(15) not null);')
        cursor.execute('alter table member_info add(name varchar(25) not null);')
        cursor.execute('alter table member_info add(password varchar(25) not null)')
        cursor.execute('create table admin_info(admin_id varchar(10) primary key not null);')
        cursor.execute('alter table admin_info add(admin_phonenumber varchar(15) not null);')
        cursor.execute('alter table admin_info add(admin_name varchar(25) not null);')
        cursor.execute('alter table admin_info add(admin_password varchar(25) not null)')
#cursor.execute('')
mysql()

#labels beside the button (design)
class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    pass


#Home Page
class Home(Screen,FloatLayout):
    def  __init__(self,**kwargs):
        super(Home,self).__init__(**kwargs)

        with self.canvas:
            Color(1,1,0,1)
            self.rect =Rectangle(size=(3000,2000))

        self.label = Label(text="Select an option: ",font_size=75,color=(225, 225, 225, 1), size_hint =(.4,.3),
                pos_hint={"x":0.31,"top":1})
        self.add_widget(self.label)

        self.guest = Button(text="Guest", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.7})
        self.guest.bind(on_release=self.call_guest)
        self.add_widget(self.guest)

        self.member = Button(text="Member",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":0.5})
        self.member.bind(on_release=self.call_member)
        self.add_widget(self.member)

        self.admin = Button(text="Admin",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.3})
        self.admin.bind(on_release=self.call_admin)
        self.add_widget(self.admin)

        self.create = Button(text='NEW',font_size=30,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.1),pos_hint={"x":0.05,"top":.15})
        self.create.bind(on_release=self.call_create)
        self.add_widget(self.create)

        self.rooms = Button(text='ROOMS', font_size=30, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                         size_hint=(.15, .1), pos_hint={"x": 0.8, "top": .15})
        self.rooms.bind(on_release=self.call_rooms)
        self.add_widget(self.rooms)

    def call_guest(self,instances):
        sm.transition.direction = 'left'
        sm.current = 'GuestReservation'
    def call_member(self,instances):
        sm.transition.direction = 'left'
        sm.current = 'MemberLogin'
    def call_admin(self,instances):
        sm.transition.direction = 'left'
        sm.current = 'AdminLogin'
    def call_create(self,instances):
        sm.transition.direction = 'up'
        sm.current = 'Create'
    def call_rooms(self,instances):
        sm.transition.direction = 'up'
        sm.current = 'Rooms'
    pass


#Create Account Page
class Create(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Create, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Account Creation Page", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.createmember = Button(text="Become a member", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.4, .15), pos_hint={"x": 0.3, "top": .55})
        self.createmember.bind(on_release=self.call_createmember)
        self.add_widget(self.createmember)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self,instances):
        sm.transition.direction='right'
        sm.current='Home'
    def call_createmember(self,instances):
        sm.transition.direction='left'
        sm.current='Createmember'
    pass


#Rooms
class Rooms(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Rooms, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Room Selection", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self,instances):
        sm.transition.direction='right'
        sm.current='Home'
    pass


#Guest reservation
class GuestReservation(Screen,FloatLayout):
        def __init__(self,**kwargs):
                super(GuestReservation,self).__init__(**kwargs)

                with self.canvas:
                        Color(1,1,0,1)
                        self.rect=Rectangle(size=(3000,2000))

                self.label = Label(text="Guest Registration",font_size=75,color=(225, 225, 225, 1), size_hint =(.4,.3),
                pos_hint={"x":0.31,"top":1})
                self.add_widget(self.label)

                self.name_label = MyLabel(text="Name",font_size=40,color=(225,225,1,1),size_hint=(.35,.05),
                pos_hint={"x":0.15,"top":0.8})
                self.add_widget(self.name_label)
                self.nameofguest = TextInput(multiline=False,font_size=40,size_hint=(.35,.05),
                pos_hint={"x":0.5,"top":0.8})
                self.add_widget(self.nameofguest)

                self.phone_label = MyLabel(text="Phone Number", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                pos_hint={"x": 0.15, "top": 0.7})
                self.add_widget(self.phone_label)
                self.phoneofguest = TextInput(multiline=False,font_size=40, size_hint=(.35, .05),
                pos_hint={"x": 0.5, "top": 0.7})
                self.add_widget(self.phoneofguest)

                self.roomno_label = MyLabel(text="Room Type", font_size=40, color=(225, 225,1, 1), size_hint=(.35, .05),
                pos_hint={"x": 0.15, "top": 0.6})
                self.add_widget(self.roomno_label)
                self.roomnoofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                pos_hint={"x": 0.5, "top": 0.6})
                self.add_widget(self.roomnoofguest)

                self.noofguests_label = MyLabel(text="Number of Guests", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                pos_hint={"x": 0.15, "top": 0.5})
                self.add_widget(self.noofguests_label)
                self.noofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                pos_hint={"x": 0.5, "top": 0.5})
                self.add_widget(self.noofguest)

                self.checkin_label = MyLabel(text="Check-in Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                pos_hint={"x": 0.15, "top": 0.4})
                self.add_widget(self.checkin_label)
                self.checkinofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                pos_hint={"x": 0.5, "top": 0.4})
                self.add_widget(self.checkinofguest)

                self.home = Button(text="Home",font_size=25,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.025),pos_hint={"x":0.01,"top":.99})
                self.home.bind(on_release=self.call_home)
                self.add_widget(self.home)

                self.submit = Button(text="Submit  form as Guest",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.3})
                self.add_widget(self.submit)


        def call_home(self,instances):
                sm.transition.direction='right'
                sm.current='Home'

        pass


#Member login and reservation and signup
class MemberLogin(Screen,FloatLayout):
        def __init__(self,**kwargs):
                super(MemberLogin,self).__init__(**kwargs)

                with self.canvas:
                        Color(1,1,0,1)
                        self.rect=Rectangle(size=(3000,2000))
                        
                self.label = Label(text="Member Login",font_size=75,color=(225, 225, 225, 1), size_hint =(.4,.3),
                pos_hint={"x":0.31,"top":1})
                self.add_widget(self.label)

                self.email_label = MyLabel(text="Login Email", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                          pos_hint={"x": 0.15, "top": 0.8})

                self.add_widget(self.email_label)
                self.emailofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                             pos_hint={"x": 0.5, "top": 0.8})
                self.add_widget(self.emailofguest)

                self.password_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1),
                                           size_hint=(.35, .05),
                                           pos_hint={"x": 0.15, "top": 0.7})
                self.add_widget(self.password_label)
                self.passwordofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                              pos_hint={"x": 0.5, "top": 0.7})
                self.add_widget(self.passwordofguest)

                self.home = Button(text="Home",font_size=25,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.025),pos_hint={"x":0.01,"top":.99})
                self.home.bind(on_release=self.call_home)
                self.add_widget(self.home)

                self.memberregistration = Button(text="Login",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.3})
                self.memberregistration.bind(on_release=self.call_memberreservation)
                self.add_widget(self.memberregistration)

        def call_home(self,instances):
                sm.transition.direction='right'
                sm.current='Home'
        def call_memberreservation(self,instances):
                sm.transition.direction='left'
                sm.current='MemberReservation'
        pass

class MemberReservation(Screen,FloatLayout):
        def __init__(self,**kwargs):
                super(MemberReservation,self).__init__(**kwargs)

                with self.canvas:
                        Color(1,1,0,1)
                        self.rect=Rectangle(size=(3000,2000))

                self.label = Label(text='Member Reservation',font_size=75,color=(225,225,225,1),size_hint=(.4,.3),
                pos_hint={'x':0.31,'top':1})
                self.add_widget(self.label)

                self.name_label = MyLabel(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                          pos_hint={"x": 0.15, "top": 0.8})
                self.add_widget(self.name_label)
                self.nameofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                             pos_hint={"x": 0.5, "top": 0.8})
                self.add_widget(self.nameofguest)

                self.phone_label = MyLabel(text="Phone Number", font_size=40, color=(225, 225, 1, 1),
                                           size_hint=(.35, .05),
                                           pos_hint={"x": 0.15, "top": 0.7})
                self.add_widget(self.phone_label)
                self.phoneofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                              pos_hint={"x": 0.5, "top": 0.7})
                self.add_widget(self.phoneofguest)

                self.roomno_label = MyLabel(text="Room Type", font_size=40, color=(225, 225, 1, 1),
                                            size_hint=(.35, .05),
                                            pos_hint={"x": 0.15, "top": 0.6})
                self.add_widget(self.roomno_label)
                self.roomnoofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                               pos_hint={"x": 0.5, "top": 0.6})
                self.add_widget(self.roomnoofguest)

                self.noofguests_label = MyLabel(text="Number of Guests", font_size=40, color=(225, 225, 1, 1),
                                                size_hint=(.35, .05),
                                                pos_hint={"x": 0.15, "top": 0.5})
                self.add_widget(self.noofguests_label)
                self.noofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                           pos_hint={"x": 0.5, "top": 0.5})
                self.add_widget(self.noofguest)

                self.checkin_label = MyLabel(text="Check-in Date", font_size=40, color=(225, 225, 1, 1),
                                             size_hint=(.35, .05),
                                             pos_hint={"x": 0.15, "top": 0.4})
                self.add_widget(self.checkin_label)
                self.checkinofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                                pos_hint={"x": 0.5, "top": 0.4})
                self.add_widget(self.checkinofguest)

                self.memberlogin = Button(text="Home",font_size=25,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.025),pos_hint={"x":0.01,"top":.99})
                self.memberlogin.bind(on_release=self.call_memberlogin)
                self.add_widget(self.memberlogin)

                self.submit = Button(text="Submit  form as Member",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.3})
                self.add_widget(self.submit)

        def call_memberlogin(self,instances):
                sm.transition.direction = 'right'
                sm.current = 'Home'
        pass

class Createmember(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(Createmember, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Member Sign Up", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.name_label = MyLabel(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.name_label)
        self.nameofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                     pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.nameofmember)

        self.phone_label = MyLabel(text="Phone Number", font_size=40, color=(225, 225, 1, 1),
                                   size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.phone_label)
        self.phoneofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.phoneofmember)

        self.pass_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1),
                                    size_hint=(.35, .05),
                                    pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.pass_label)
        self.passofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.passofmember)

        self.pass2_label = MyLabel(text="Confirm password", font_size=40, color=(225, 225, 1, 1),
                                        size_hint=(.35, .05),
                                        pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.pass2_label)
        self.pass2ofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                   pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.pass2ofmember)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.submit = Button(text="Done", font_size=40, background_color=(0, 225, 225, 1),
                                        color=(225, 225, 225, 1),
                                        size_hint=(.4, .15), pos_hint={"x": 0.3, "top": .3})
        #self.submit.bind(on_release=self.call_home)
        self.add_widget(self.submit)


    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'Home'
    pass

#Admin Login
class AdminLogin(Screen,FloatLayout):
        def __init__(self,**kwargs):
                super(AdminLogin,self).__init__(**kwargs)

                with self.canvas:
                        Color(1,1,0,1)
                        self.rect=Rectangle(size=(3000,2000))

                self.label = Label(text="Admin Login",font_size=75,color=(225, 225, 225, 1), size_hint =(.4,.3),
                pos_hint={"x":0.31,"top":1})
                self.add_widget(self.label)

                self.email_label = MyLabel(text="Login Email", font_size=40, color=(225, 225, 1, 1),
                                           size_hint=(.35, .05),
                                           pos_hint={"x": 0.15, "top": 0.8})
                self.add_widget(self.email_label)
                self.emailofadmin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                              pos_hint={"x": 0.5, "top": 0.8})
                self.add_widget(self.emailofadmin)

                self.password_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1),
                                              size_hint=(.35, .05),
                                              pos_hint={"x": 0.15, "top": 0.7})
                self.add_widget(self.password_label)
                self.passwordofadmin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                                 pos_hint={"x": 0.5, "top": 0.7})
                self.add_widget(self.passwordofadmin)

                self.home = Button(text="Home",font_size=25,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.025),pos_hint={"x":0.01,"top":.99})
                self.home.bind(on_release=self.call_home)
                self.add_widget(self.home)

                self.adminconfirmation = Button(text="Login",font_size=40,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.4,.15),pos_hint={"x":0.3,"top":.3})
                self.adminconfirmation.bind(on_release=self.call_adminconfirmation)
                self.add_widget(self.adminconfirmation)

        def call_home(self,instances):
                sm.transition.direction='right'
                sm.current='Home'
        def call_adminconfirmation(self,instances):
                sm.transition.direction='left'
                sm.current='AdminConfirmation'
        pass

class AdminConfirmation(Screen,FloatLayout):
        def __init__(self,**kwargs):
                super(AdminConfirmation,self).__init__(**kwargs)

                with self.canvas:
                        Color(1,1,0,1)
                        self.rect=Rectangle(size=(3000,2000))

                self.label = Label(text='Admin Confirmation',font_size=75,color=(225,225,225,1),size_hint=(.4,.3),
                pos_hint={'x':0.31,'top':1})
                self.add_widget(self.label)

                self.home = Button(text="Home",font_size=25,background_color=(0,225,225,1),color=(225,225,225,1),
                size_hint =(.15,.025),pos_hint={"x":0.01,"top":.99})
                self.home.bind(on_release=self.call_home)
                self.add_widget(self.home)

        def call_home(self,instances):
                sm.transition.direction = 'right'
                sm.current = 'Home'
        pass



#Screen manager
sm = ScreenManager()
sm.add_widget(Home(name='Home'))
sm.add_widget(Create(name='Create'))
sm.add_widget(Rooms(name='Rooms'))
sm.add_widget(GuestReservation(name='GuestReservation'))
sm.add_widget(MemberLogin(name='MemberLogin'))
sm.add_widget(MemberReservation(name='MemberReservation'))
sm.add_widget(Createmember(name='Createmember'))
sm.add_widget(AdminLogin(name='AdminLogin'))
sm.add_widget(AdminConfirmation(name='AdminConfirmation'))




class HotelReservationApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    HotelReservationApp().run()




