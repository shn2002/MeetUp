# MVC pattern:
# View class is for user interface
# Controller class is for handling the request from view and call the Model
# Model class is for getting the data from database

from user import *
from VOUser import *
from message import *
from connectionPool import *
import mpu


class View():

    @staticmethod
    def start_page():
        login_option = input("If you would like to sign in, please enter 1, otherwise you would like to sign up. "
                             "please enter 2: ")
        return int(login_option)

    @staticmethod
    def login():
        print("Hi meetup user, welcome back!")
        user_name = input("Please enter your username:  ")
        password = input("Please enter your password:  ")
        return user_name, password

    @staticmethod
    def enter_user_info():
        name = input("Name: ")
        password = input("Password: ")
        occupation = input("Occupation: ")
        address = input("Address: ")
        age = int(input("Age: "))
        return name, password, occupation, address, age

    @staticmethod
    def main_options_page():
        print("Main options menu: ")
        print("1. Search near by users")
        print("2. Send message")
        print("3. Search message")
        print("4. Exit")
        option = int(input("Please enter an option: "))
        return option

    @staticmethod
    def search_nearby_users():
        radius = int(input("Please enter a radius, in km, to search other users with in that range: "))
        occupation = input("Please enter an occupation to search users that work for that occupation: ")
        return radius, occupation

    @staticmethod
    def send_message():
        recipient_id = int(input("Please enter the ID number of the recipient: "))
        content = input("Please enter the message content: ")
        return recipient_id, content


class Controller():
    current_user = None

    def __init__(self, view, model):
        self.__view = view
        self.__model = model

    def run(self):

        pool = ConnectionPool()
        self.connection = pool.get_connection()
        # When a user choose to sign up , after the account is successfully created.the user will be redirect to the start page
        # When a user put the wrong password or wrong user name, user can't successfully login
        while True:
            start_option = self.__view.start_page()
            if start_option == 1:
                current_user = self.__log_in()
                if current_user:
                    break
            elif start_option == 2:
                self.__create_new_account()

        # This is the main functionality
        # user can choose any option
        while True:
            main_options = self.__view.main_options_page()

            if main_options == 1:
                radius, occupation = self.__view.search_nearby_users()
                self.__search_users(current_user, radius, occupation)

            elif main_options == 2:
                recipient_id, content = self.__view.send_message()
                self.__send_message(current_user.id, recipient_id, content)
                print("The message has been sent and saved in the database")
            elif main_options == 3:
                message_list = self.__search_message(current_user.id)
                print('-------------------below is the message list--------------------\n')
                for message in message_list:
                    print('message id: ' + str(message.id) + ' sender id: ' + str(
                        message.sender_id) + ' recipient id: ' + str(message.recipient_id) + ' sent time: ' + str(
                        message.sent_Time) + ' content: ' + str(message.content) + '\n')
                print('-------------------end--------------------\n')
            else:
                print("Thanks for using Meetup!")
                exit()

    def __log_in(self):
        user_name, password = self.__view.login()
        if user_name == "":
            print("username should not be empty")
            return None
        if password == "":
            print("password should not be empty")
            return None
        user = self.__model.get_user_by_name(user_name, self.connection)
        if user:
            if user.password == password:
                print("username and password matches, you are successfully login in")
                name = user.name
                print('Hi', name + ',', 'You are now logged in!')
                return user
            else:
                print("password doesn't match")
                return None
        else:
            print("user doesn't exist")
            return None

    def __create_new_account(self):
        name, password, occupation, address, age = self.__view.enter_user_info()
        new_user = User(name, password, occupation, address, age)
        self.__model.add_new_user(new_user, self.connection)
        print('User has been created, please enter 1 to log in.')

    def __search_users(self, current_user, radius, occupation):

        other_users = self.__model.get_all_users(self.connection)
        org_user_coordinates = (current_user.lat, current_user.lng)
        matched_users = []

        for user in other_users:
            dst_user_coordinates = (user.lat, user.lng)
            distance = mpu.haversine_distance(org_user_coordinates, dst_user_coordinates)

            if distance < radius and current_user.occupation == user.occupation and current_user.id != user.id:
                matched_users.append(user)
        print('-------------------below is the message list--------------------\n')
        for user in matched_users:
            print('Matched user: user name is ' + user.name + ' and user occupation is ' + user.occupation + '\n')
        print('-------------------end--------------------\n')

    def __send_message(self, sender_id, recipient_id, content):
        new_message = Message(sender_id, recipient_id, content)
        new_message_wrapper = Message(sender_id, recipient_id, BoldWrapper(UnderlineWarpper(new_message)).render())
        self.__model.add_message_by_sender_id(new_message_wrapper, self.connection)

    def __search_message(self, current_user_id):
        message_list = self.__model.get_messages_by_sender_id(current_user_id, self.connection)
        return message_list


class Model():
    # add new user
    def add_new_user(self, new_user, connection):
        sql = "INSERT INTO Users ( name, password, occupation, address, age, lat, lng) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values = new_user.get_user()
        connection.cursor.execute(sql, values)
        connection.cnxn.commit()
        print("The user has been successfully created. ")

    # get user by name
    def get_user_by_name(self, user_name, connection):
        sql = "SELECT * FROM Users WHERE name = %(name)s"
        connection.cursor.execute(sql, {'name': user_name})
        records = connection.cursor.fetchall()
        new_user = VOUser()
        for row in records:
            new_user.id = row[0]
            new_user.name = row[1]
            new_user.password = row[2]
            new_user.occupation = row[3]
            new_user.address = row[4]
            new_user.age = row[5]
            new_user.lat = row[6]
            new_user.lng = row[7]
        if new_user.id is not None:
            return new_user
        else:
            return None

    # get all users
    def get_all_users(self, connection):
        sql = "SELECT * FROM Users"
        connection.cursor.execute(sql)
        records = connection.cursor.fetchall()
        users = []
        for row in records:
            new_user = VOUser()
            new_user.id = row[0]
            new_user.name = row[1]
            new_user.password = row[2]
            new_user.occupation = row[3]
            new_user.address = row[4]
            new_user.age = row[5]
            new_user.lat = row[6]
            new_user.lng = row[7]
            users.append(new_user)
        if len(users) > 0:
            return users
        else:
            return None

    def get_messages_by_sender_id(self, user_id, connection):
        sql = "SELECT * FROM Messages WHERE senderID = %(sender_id)s"
        connection.cursor.execute(sql, {'sender_id': user_id})
        records = connection.cursor.fetchall()
        new_messages = []
        for row in records:
            new_message = Message()
            new_message.id = row[0]
            new_message.sender_id = row[1]
            new_message.recipient_id = row[2]
            new_message.content = row[4]
            new_message.sent_Time = row[3]
            new_messages.append(new_message)

        if len(new_messages) > 0:
            return new_messages
        else:
            return None

    def get_messages_by_recipient_id(self, user_id, connection):
        sql = "SELECT * FROM Messages WHERE recipientID = = %(recipient_id)s"
        connection.cursor.execute(sql, {'recipient_id': user_id})
        records = connection.cursor.fetchall()
        new_messages = []
        for row in records:
            new_message = Message()
            new_message.id = row[0]
            new_message.sender_id = row[1]
            new_message.recipient_id = row[2]
            new_message.content = row[4]
            new_message.sent_Time = row[3]
            new_messages.append(new_message)

        if len(new_messages) > 0:
            return new_messages
        else:
            return None

    def add_message_by_sender_id(self, new_message, connection):
        sql = "INSERT INTO Messages ( senderID, recipientID, content) VALUES(%s,%s,%s)"
        value = new_message.get_message()
        connection.cursor.execute(sql, value)
        connection.cnxn.commit()
        print("The message has been successfully saved. ")
