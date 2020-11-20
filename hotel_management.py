import kivy
import time
# from kivy.lang import Builder
# from kivy.base import runTouchApp
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# from kivy.uix.layout import Layout
from kivy.graphics import Color, Rectangle
# from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup


"""
/usr/local/mysql/bin/mysql -u root -p
"""


# creating database if not exists
def mysql():

    """
    /usr/local/mysql/bin/mysql -u root -p
    """
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002')
    cursor = mycon.cursor()
    cursor.execute('show databases;')
    databases = cursor.fetchall()
    condition = ''
    for database in databases:
        if "hotel_management" == database[0]:
            condition = "Exists"
            break
        else:
            condition = "Does not exist"
    if condition != "Exists":
        cursor.execute('create database if not exists hotel_management;')
        cursor.execute('use hotel_management;')

        cursor.execute('create table admin_info(admin_id varchar(10) primary key not null);')
        cursor.execute('alter table admin_info add(admin_phonenumber varchar(15) not null);')
        cursor.execute('alter table admin_info add(admin_email varchar(50) not null);')
        cursor.execute('alter table admin_info add(admin_name varchar(25) not null);')
        cursor.execute('alter table admin_info add(admin_password varchar(25) not null)')

        cursor.execute('create table member_info (member_id varchar(10) primary key not null);')
        cursor.execute('alter table member_info add(member_phonenumber varchar(15) not null);')
        cursor.execute('alter table member_info add(member_email varchar(50) not null);')
        cursor.execute('alter table member_info add(member_name varchar(25) not null);')
        cursor.execute('alter table member_info add(member_password varchar(25) not null);')
        cursor.execute('alter table member_info add(member_points int(5) not null);')

        cursor.execute('create table rooms (room_no varchar(5) primary key not null);')
        cursor.execute("alter table rooms add(room_type varchar(25) not null);")
        cursor.execute('alter table rooms add(room_availability char(1));')
        cursor.execute('alter table rooms add(room_capacity int(2) not null);')
        cursor.execute('alter table rooms add(room_price int(5) not null);')

        cursor.execute('create table booked_rooms(room_no varchar(5) not null);')
        cursor.execute('alter table booked_rooms add(foreign key(room_no) references rooms(room_no));')
        cursor.execute('alter table booked_rooms add(id varchar(10) not null);')
        cursor.execute('alter table booked_rooms add(foreign key(id) references member_info(member_id));')
        cursor.execute('alter table booked_rooms add(phonenumber varchar(15) not null);')
        cursor.execute('alter table booked_rooms add(email varchar(50) not null);')
        cursor.execute('alter table booked_rooms add(name varchar(25) not null);')
        cursor.execute('alter table booked_rooms add(check_in date not null);')
        cursor.execute('alter table booked_rooms add(check_out date not null);')

        cursor.execute('create table requested_rooms(room_type varchar(25) not null);')
        cursor.execute('alter table requested_rooms add(id varchar(10) not null);')
        cursor.execute('alter table requested_rooms add(phonenumber varchar(15) not null);')
        cursor.execute('alter table requested_rooms add(name varchar(25) not null);')
        cursor.execute('alter table requested_rooms add(no_guests int(2) not null);')
        cursor.execute('alter table requested_rooms add(check_in date not null);')
        cursor.execute('alter table requested_rooms add(check_out date not null);')
        mycon.commit()
        mycon.close()
    else:
        print("Database 'hotel_management' exists.")


mysql()


# getting available rooms
def available_rooms():
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute('use hotel_management;')
    cursor.execute("select * from rooms;")
    rooms = cursor.fetchall()
    mycon.close()
    return rooms


# getting requested rooms
def requested_rooms():
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute('use hotel_management;')
    cursor.execute("select * from requested_rooms;")
    rooms = cursor.fetchall()
    mycon.close()
    return rooms


# getting booked rooms
def booked_rooms():
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute('use hotel_management;')
    cursor.execute("select * from booked_rooms;")
    rooms = cursor.fetchall()
    mycon.close()
    return rooms


# getting admin information
def admin_info():
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute('use hotel_management;')
    cursor.execute("select * from admin_info;")
    data = cursor.fetchall()
    mycon.close()
    return data


# getting member information
def member_info():
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute('use hotel_management;')
    cursor.execute("select * from member_info;")
    data = cursor.fetchall()
    mycon.close()
    return data


# incorrect login details
def popup_incorrect():

    # incorrect login details screen
    class popup_incorrect_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_incorrect_screen, self).__init__(**kwargs)

            self.label = Label(text="ID or Password is incorrect!", font_size=50, color=(1, 0, 0, 1),
                               size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Try Again", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            popupWindow.dismiss()

        pass

    show = popup_incorrect_screen()

    popupWindow = Popup(title="Login Error", content=show, size_hint=(None, None), size=(650, 600),
                        pos=(0, 0), auto_dismiss=False)

    popupWindow.open()


# invalid room reservation submission
def popup_invalid_submission():

    # invalid room reservation submission screen
    class popup_invalid_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_invalid_screen, self).__init__(**kwargs)

            self.label = Label(text="The text boxes must not be left empty and must be in correct format!",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Re-try submitting form", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            invalidWindow.dismiss()

        pass

    show = popup_invalid_screen()

    invalidWindow = Popup(title="Submission Error", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    invalidWindow.open()


# valid room reservation submission
def popup_valid_submission():

    # valid room reservation submission screen
    class popup_valid_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_valid_screen, self).__init__(**kwargs)

            self.label = Label(text="Successfully sent request for room reservation!",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Return to Home Screen", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            validWindow.dismiss()

        pass

    show = popup_valid_screen()

    validWindow = Popup(title="Submission success", content=show, size_hint=(None, None), size=(650, 600),
                        pos=(0, 0), auto_dismiss=False)

    validWindow.open()


# confirm reservations as Admin
def popup_confirm():

    # confirm reservation screen
    class popup_confirm_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_confirm_screen, self).__init__(**kwargs)

            self.label = Label(text="Confirmed reservations for the selected rooms!",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Return to your Page", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            confirmWindow.dismiss()

        pass

    show = popup_confirm_screen()

    confirmWindow = Popup(title="Confirmation success", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    confirmWindow.open()


# creating member account
def create_member(ID, phone_number, email, name, password):
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute("insert into member_info(member_id,member_phonenumber,member_email,member_name,"
                   "member_password, member_points) values('{}','{}','{}','{}','{}',{})"
                   .format(ID, phone_number, email, name, password, 0))
    mycon.commit()
    mycon.close()
    return


# member account created
def popup_account_created():

    # member account created screen
    class account_created_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(account_created_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Member Account has been successfully created!",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            accountWindow.dismiss()
            sm.transition.direction = 'right'
            sm.current = 'Home'

        pass

    show = account_created_screen()

    accountWindow = Popup(title="Account Created", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    accountWindow.open()


# member account creation failure
def popup_account_notcreated():

    # member account creation failure screen
    class account_notcreated_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(account_notcreated_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Member Account could not be processed!",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Try Again", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            failureWindow.dismiss()

        pass

    show = account_notcreated_screen()

    failureWindow = Popup(title="ERROR", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    failureWindow.open()


# inserting value into requested_rooms as guest
def request_room(name, phone, room_type, noofquests, check_in, check_out):
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute("insert into requested_rooms(room_type,id,phonenumber,name,no_guests,check_in,check_out)"
                   "values('{}','{}','{}','{}',{},'{}','{}')"
                   .format(room_type, 'GUEST', phone, name, noofquests, check_in, check_out))
    mycon.commit()
    return


# inserting value into requested_rooms as member
def request_room_asmember(ID, room_type, noofquests, check_in, check_out):
    import mysql.connector
    mycon = mysql.connector.connect(user='root', password='avishek2002', database='hotel_management')
    cursor = mycon.cursor()
    cursor.execute("select * from member_info where member_id = '{}';".format(ID))
    data = cursor.fetchall()
    phone = data[0][1]
    name = data[0][3]
    cursor.execute("insert into requested_rooms(room_type,id,phonenumber,name,no_guests,check_in,check_out)"
                   "values('{}','{}','{}','{}',{},'{}','{}')"
                   .format(room_type, ID, phone, name, noofquests, check_in, check_out))
    mycon.commit()
    return


# labels beside the button (design)
class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    pass


# Home page
class Home(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Select an option: ", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.guest = Button(text="Guest", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                            size_hint=(.4, .15), pos_hint={"x": 0.3, "top": .7})
        self.guest.bind(on_release=self.call_guest)
        self.add_widget(self.guest)

        self.member = Button(text="Member", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                             size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.5})
        self.member.bind(on_release=self.call_member)
        self.add_widget(self.member)

        self.admin = Button(text="Admin", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                            size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.admin.bind(on_release=self.call_admin)
        self.add_widget(self.admin)

        self.create = Button(text='NEW', font_size=30, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                             size_hint=(.15, .1), pos_hint={"x": 0.05, "top": 0.15})
        self.create.bind(on_release=self.call_create)
        self.add_widget(self.create)

        self.rooms = Button(text='ROOMS', font_size=30, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                            size_hint=(.15, .1), pos_hint={"x": 0.8, "top": .15})
        self.rooms.bind(on_release=self.call_rooms)
        self.add_widget(self.rooms)

    def call_guest(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'GuestReservation'

    def call_member(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'MemberLogin'

    def call_admin(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'AdminLogin'

    def call_create(self, instances):
        sm.transition.direction = 'up'
        sm.current = 'Create'

    def call_rooms(self, instances):
        sm.transition.direction = 'up'
        sm.current = 'Rooms'
    pass


# Create account screen (middle screen for Member signup screen)
class Create(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Create, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Account Creation Page", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.createmember = Button(text="Become a member", font_size=40, background_color=(0, 225, 225, 1),
                                   color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.55})
        self.createmember.bind(on_release=self.call_createmember)
        self.add_widget(self.createmember)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self, instances):
        sm.transition.direction = 'down'
        sm.current = 'Home'

    def call_createmember(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'Createmember'
    pass


# Rooms screen
class Rooms(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(Rooms, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Room Selection", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        x = [0.2, 0.35, 0.5, 0.65, 0.8]
        top = 0.75
        header_string = ['Room No.', 'Room Type', 'Available', 'Capacity', 'Price(¥)']
        for i in range(0, len(header_string)):
            self.header = Label(text=header_string[i], font_size=40, color=(225, 225, 225, 1), size_hint=(0, 0),
                                pos_hint={'x': x[i], 'top': top})
            self.add_widget(self.header)

        rooms = available_rooms()
        x = [0.2, 0.35, 0.5, 0.65, 0.8]
        top = 0.7
        for room in rooms:
            for i in range(0, len(room)):
                self.room = Label(text=str(room[i]), font_size=25, color=(225, 225, 225, 1),  size_hint=(.0, .0),
                                  pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.room)
            top -= .05

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self, instances):
        sm.transition.direction = 'down'
        sm.current = 'Home'
    pass


# Booked rooms screen
class BookedRooms(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(BookedRooms, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Booked Rooms", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        x = [0.1, 0.175, 0.3, 0.45, 0.6, 0.75, 0.9]
        top = 0.75
        header_string = ['Room No.', 'ID', 'Phone Number', 'Email', 'Name', 'Check-in', 'Check-out']
        for i in range(0, len(header_string)):
            self.header = Label(text=header_string[i], font_size=40, color=(225, 225, 225, 1), size_hint=(0, 0),
                                pos_hint={'x': x[i], 'top': top})
            self.add_widget(self.header)

        rooms = booked_rooms()
        x = [0.1, 0.175, 0.3, 0.45, 0.6, 0.75, 0.9]
        top = 0.7
        for room in rooms:
            for i in range(0, len(room)):
                self.room = Label(text=str(room[i]), font_size=25, color=(225, 225, 225, 1),  size_hint=(.0, .0),
                                  pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.room)
            top -= .05

        self.home = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'AdminConfirmation'
    pass


# Guest reservation screen
class GuestReservation(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(GuestReservation, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Guest Reservation", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.name_label = MyLabel(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.name_label)
        self.nameofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                     pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.nameofguest)

        self.phone_label = MyLabel(text="Phone Number", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.phone_label)
        self.phoneofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.phoneofguest)

        self.room_label = MyLabel(text="Room Type", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.room_label)
        self.roomofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                     pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.roomofguest)

        self.noofguests_label = MyLabel(text="Number of Guests", font_size=40, color=(225, 225, 1, 1),
                                        size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.5})
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

        self.checkout_label = MyLabel(text="Check-in Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                      pos_hint={"x": 0.15, "top": 0.3})
        self.add_widget(self.checkout_label)
        self.checkoutofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                         pos_hint={"x": 0.5, "top": 0.3})
        self.add_widget(self.checkoutofguest)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.submit = Button(text="Submit  form as Guest", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.2})
        self.submit.bind(on_release=self.guest_submit)
        self.add_widget(self.submit)

    def call_home(self, instances):
        self.nameofguest.text = ""
        self.phoneofguest.text = ""
        self.roomofguest.text = ""
        self.checkinofguest.text = ""
        self.checkoutofguest.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def guest_submit(self, instances):
        name = self.nameofguest.text
        phone = self.phoneofguest.text
        room_type = self.roomofguest.text
        noofquests = self.noofguest.text
        check_in = self.checkinofguest.text
        check_out = self.checkoutofguest.text
        if name != "" and phone != "" and room_type != "" and noofquests != "" and check_in != "" and check_out != "":
            request_room(name, phone, room_type, noofquests, check_in, check_out)
            popup_valid_submission()
        else:
            popup_invalid_submission()
        self.nameofguest.text = ""
        self.phoneofguest.text = ""
        self.roomofguest.text = ""
        self.checkinofguest.text = ""
        self.checkoutofguest.text = ""
    pass


# Member login screen
class MemberLogin(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(MemberLogin, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))
                        
        self.label = Label(text="Member Login", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.id_label = MyLabel(text="Member ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.65})
        self.add_widget(self.id_label)
        self.idofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                   pos_hint={"x": 0.5, "top": 0.65})
        self.add_widget(self.idofguest)

        self.password_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                      pos_hint={"x": 0.15, "top": 0.55})
        self.add_widget(self.password_label)
        self.passwordofguest = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                         pos_hint={"x": 0.5, "top": 0.55})
        self.add_widget(self.passwordofguest)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.memberregistration = Button(text="Login", font_size=40, background_color=(0, 225, 225, 1),
                                         color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.memberregistration.bind(on_release=self.call_memberreservation)
        self.add_widget(self.memberregistration)

    def call_home(self, instances):
        self.idofguest.text = ""
        self.passwordofguest.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_memberreservation(self, instances):
        ID = self.idofguest.text
        password = self.passwordofguest.text
        memberinfo = member_info()
        state = ''
        for member in memberinfo:
            if ID in member and password in member:
                sm.transition.direction = 'left'
                sm.current = 'MemberReservation'
                state = 'correct'
                break
            else:
                state = 'incorrect'
        if state == 'incorrect':
            popup_incorrect()
        self.idofguest.text = ""
        self.passwordofguest.text = ""
    pass


# Member reservation screen
class MemberReservation(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(MemberReservation, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text='Member Reservation', font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={'x': 0.31, 'top': 1})
        self.add_widget(self.label)

        self.id_label = MyLabel(text="Member ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.id_label)
        self.idofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                    pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.idofmember)

        self.room_label = MyLabel(text="Room Type", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.room_label)
        self.room = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.room)

        self.noofguests_label = MyLabel(text="Number of Guests", font_size=40, color=(225, 225, 1, 1),
                                        size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.noofguests_label)
        self.noofguests = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                    pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.noofguests)

        self.checkin_label = MyLabel(text="Check-in Date", font_size=40, color=(225, 225, 1, 1),
                                     size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.checkin_label)
        self.checkin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                 pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.checkin)

        self.checkout_label = MyLabel(text="Check-out Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                      pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.checkout_label)
        self.checkout = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                  pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.checkout)

        self.memberlogin = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1),
                                  color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.memberlogin.bind(on_release=self.call_memberlogin)
        self.add_widget(self.memberlogin)

        self.member_submit = Button(text="Submit form as Member", font_size=40, background_color=(0, 225, 225, 1),
                                    color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.member_submit.bind(on_release=self.submit)
        self.add_widget(self.member_submit)

    def call_memberlogin(self, instances):
        self.idofmember.text = ""
        self.room.text = ""
        self.noofguests.text = ""
        self.checkin.text = ""
        self.checkout.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def submit(self, instances):
        ID = self.idofmember.text
        room_type = self.room.text
        noofquests = self.noofguests.text
        check_in = self.checkin.text
        check_out = self.checkout.text
        if ID != "" and room_type != "" and noofquests != "" and check_in != "" and check_out != "":
            request_room_asmember(ID, room_type, noofquests, check_in, check_out)
            popup_valid_submission()
        else:
            popup_invalid_submission()
        self.idofmembert.text = ""
        self.room.text = ""
        self.noofguests.text = ""
        self.checkin.text = ""
        self.checkout.text = ""
    pass


# Member signup screen
class Createmember(Screen, FloatLayout):
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

        self.email_label = MyLabel(text="Email", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.email_label)
        self.emailofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.emailofmember)

        self.pass_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.pass_label)
        self.passofmember = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.passofmember)

        self.pass2_label = MyLabel(text="Confirm Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.pass2_label)
        self.pass2ofmember = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.pass2ofmember)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.submit = Button(text="Done", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                             size_hint=(.4, .15), pos_hint={"x": 0.3, "top": .3})
        self.submit.bind(on_release=self.call_create_member)
        self.add_widget(self.submit)

    def call_home(self, instances):
        self.nameofmember.text = ""
        self.phoneofmember.text = ""
        self.emailofmember.text = ""
        self.passofmember.text = ""
        self.pass2ofmember.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_create_member(self, instances):
        name = self.nameofmember.text
        phone_number = self.phoneofmember.text
        email = self.emailofmember.text
        password = self.passofmember.text
        password_check = self.pass2ofmember.text
        data = member_info()
        member_id = ''
        for member in data:
            member_id = member[0]
        ID = member_id[0]
        for i in range(1, 4):
            if int(member_id[i]) == 9:
                ID += str(int(member_id[i-1])+1)
            elif int(member_id[i]) != 0:
                ID += str(int(member_id[i])+1)
            else:
                ID += str(int(member_id[i]) + 0)
        if name != '' and phone_number != '' and email != '' and password != '' and password == password_check:
            create_member(ID, phone_number, email, name, password)
            popup_account_created()
        else:
            popup_account_notcreated()
        self.nameofmember.text = ""
        self.phoneofmember.text = ""
        self.emailofmember.text = ""
        self.passofmember.text = ""
        self.pass2ofmember.text = ""
    pass


# Admin login screen
class AdminLogin(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(AdminLogin, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Admin Login", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        self.id_label = MyLabel(text="Admin ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.65})
        self.add_widget(self.id_label)
        self.idofadmin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                   pos_hint={"x": 0.5, "top": 0.65})
        self.add_widget(self.idofadmin)

        self.password_label = MyLabel(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                      pos_hint={"x": 0.15, "top": 0.55})
        self.add_widget(self.password_label)
        self.passwordofadmin = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                         pos_hint={"x": 0.5, "top": 0.55})
        self.add_widget(self.passwordofadmin)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.adminconfirmation = Button(text="Login", font_size=40, background_color=(0, 225, 225, 1),
                                        color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.adminconfirmation.bind(on_release=self.call_adminconfirmation)
        self.add_widget(self.adminconfirmation)

    def call_home(self, instances):
        self.idofadmin.text = ""
        self.passwordofadmin.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_adminconfirmation(self, instances):
        ID = self.idofadmin.text
        password = self.passwordofadmin.text
        admininfo = admin_info()
        state = ''
        for admin in admininfo:
            if ID in admin and password in admin:
                sm.transition.direction = 'left'
                sm.current = 'AdminConfirmation'
                state = 'correct'
                break
            else:
                state = 'incorrect'
        if state == 'incorrect':
            popup_incorrect()
        self.idofadmin.text = ""
        self.passwordofadmin.text = ""
    pass


# Admin room confirmation screen
class AdminConfirmation(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(AdminConfirmation, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text='Admin Confirmation', font_size=75, color=(225, 225, 225, 1),
                           size_hint=(.4, .3), pos_hint={'x': 0.31, 'top': 1})
        self.add_widget(self.label)

        x = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
        top = 0.75
        header_string = ['Room Type', 'ID', 'Phone No.', 'Name', 'No. of guests', 'Check-in', 'Check-out', 'Approve']
        for i in range(0, len(header_string)):
            self.header = Label(text=header_string[i], font_size=30, color=(225, 225, 225, 1), size_hint=(0, 0),
                                pos_hint={'x': x[i], 'top': top})
            self.add_widget(self.header)

        requested = requested_rooms()
        x = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
        top = 0.7
        for request in requested:
            for i in range(0, len(request)):
                self.value = MyLabel(text=str(request[i]), font_size=25, color=(225, 225, 225, 1), size_hint=(.0, .0),
                                     pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.value)
            self.check = CheckBox(size_hint=(.02, .02), pos_hint={'x': x[7], 'top': top + 0.01}, active=False)
            self.add_widget(self.check)

            top -= 0.05

        self.submit = Button(text="Confirm reservation", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1),
                           color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.view = Button(text="Booked rooms", font_size=25, background_color=(0, 225, 225, 1),
                           color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.81, "top": 0.99})
        self.view.bind(on_release=self.call_booked)
        self.add_widget(self.view)

    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_booked(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'BookedRooms'

    def call_confirm(self, instances):
        popup_confirm()
    pass


# Screen manager
sm = ScreenManager()
sm.add_widget(Home(name='Home'))
sm.add_widget(Create(name='Create'))
sm.add_widget(Rooms(name='Rooms'))
sm.add_widget(BookedRooms(name='BookedRooms'))
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
