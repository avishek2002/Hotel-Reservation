import random
import mysql.connector as connector
from datetime import datetime, date
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown


"""
/usr/local/mysql/bin/mysql -u root -p
"""


# creating database if not exists
def mysql():
    mycon = connector.connect(user='root', password='avishek2002')
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

        cursor.execute("create table checked_in(room_no varchar(5) not null);")
        cursor.execute("alter table checked_in add(id varchar(10) not null);")
        cursor.execute("alter table checked_in add(name varchar(25) not null);")
        cursor.execute("alter table checked_in add(checked_in date not null);")
        cursor.execute("alter table checked_in add(check_out date not null);")
        mycon.commit()
        mycon.close()
    else:
        return


mysql()


mycon = connector.connect(user='root', password='avishek2002', database='hotel_management')
cursor = mycon.cursor()


# getting available rooms
def available_rooms():
    cursor.execute("select * from rooms;")
    rooms = cursor.fetchall()
    return rooms


# getting requested rooms
def requested_rooms():
    cursor.execute("select * from requested_rooms;")
    rooms = cursor.fetchall()
    return rooms


# getting booked rooms
def booked_rooms():
    cursor.execute("select * from booked_rooms;")
    rooms = cursor.fetchall()
    return rooms


# getting checked in rooms
def checked_rooms():
    cursor.execute("select * from checked_in;")
    rooms = cursor.fetchall()
    return rooms


# getting room type
def room_types():
    cursor.execute("select distinct(room_type) from rooms;")
    room_type = cursor.fetchall()
    return room_type


# getting admin information
def admin_info():
    cursor.execute("select * from admin_info;")
    data = cursor.fetchall()
    return data


# getting member information
def member_info():
    cursor.execute("select * from member_info;")
    data = cursor.fetchall()
    return data


# incorrect login details
def popup_incorrect():

    # incorrect login details screen
    class popup_incorrect_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_incorrect_screen, self).__init__(**kwargs)

            self.label = Label(text="ID or Password is incorrect!", font_size=50, color=(1, 0, 0, 1),
                               size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75}, text_size=(600, None),
                               halign="center")
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
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75},
                               text_size=(600, None), halign="center")
            self.add_widget(self.label)

            self.back = Button(text="Re-try submitting form", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.42, .15), pos_hint={"x": 0.3, "top": 0.3})
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

            self.label = Label(text="Successfully sent request for room reservation!", text_size=(600, None),
                               halign="center", font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2),
                               pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Return to Home Screen", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            validWindow.dismiss()
            sm.transition.direction = 'right'
            sm.current = 'Home'
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

            self.label = Label(text="Confirmed reservations for the selected rooms!", text_size=(600, None),
                               halign="center", font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2),
                               pos_hint={"x": 0.3, "top": .75})
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


# deleteing reservations as Admin
def popup_confirm_delete():

    # delete reservation screen
    class popup_confirm_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(popup_confirm_screen, self).__init__(**kwargs)

            self.label = Label(text="Deleted reservations for the selected rooms!", text_size=(600, None),
                               halign="center", font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2),
                               pos_hint={"x": 0.3, "top": .75})
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

    confirmWindow = Popup(title="Deletion success", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    confirmWindow.open()


# generating admin id
def makeid():
    cursor.execute('select admin_id from admin_info;')
    data = cursor.fetchall()
    if data != "":
        ID = 'A'
        while True:
            for i in range(0, 3):
                ID += str(random.randrange(0, 10))
            if ID not in data:
                break
            else:
                continue
    else:
        ID = "A001"
    return ID


# creating admin acoount
def create_admin(id_, phone, email, name, password):
    cursor.execute("insert into admin_info(admin_id,admin_phonenumber,admin_email,admin_name,admin_password) "
                   "values('{}','{}','{}','{}','{}')".format(id_, phone, email, name, password))
    mycon.commit()
    return


# deleting admin account
def adminaccountdelete(admin_identifier):
    cursor.execute("delete from admin_info where admin_id = '{}'".format(admin_identifier))
    mycon.commit()
    return


# generating member id
def makememberid():
    cursor.execute('select member_id from member_info;')
    data = cursor.fetchall()
    if data != "":
        ID = 'M'
        while True:
            for i in range(0,3):
                ID += str(random.randrange(0,10))
            if ID not in data:
                break
            else:
                continue
    else:
        ID = "M001"
    return ID


# creating member account
def create_member(ID, phone_number, email, name, password):
    cursor.execute("insert into member_info(member_id,member_phonenumber,member_email,member_name,"
                   "member_password) values('{}','{}','{}','{}','{}')"
                   .format(ID, phone_number, email, name, password))
    mycon.commit()
    return


# deleting member account and its data
def member_delete(ID):
    cursor.execute("set foreign_key_checks = 0")
    cursor.execute("delete from member_info where member_id='{}'".format(ID))
    cursor.execute("delete from requested_rooms where id = '{}'".format(ID))
    cursor.execute("delete from booked_rooms where id = '{}'".format(ID))
    cursor.execute("set foreign_key_checks = 1")
    mycon.commit()
    return


# account created
def popup_account_created():

    #  account created screen
    class account_created_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(account_created_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Account has been successfully created!", text_size=(600, None),
                               halign="center", font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2),
                               pos_hint={"x": 0.3, "top": .75})
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


# account creation failure
def popup_account_notcreated():

    # account creation failure screen
    class account_notcreated_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(account_notcreated_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Account could not be processed!", text_size=(600, None), halign="center",
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


# member account delete
def popup_member_delete():

    # member account delete screen
    class member_delete_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(member_delete_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Account has been deleted!", text_size=(600, None), halign="center",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            memberdeleteWindow.dismiss()
            sm.transition.direction = 'right'
            sm.current = 'Home'
        pass

    show = member_delete_screen()

    memberdeleteWindow = Popup(title="DELETED", content=show, size_hint=(None, None), size=(650, 600),
                               pos=(0, 0), auto_dismiss=False)

    memberdeleteWindow.open()


# member account delete failure
def popup_member_delete_failure():

    # member account delete failure screen
    class member_delete_failure_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(member_delete_failure_screen, self).__init__(**kwargs)

            self.label = Label(text="Your Account could not deleted!", text_size=(600, None), halign="center",
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Retry", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            memberdeletefailWindow.dismiss()

        pass

    show = member_delete_failure_screen()

    memberdeletefailWindow = Popup(title="ERROR", content=show, size_hint=(None, None), size=(650, 600),
                                   pos=(0, 0), auto_dismiss=False)

    memberdeletefailWindow.open()


# admin account delete cornfirmation
def popup_confirm_admindelete():

    # admin account delete confirmation screen
    class admin_delete_confirmation_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(admin_delete_confirmation_screen, self).__init__(**kwargs)

            self.label = Label(text="Are you sure you want to delete this Admin Account!", text_size=(600, None),
                               halign="center", font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2),
                               pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Cancel", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.1, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

            self.delete = Button(text="Delete", font_size=25, background_color=(0, 225, 225, 1),
                                 color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.5, "top": 0.3})
            self.delete.bind(on_release=self.call_delete)
            self.add_widget(self.delete)

        def call_back(self, instances):
            admindeleteconfirmationWindow.dismiss()

        def call_delete(self, instances):
            global admin_identifier
            adminaccountdelete(admin_identifier)
            admindeleteconfirmationWindow.dismiss()
            sm.transition.direction = "right"
            sm.current = "Home"
        pass

    show = admin_delete_confirmation_screen()

    admindeleteconfirmationWindow = Popup(title="Confirm", content=show, size_hint=(None, None), size=(650, 600),
                                          pos=(0, 0), auto_dismiss=False)

    admindeleteconfirmationWindow.open()


# creating room details
def create_room(roomno, roomcap, roomtype, roomprice):
    roomavailability = "Y"
    cursor.execute("insert into rooms(room_no,room_type,room_availability,room_capacity,room_price)"
                   "values('{}','{}','{}','{}','{}')".format(roomno, roomtype, roomavailability, roomcap, roomprice))
    mycon.commit()
    return


# room created
def popup_room_created():

    #  room created screen
    class room_created_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(room_created_screen, self).__init__(**kwargs)

            self.label = Label(text="Room Created!", halign="center", text_size=(600, None),
                               font_size=50, color=(1, 0, 0, 1), size_hint=(.4, .2), pos_hint={"x": 0.3, "top": .75})
            self.add_widget(self.label)

            self.back = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1),
                               size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
            self.back.bind(on_release=self.call_back)
            self.add_widget(self.back)

        def call_back(self, instances):
            roomWindow.dismiss()
            sm.transition.direction = 'right'
            sm.current = 'AdminConfirmation'

        pass

    show = room_created_screen()

    roomWindow = Popup(title="Success", content=show, size_hint=(None, None), size=(650, 600),
                       pos=(0, 0), auto_dismiss=False)

    roomWindow.open()


# room creation failure
def popup_room_notcreated():

    # room creation failure screen
    class room_notcreated_screen(FloatLayout):
        def __init__(self, **kwargs):
            super(room_notcreated_screen, self).__init__(**kwargs)

            self.label = Label(text="Room could not be created!", halign="center", text_size=(600, None),
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

    show = room_notcreated_screen()

    failureWindow = Popup(title="ERROR", content=show, size_hint=(None, None), size=(650, 600),
                          pos=(0, 0), auto_dismiss=False)

    failureWindow.open()


# inserting value into requested_rooms as guest
def request_room(name, phone, room_type, noofquests, check_in, check_out):
    cursor.execute("insert into requested_rooms(room_type,id,phonenumber,name,no_guests,check_in,check_out)"
                   "values('{}','{}','{}','{}',{},'{}','{}')"
                   .format(room_type, 'GUEST', phone, name, noofquests, check_in, check_out))
    mycon.commit()
    return


# inserting value into requested_rooms as member
def request_room_asmember(ID, room_type, noofquests, check_in, check_out):
    cursor.execute("select * from member_info where member_id = '{}';".format(ID))
    data = cursor.fetchall()
    phone = data[0][1]
    name = data[0][3]
    cursor.execute("insert into requested_rooms(room_type,id,phonenumber,name,no_guests,check_in,check_out)"
                   "values('{}','{}','{}','{}',{},'{}','{}')"
                   .format(room_type, ID, phone, name, noofquests, check_in, check_out))
    mycon.commit()
    return


# moving requested_room to booked_rooms
def move_to_booked_rooms(idx):
    name = idx
    cursor.execute("set foreign_key_checks = 0")
    cursor.execute("select * from requested_rooms where name='{}'".format(name))
    data = cursor.fetchone()
    if data[1] != "GUEST":
        cursor.execute("select * from member_info where member_name='{}'".format(name))
        more_data = cursor.fetchone()
        id_ = data[1]
        phone = data[2]
        email = more_data[2]
        name = name
        check_in = data[5]
        check_out = data[6]
        room_type = data[0]

        # checking if there is free room for the above room type
        cursor.execute("select room_no,room_availability from rooms where room_type='{}'".format(room_type))
        rooms_data = cursor.fetchall()
        for room_data in rooms_data:
            room_no = room_data[0]
            room_availability = room_data[1]
            if room_availability == 'Y':
                cursor.execute("insert into booked_rooms(room_no,id,phonenumber,email,name,check_in,check_out)"
                               "values('{}','{}','{}','{}','{}','{}','{}')"
                               .format(room_no, id_, phone, email, name, check_in, check_out))
                cursor.execute("alter table booked_rooms order by check_in")
                cursor.execute("delete from requested_rooms where name='{}'".format(name))
                cursor.execute("update rooms set room_availability='N' where room_no='{}'".format(room_no))
                mycon.commit()
                break
            else:
                continue
        else:
            print("NO ROOM")

    elif data[1] == "GUEST":
        id_ = data[1]
        phone = data[2]
        name = name
        check_in = data[5]
        check_out = data[6]
        room_type = data[0]
        email = "NULL"

        # checking if there is free room for the above room type
        cursor.execute("select room_no,room_availability from rooms where room_type='{}'".format(room_type))
        rooms_data = cursor.fetchall()
        for room_data in rooms_data:
            room_no = room_data[0]
            room_availability = room_data[1]
            if room_availability == 'Y':
                cursor.execute("insert into booked_rooms(room_no,id,phonenumber,email,name,check_in,check_out)"
                               "values('{}','{}','{}','{}','{}','{}','{}')"
                               .format(room_no, id_, phone, email, name, check_in, check_out))
                cursor.execute("alter table booked_rooms order by check_in")
                cursor.execute("delete from requested_rooms where name='{}'".format(name))
                cursor.execute("update rooms set room_availability='N' where room_no='{}'".format(room_no))
                mycon.commit()
                break
            else:
                continue
        else:
            print("NO ROOM")
    cursor.execute("set foreign_key_checks = 1")
    return


# deleting requests from requested_rooms
def delete_requestedroom(idx):
    name = idx
    cursor.execute("delete from requested_rooms where name='{}'".format(name))
    mycon.commit()
    return


# moving booked_rooms to checked_in
def checked_in_rooms(idx):
    name = idx
    cursor.execute("select * from booked_rooms where name = '{}'".format(name))
    data = cursor.fetchone()
    room_no = data[0]
    ID = data[1]
    checked_in = datetime.today().strftime('%Y-%m-%d')
    check_out = data[6]
    cursor.execute("insert into checked_in(room_no,id,name,checked_in,check_out)"
                   "values('{}','{}','{}','{}','{}')".format(room_no, ID, name, checked_in, check_out))
    cursor.execute("delete from booked_rooms where name = '{}'".format(name))
    mycon.commit()
    return


# checking out guests and opening the room
def check_out(idx):
    name = idx
    cursor.execute("select * from checked_in where name = '{}'".format(name))
    data = cursor.fetchone()
    room_no = data[0]
    cursor.execute("delete from checked_in where name = '{}'".format(name))
    cursor.execute("update rooms set room_availability = 'Y' where room_no = '{}'".format(room_no))
    mycon.commit()
    return


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

        self.layout = GridLayout(cols=5, spacing=40, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        rooms = available_rooms()
        x = [0.2, 0.35, 0.5, 0.65, 0.8]
        top = 0.8

        def lining():
            for i in range(0, 5):
                self.room = Label(text="", font_size=25, color=(225, 225, 225, 1),
                                  pos_hint={'x': x[i], 'top': top})
                self.layout.add_widget(self.room)
            return
        lining()
        for room in rooms:
            for i in range(0, len(room)):
                self.room = Label(text=str(room[i]), font_size=25, color=(225, 225, 225, 1),
                                  pos_hint={'x': x[i], 'top': top})
                self.layout.add_widget(self.room)
            top -= .05
        lining()
        self.root = ScrollView(size_hint=(None, None), size=(Window.width * .75, Window.height * .6),
                               pos_hint={"x": 0.125, 'top': 0.675})
        self.root.add_widget(self.layout)
        self.add_widget(self.root)

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
        x = [0.1, 0.175, 0.3, 0.45, 0.6, 0.75, 0.9, 0.8]
        top = 0.7
        self.checkref = {}
        for room in rooms:
            for i in range(0, len(room)):
                self.room = Label(text=str(room[i]), font_size=25, color=(225, 225, 225, 1),  size_hint=(.0, .0),
                                  pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.room)
            self.check = CheckBox(size_hint=(.02, .02), pos_hint={'x': x[7], 'top': top + 0.01}, active=False)
            self.add_widget(self.check)
            self.checkref[room[4]] = self.check
            top -= 0.05

        self.home = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.submit = Button(text="Checked In Now", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .1), pos_hint={"x": 0.3, "top": 0.125})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'AdminConfirmation'

    def call_confirm(self, instances):
        for idx, wgt in self.checkref.items():
            if wgt.active:
                checked_in_rooms(idx)
                self.parent.get_screen('BookedRooms').__init__()
                self.parent.get_screen('CheckedInRooms').__init__()

    pass


# CheckedIn rooms screen
class CheckedInRooms(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(CheckedInRooms, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text="Checked-In Rooms", font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={"x": 0.31, "top": 1})
        self.add_widget(self.label)

        x = [0.1, 0.25, 0.4, 0.55, 0.7, 0.9]
        top = 0.75
        header_string = ['Room No.', 'ID', 'Name', 'Checked-in', 'Check-out', 'Current Cost(¥)']
        for i in range(0, len(header_string)):
            self.header = Label(text=header_string[i], font_size=40, color=(225, 225, 225, 1), size_hint=(0, 0),
                                pos_hint={'x': x[i], 'top': top})
            self.add_widget(self.header)

        rooms = checked_rooms()
        x = [0.1, 0.25, 0.4, 0.55, 0.7, 0.8]
        top = 0.7
        self.checkref = {}
        for room in rooms:
            for i in range(0, len(room)):
                self.room = Label(text=str(room[i]), font_size=25, color=(225, 225, 225, 1),  size_hint=(.0, .0),
                                  pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.room)
            self.check = CheckBox(size_hint=(.02, .02), pos_hint={'x': x[5], 'top': top + 0.01}, active=False)
            self.add_widget(self.check)
            self.checkref[room[2]] = self.check
            cursor.execute("select room_price from rooms where room_no='{}'".format(room[0]))
            price = cursor.fetchone()
            days_stayed = (date.today() - room[3]).days
            curr_cost = days_stayed * price[0]
            self.cost = Label(text=str(curr_cost), font_size=25, color=(225, 225, 225, 1), size_hint=(.0, .0),
                              pos_hint={'x': 0.9, 'top': top})
            self.add_widget(self.cost)
            top -= 0.05

        self.home = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.refresh = Button(text="Refresh Page", font_size=35, background_color=(0, 225, 225, 1),
                              color=(225, 225, 225, 1), size_hint=(.2, .05), pos_hint={"x": 0.76, "top": .1})
        self.refresh.bind(on_release=self.call_refresh)
        self.add_widget(self.refresh)

        self.submit = Button(text="Checked Out Now", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .1), pos_hint={"x": 0.3, "top": 0.125})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'AdminConfirmation'

    def call_refresh(self, instances):
        self.parent.get_screen('CheckedInRooms').__init__()

    def call_confirm(self, instances):
        for idx, wgt in self.checkref.items():
            if wgt.active:
                check_out(idx)
                self.parent.get_screen('CheckedInRooms').__init__()
                self.parent.get_screen('Rooms').__init__()

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

        self.name_label = Label(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.name_label)
        self.nameofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                     pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.nameofguest)

        self.phone_label = Label(text="Phone Number", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.phone_label)
        self.phoneofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.phoneofguest)

        room_type = room_types()
        self.room_label = Label(text="Room Type", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.room_label)
        self.dropdown = DropDown()
        for room_type_ in room_type:
            type = room_type_[0]
            self.val = Button(text=type, color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                              size_hint_y=None, height=44)
            self.val.bind(on_release=lambda val: self.dropdown.select(val.text))
            self.dropdown.add_widget(self.val)
        self.roomofguest = Button(text='Select', color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                                  size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.6})
        self.roomofguest.bind(on_release=self.dropdown.open)
        self.add_widget(self.roomofguest)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.roomofguest, 'text', x))

        self.noofguests_label = Label(text="Number of Guests", font_size=40, color=(225, 225, 1, 1),
                                      size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.noofguests_label)
        self.dropdown2 = DropDown()
        for num in range(1, 11):
            self.val = Button(text=str(num), color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                              size_hint_y=None, height=44)
            self.val.bind(on_release=lambda val: self.dropdown2.select(val.text))
            self.dropdown2.add_widget(self.val)
        self.noofguest = Button(text='Select', color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                                size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.5})
        self.noofguest.bind(on_release=self.dropdown2.open)
        self.add_widget(self.noofguest)
        self.dropdown2.bind(on_select=lambda instance, x: setattr(self.noofguest, 'text', x))

        self.checkin_label = Label(text="Check-in Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.checkin_label)
        self.checkinofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                        pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.checkinofguest)

        self.checkout_label = Label(text="Check-out Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
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
        self.roomofguest.text = "Select"
        self.noofguest.text = "Select"
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
        phoneCheck = ''
        for i in range(0, len(phone)):
            if phone[i] == "-":
                phoneCheck = phoneCheck
            else:
                phoneCheck += phone[i]
                continue
        today = date.today()
        if name != "" and phoneCheck.isnumeric() and room_type != "Select" and noofquests != "Select" and\
                check_in > str(today) and check_out > str(today) and check_out > check_in:
            request_room(name, phone, room_type, noofquests, check_in, check_out)
            self.parent.get_screen('AdminConfirmation').__init__()
            popup_valid_submission()
        else:
            popup_invalid_submission()
        self.nameofguest.text = ""
        self.phoneofguest.text = ""
        self.roomofguest.text = "Select"
        self.noofguest.text = "Select"
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

        self.id_label = Label(text="Member ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.65})
        self.add_widget(self.id_label)
        self.idofguest = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                   pos_hint={"x": 0.5, "top": 0.65})
        self.add_widget(self.idofguest)

        self.password_label = Label(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
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
        global member_identifier
        member_identifier = ID
        password = self.passwordofguest.text
        memberinfo = member_info()
        state = ''
        for member in memberinfo:
            if ID in member and password in member:
                self.parent.get_screen("MemberReservation").__init__()
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


member_identifier = ""
mID = ''


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

        global member_identifier
        self.id_label = Label(text="Member ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.id_label)
        self.idofmember = Label(text=member_identifier, color=(225, 225, 225, 1), font_size=40, size_hint=(.35, .05),
                                pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.idofmember)

        room_type = room_types()
        self.room_label = Label(text="Room Type", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.room_label)
        self.dropdown = DropDown()
        for room_type_ in room_type:
            type = room_type_[0]
            self.val = Button(text=type, color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                              size_hint_y=None, height=44)
            self.val.bind(on_release=lambda val: self.dropdown.select(val.text))
            self.dropdown.add_widget(self.val)
        self.room = Button(text='Select', color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                           size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.7})
        self.room.bind(on_release=self.dropdown.open)
        self.add_widget(self.room)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.room, 'text', x))

        self.noofguests_label = Label(text="Number of Guests", font_size=40, color=(225, 225, 1, 1),
                                      size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.noofguests_label)
        self.dropdown2 = DropDown()
        for num in range(1, 11):
            self.val = Button(text=str(num), color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                              size_hint_y=None, height=44)
            self.val.bind(on_release=lambda val: self.dropdown2.select(val.text))
            self.dropdown2.add_widget(self.val)
        self.noofguests = Button(text='Select', color=(225, 225, 1, 1), background_color=(0, 225, 225, 1),
                                 size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.6})
        self.noofguests.bind(on_release=self.dropdown2.open)
        self.add_widget(self.noofguests)
        self.dropdown2.bind(on_select=lambda instance, x: setattr(self.noofguests, 'text', x))

        self.checkin_label = Label(text="Check-in Date", font_size=40, color=(225, 225, 1, 1),
                                   size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.checkin_label)
        self.checkin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                 pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.checkin)

        self.checkout_label = Label(text="Check-out Date", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
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

        self.delete = Button(text="Delete Acoount", font_size=25, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.83, "top": 0.99})
        self.delete.bind(on_release=self.call_delete)
        self.add_widget(self.delete)

    def call_memberlogin(self, instances):
        self.idofmember.text = ""
        self.room.text = "Select"
        self.noofguests.text = "Select"
        self.checkin.text = ""
        self.checkout.text = ""
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_delete(self, instances):
        self.parent.get_screen('MemberDelete').__init__()
        sm.transition.direction = 'left'
        sm.current = 'MemberDelete'

    def submit(self, instances):
        ID = member_identifier
        room_type = self.room.text
        noofquests = self.noofguests.text
        check_in = self.checkin.text
        check_out = self.checkout.text
        today = date.today()
        if ID != "" and room_type != "Select" and noofquests != "Select" and check_in > str(today) and\
                check_out > str(today) and check_out > check_in:
            request_room_asmember(ID, room_type, noofquests, check_in, check_out)
            self.parent.get_screen('AdminConfirmation').__init__()
            popup_valid_submission()
        else:
            popup_invalid_submission()
        self.idofmember.text = ""
        self.room.text = "Select"
        self.noofguests.text = "Select"
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

        self.name_label = Label(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.name_label)
        self.nameofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.nameofmember)

        self.phone_label = Label(text="Phone Number", font_size=40, color=(225, 225, 1, 1),
                                 size_hint=(.35, .05), pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.phone_label)
        self.phoneofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.phoneofmember)

        self.email_label = Label(text="Email", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.email_label)
        self.emailofmember = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.emailofmember)

        self.pass_label = Label(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.pass_label)
        self.passofmember = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                      pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.passofmember)

        self.pass2_label = Label(text="Confirm Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.pass2_label)
        self.pass2ofmember = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                       pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.pass2ofmember)

        global mID
        mID = makememberid()
        self.id_label = Label(text="Your ID will be", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.3})
        self.add_widget(self.id_label)
        self.id_value = Label(text=mID, font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.5, "top": 0.3})
        self.add_widget(self.id_value)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": .99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.submit = Button(text="Done", font_size=40, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                             size_hint=(.4, .15), pos_hint={"x": 0.3, "top": .2})
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
        phone = self.phoneofmember.text
        email = self.emailofmember.text
        password = self.passofmember.text
        password_check = self.pass2ofmember.text
        global mID
        phoneCheck = ''
        for i in range(0, len(phone)):
            if phone[i] == "-":
                phoneCheck = phoneCheck
            else:
                phoneCheck += phone[i]
                continue
        mail_list = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@aol.com', '@msn.com', '@icloud.com']
        if '@' in email:
            mail = email[email.index('@'):len(email)+1]
        else:
            mail = email
        if name != '' and phoneCheck.isnumeric() and mail in mail_list and password != '' and\
                password == password_check:
            create_member(mID, phone, email, name, password)
            self.parent.get_screen('Createmember').__init__()
            popup_account_created()
        else:
            popup_account_notcreated()
        self.nameofmember.text = ""
        self.phoneofmember.text = ""
        self.emailofmember.text = ""
        self.passofmember.text = ""
        self.pass2ofmember.text = ""
    pass


# Delete my member account screen
class MemberDelete(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(MemberDelete, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text='Delete my Member account', font_size=75, color=(225, 225, 225, 1), size_hint=(.4, .3),
                           pos_hint={'x': 0.31, 'top': 1})
        self.add_widget(self.label)

        global member_identifier
        self.id_label = Label(text="Member ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.65})
        self.add_widget(self.id_label)
        self.idofmember = TextInput(text=member_identifier, multiline=False, font_size=40, size_hint=(.35, .05),
                                    pos_hint={"x": 0.5, "top": 0.65})
        self.add_widget(self.idofmember)

        self.password_label = Label(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                    pos_hint={"x": 0.15, "top": 0.55})
        self.add_widget(self.password_label)
        self.password = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                  pos_hint={"x": 0.5, "top": 0.55})
        self.add_widget(self.password)

        self.memberconfirm = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1),
                                    color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.memberconfirm.bind(on_release=self.call_memberconfirmation)
        self.add_widget(self.memberconfirm)

        self.delete = Button(text="Confirm Delete", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .15), pos_hint={"x": 0.3, "top": 0.3})
        self.delete.bind(on_release=self.call_deleter)
        self.add_widget(self.delete)

    def call_memberconfirmation(self, instances):
        self.idofmember.text = ""
        self.password.text = ""
        sm.transition.direction = 'right'
        sm.current = 'MemberReservation'

    def call_deleter(self, instances):
        ID = self.idofmember.text
        password = self.password.text
        memberinfo = member_info()
        state = ''
        for member in memberinfo:
            if ID in member and password in member:
                member_delete(ID)
                self.parent.get_screen("AdminConfirmation").__init__()
                self.parent.get_screen("BookedRooms").__init__()
                popup_member_delete()
                state = 'correct'
                self.idofmember.text = ""
                break
            else:
                state = 'incorrect'
        if state == 'incorrect':
            popup_member_delete_failure()
        self.password.text = ""
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

        self.id_label = Label(text="Admin ID", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.65})
        self.add_widget(self.id_label)
        self.idofadmin = TextInput(multiline=False, font_size=40, size_hint=(.35, .05),
                                   pos_hint={"x": 0.5, "top": 0.65})
        self.add_widget(self.idofadmin)

        self.password_label = Label(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
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
        global admin_identifier
        admin_identifier = ID
        password = self.passwordofadmin.text
        admininfo = admin_info()
        state = ''
        for admin in admininfo:
            if ID in admin and password in admin:
                self.parent.get_screen("AdminConfirmation").__init__()
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


admin_identifier = ""
id_ = ''


# Admin room confirmation screen
class AdminConfirmation(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(AdminConfirmation, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        global admin_identifier
        self.label = Label(text=admin_identifier, font_size=75, color=(225, 225, 225, 1),
                           size_hint=(.4, .1), pos_hint={'x': 0.31, 'top': 0.95})
        self.add_widget(self.label)
        self.label = Label(text='Admin Confirmation', font_size=75, color=(225, 225, 225, 1),
                           size_hint=(.4, .1), pos_hint={'x': 0.31, 'top': 0.875})
        self.add_widget(self.label)

        x = [0.15, 0.25, 0.335, 0.45, 0.55, 0.65, 0.75, 0.85]
        top = 0.75
        header_string = ['Room Type', 'ID', 'Phone No.', 'Name', 'No. of guests', 'Check-in', 'Check-out', 'Approve']
        for i in range(0, len(header_string)):
            self.header = Label(text=header_string[i], font_size=30, color=(225, 225, 225, 1), size_hint=(0, 0),
                                pos_hint={'x': x[i], 'top': top})
            self.add_widget(self.header)

        requested = requested_rooms()
        self.checkref = {}
        x = [0.15, 0.25, 0.335, 0.465, 0.55, 0.65, 0.75, 0.85]
        top = 0.7
        for request in requested:
            for i in range(0, len(request)):
                self.value = Label(text=str(request[i]), font_size=25, color=(225, 225, 225, 1), size_hint=(.0, .0),
                                   pos_hint={'x': x[i], 'top': top})
                self.add_widget(self.value)
            self.check = CheckBox(size_hint=(.02, .02), pos_hint={'x': x[7], 'top': top + 0.01}, active=False)
            self.add_widget(self.check)
            self.checkref[request[3]] = self.check
            top -= 0.05

        self.submit = Button(text="Confirm reservation", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .1), pos_hint={"x": 0.3, "top": 0.125})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

        self.delete = Button(text="Delete reservation", font_size=30, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.2, .05), pos_hint={"x": 0.05, "top": 0.1})
        self.delete.bind(on_release=self.call_delete)
        self.add_widget(self.delete)

        self.home = Button(text="Home", font_size=25, background_color=(0, 225, 225, 1),
                           color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

        self.view = Button(text="Booked rooms", font_size=25, background_color=(0, 225, 225, 1),
                           color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.83, "top": 0.99})
        self.view.bind(on_release=self.call_booked)
        self.add_widget(self.view)

        self.view2 = Button(text="Checked-In rooms", font_size=25, background_color=(0, 225, 225, 1),
                            color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.83, "top": 0.96})
        self.view2.bind(on_release=self.call_booked2)
        self.add_widget(self.view2)

        self.new_admin = Button(text="New Admin", font_size=25, background_color=(0, 225, 225, 1),
                                color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.63, "top": 0.99})
        self.new_admin.bind(on_release=self.call_newadmin)
        self.add_widget(self.new_admin)

        self.new_room = Button(text="Create room", font_size=25, background_color=(0, 225, 225, 1),
                               color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.43, "top": 0.99})
        self.new_room.bind(on_release=self.call_newroom)
        self.add_widget(self.new_room)

        self.admindelete = Button(text="Delete My Account", font_size=25, background_color=(0, 225, 225, 1),
                                  color=(225, 225, 225, 1), size_hint=(.15, .025), pos_hint={"x": 0.23, "top": 0.99})
        self.admindelete.bind(on_release=self.call_admindelete)
        self.add_widget(self.admindelete)

    def call_home(self, instances):
        sm.transition.direction = 'right'
        sm.current = 'Home'

    def call_booked(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'BookedRooms'

    def call_booked2(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'CheckedInRooms'

    def call_newadmin(self, instanes):
        sm.transition.direction = 'left'
        sm.current = 'NewAdmin'

    def call_newroom(self, instances):
        sm.transition.direction = 'left'
        sm.current = 'NewRoom'

    def call_confirm(self, instances):
        for idx, wgt in self.checkref.items():
            if wgt.active:
                move_to_booked_rooms(idx)
                self.parent.get_screen('AdminConfirmation').__init__()
                self.parent.get_screen('BookedRooms').__init__()
                self.parent.get_screen('Rooms').__init__()
        popup_confirm()

    def call_delete(self, instances):
        for idx, wgt in self.checkref.items():
            if wgt.active:
                delete_requestedroom(idx)
                self.parent.get_screen('AdminConfirmation').__init__()
                self.parent.get_screen('BookedRooms').__init__()
        popup_confirm_delete()

    def call_admindelete(self, instances):
        popup_confirm_admindelete()
    pass


# New admin account screen
class NewAdmin(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(NewAdmin, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text='Create New Admin', font_size=75, color=(225, 225, 225, 1),
                           size_hint=(.4, .3), pos_hint={'x': 0.31, 'top': 1})
        self.add_widget(self.label)

        self.phone_label = Label(text="Phone number", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.8})
        self.add_widget(self.phone_label)
        self.phone = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.8})
        self.add_widget(self.phone)

        self.email_label = Label(text="Email", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.email_label)
        self.email = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.email)

        self.name_label = Label(text="Name", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.name_label)
        self.name_ = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.name_)

        self.password_label = Label(text="Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                    pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.password_label)
        self.password = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                                  pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.password)

        self.pass2_label = Label(text="Confirm Password", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                 pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.pass2_label)
        self.pass2 = TextInput(multiline=False, password=True, font_size=40, size_hint=(.35, .05),
                               pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.pass2)

        global id_
        id_ = makeid()
        self.id_label = Label(text="Your ID will be", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.15, "top": 0.3})
        self.add_widget(self.id_label)
        self.id_value = Label(text=id_, font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                              pos_hint={"x": 0.5, "top": 0.3})
        self.add_widget(self.id_value)

        self.submit = Button(text="Create", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .1), pos_hint={"x": 0.3, "top": 0.2})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

        self.home = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self, instances):
        self.phone.text = ""
        self.email.text = ""
        self.name_.text = ""
        self.password.text = ""
        self.pass2.text = ""
        sm.transition.direction = 'right'
        sm.current = 'AdminConfirmation'

    def call_confirm(self, instances):
        phone = self.phone.text
        email = self.email.text
        name = self.name_.text
        password = self.password.text
        pass2 = self.pass2.text
        global id_
        phoneCheck = ''
        for i in range(0, len(phone)):
            if phone[i] == '-':
                phoneCheck = phoneCheck
            else:
                phoneCheck += phone[i]
                continue
        mail_list = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@aol.com', '@msn.com', '@icloud.com']
        if '@' in email:
            mail = email[email.index('@'):len(email) + 1]
        else:
            mail = email
        if name != '' and phoneCheck.isnumeric() and mail in mail_list and password != '' and password == pass2:
            create_admin(id_, phone, email, name, password)
            self.parent.get_screen('NewAdmin').__init__()
            popup_account_created()
        else:
            popup_account_notcreated()
        self.phone.text = ""
        self.email.text = ""
        self.name_.text = ""
        self.password.text = ""
        self.pass2.text = ""
    pass


# New room create screen
class NewRoom(Screen, FloatLayout):
    def __init__(self, **kwargs):
        super(NewRoom, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 0, 1)
            self.rect = Rectangle(size=(3000, 2000))

        self.label = Label(text='Create New Room', font_size=75, color=(225, 225, 225, 1),
                           size_hint=(.4, .3), pos_hint={'x': 0.31, 'top': 1})
        self.add_widget(self.label)

        self.roomno_label = Label(text="Room Number", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                  pos_hint={"x": 0.15, "top": 0.7})
        self.add_widget(self.roomno_label)
        self.roomno = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.7})
        self.add_widget(self.roomno)

        self.roomtype_label = Label(text="Room Type", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                    pos_hint={"x": 0.15, "top": 0.6})
        self.add_widget(self.roomtype_label)
        self.roomtype = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.6})
        self.add_widget(self.roomtype)

        self.roomcap_label = Label(text="Room Capacity", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                   pos_hint={"x": 0.15, "top": 0.5})
        self.add_widget(self.roomcap_label)
        self.roomcap = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.5})
        self.add_widget(self.roomcap)

        self.roomprice_label = Label(text="Room Price", font_size=40, color=(225, 225, 1, 1), size_hint=(.35, .05),
                                     pos_hint={"x": 0.15, "top": 0.4})
        self.add_widget(self.roomprice_label)
        self.roomprice = TextInput(multiline=False, font_size=40, size_hint=(.35, .05), pos_hint={"x": 0.5, "top": 0.4})
        self.add_widget(self.roomprice)

        self.submit = Button(text="Create", font_size=40, background_color=(0, 225, 225, 1),
                             color=(225, 225, 225, 1), size_hint=(.4, .1), pos_hint={"x": 0.3, "top": 0.2})
        self.submit.bind(on_release=self.call_confirm)
        self.add_widget(self.submit)

        self.home = Button(text="Back", font_size=25, background_color=(0, 225, 225, 1), color=(225, 225, 225, 1),
                           size_hint=(.15, .025), pos_hint={"x": 0.01, "top": 0.99})
        self.home.bind(on_release=self.call_home)
        self.add_widget(self.home)

    def call_home(self, instances):
        self.roomno.text = ""
        self.roomcap.text = ""
        self.roomtype.text = ""
        self.roomprice.text = ""
        sm.transition.direction = 'right'
        sm.current = 'AdminConfirmation'

    def call_confirm(self, instances):
        roomno = self.roomno.text
        roomcap = self.roomcap.text
        roomtype = self.roomtype.text
        roomprice = self.roomprice.text
        if roomno != '' and roomcap != '' and roomtype != '' and roomprice:
            create_room(roomno, roomcap, roomtype, roomprice)
            popup_room_created()
            self.parent.get_screen('Rooms').__init__()
            self.parent.get_screen('GuestReservation').__init__()
            self.parent.get_screen('MemberReservation').__init__()
        else:
            popup_room_notcreated()
        self.roomno.text = ""
        self.roomcap.text = ""
        self.roomtype.text = ""
        self.roomprice.text = ""
    pass


# Screen manager
sm = ScreenManager()
sm.add_widget(Home(name='Home'))
sm.add_widget(Create(name='Create'))
sm.add_widget(Rooms(name='Rooms'))
sm.add_widget(BookedRooms(name='BookedRooms'))
sm.add_widget(CheckedInRooms(name="CheckedInRooms"))
sm.add_widget(GuestReservation(name='GuestReservation'))
sm.add_widget(MemberLogin(name='MemberLogin'))
sm.add_widget(MemberReservation(name='MemberReservation'))
sm.add_widget(Createmember(name='Createmember'))
sm.add_widget(MemberDelete(name='MemberDelete'))
sm.add_widget(AdminLogin(name='AdminLogin'))
sm.add_widget(AdminConfirmation(name='AdminConfirmation'))
sm.add_widget(NewAdmin(name='NewAdmin'))
sm.add_widget(NewRoom(name='NewRoom'))


class HotelReservationApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    HotelReservationApp().run()
