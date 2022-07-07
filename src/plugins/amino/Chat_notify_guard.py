from datetime import datetime
from collections import namedtuple
from threading import Thread
from time import sleep
from os import path, getcwd
import json


Chat = namedtuple("Chat", ["title", "chatId"])
Message = namedtuple("Message", ["uid", "nickname", "messageId", "content", "contentType", "createdTime"])


class Chat_notify_guard:
    def __init__(self, sub_client) -> None:
        self.sub_client = sub_client
        self.public_chats: list(tuple) | None = None
        self.chats_for_checking: list[str] | None = None
        print(getcwd())
        self.banned: list[str] = Utils.read_json()
        self.isStarted: bool = False

    def update_current_public_chats(self) -> str:
        self.public_chats == None
        return self.get_chats()

    def get_chats(self) -> str:
        if self.public_chats != None:
            return Utils.string_decoration(self.public_chats)
        else:
            try:
                public_chats: list[dict] = self.sub_client.get_public_chat_threads(size= 100).json
            except:
                public_chats = None
            if public_chats != None:
                self.public_chats = self.unpack_chats(public_chats)
                return Utils.string_decoration(self.public_chats)
            else:
                return "Get public chats failed"


    def unpack_chats(self, public_chats_: list[dict]) -> list[tuple]:
        public_chats: list[tuple] = list()
        for public_chat in public_chats_:
            chat = Chat(title= public_chat.get("title"), chatId= public_chat.get("threadId"))
            public_chats.append(chat)
        return public_chats

    def select_chats_for_protect(self, chats: list[str]) -> str:
        answer: str = "Success"
        if self.isStarted == True:
            answer += self.stop()
        self.chats_for_checking = list()
        for chat in chats:
            self.chats_for_checking.append(self.public_chats[int(chat)].chatId)
        return answer

    def clear_chat_selector(self) -> str:
        answer: str = "Success"
        if self.isStarted == True:
            answer += self.stop()
        self.chats_for_checking = None 
        return answer

    def get_chat_messages(self, chatId: str) -> list[tuple] | None:
        try:
            chat_messages: list[dict] = self.sub_client.get_chat_messages(chatId= chatId, size= 100).json
        except:
            return
        if chat_messages != None:
            return self.unpack_message(chat_messages)

    def unpack_message(self, chat_messages_: list[dict]) -> list[tuple]:
        chat_messages: list[tuple] = list()
        for chat_message in chat_messages_:
            author: dict = chat_message.get("author")
            message: tuple = Message(
                    uid= author.get("uid"),
                    nickname= author.get("nickname"),
                    messageId= chat_message.get("messageId"),
                    content= chat_message.get("content"),
                    contentType= chat_message.get("type"),
                    createdTime= chat_message.get("createdTime")
                    )
            chat_messages.append(message)
        return chat_messages
    
    def this_user_isBanned(self, userId: str) -> bool:
        for userId_ in self.banned:
            if userId == userId_:
                return True
        else:
            self.banned.append(userId)
            Utils.write_json(self.banned)
            return False

    def check_user_sequence(self, chat_messages: list[tuple], startIndex: int) -> bool:
        stopIndex: int = startIndex + 5 if len(chat_messages) - startIndex > 0 else len(chat_messages)
        for index in range(startIndex, stopIndex):
            if (chat_messages[index].uid != chat_messages[index+1]) & (Utils.get_seconds_between_two_datetimes(chat_messages[index].createdTime, chat_messages[index+1].createdTime) <= 2):
                return False
        else:
            return True
   
    def check_chat_message(self, chatId: str) -> None:
        chat_messages: list[tuple] = self.get_chat_messages(chatId)
        if chat_messages != None:
            for message in chat_messages:
                    if message.contentType >= 100:
                        if message.content != None:
                            if self.this_user_isBanned(message.uid) == False:
                                try:
                                    self.sub_client.ban(userId= message.uid, reason= "ban by spam filter")
                                    print(f"{message.nickname} - ban")
                                except:
                                    pass
                        elif message.content == None:
                            pass
                            #six_times_together: bool = self.check_user_sequence(chat_messages, chat_messages.index(message))
                            #if six_times_together == True:
                                #try:
                                    #print(f"{message.nickname} - ban")#self.sub_client.ban(userId= message.uid, reason= "ban by spam filter")
                                #except:
                                    #pass

    def check_chat(self) -> None:
        while self.isStarted == True:
            for chatId in self.chats_for_checking:
                sleep(5)
                self.check_chat_message(chatId)
    
    def start(self) -> None:
        if self.isStarted == False:
            self.isStarted = True
            self.chatGuard_thread = Thread(target= self.check_chat, args=())

            self.chatGuard_thread.start()
            answer: str = "Amino chat guard module is started"
            print(answer)
            return answer
        else:
            answer: str = 'Amino chat guard module is already started'
            print(answer)
            return answer

    def stop(self) -> str:
        if self.isStarted == True:
            self.isStarted = False
            del self.chatGuard_thread
            answer: str = 'Amino chat guard module is stoped'
            print(answer)
            return answer
        else:
            answer: str = 'Amino chat guard module is already stoped'
            print(answer)
            return answer

    def restart(self) -> str:
        if self.isStarted == False:
            answer: str = "Amino chat guard wasn't started for restarting. Cannot restart"
            print(answer)
            return answer
        else:
            self.stop()
            self.start()
            answer: str ='Amino chat guard module was restarted'
            print(answer)
            return answer


class Utils:
    def string_decoration(public_chats: list[tuple]) -> str:
        decorated_string: str = str(f"PUBLIC CHATS:\n\n\n")
        for chat in public_chats:
            decorated_string += str(f"[{public_chats.index(chat)}]:= {chat.title}\n\n")
        return decorated_string

    def convert_createdTime_into_datetime_module_format(createdTime: str) -> str:
        DATE_TIME_:list[str] = createdTime.split("T")
        TIME_:list[str] = DATE_TIME_[1].split("Z")
        return str(f"{DATE_TIME_[0]} {TIME_[0]}")

    def get_seconds_between_two_datetimes(first_datetime: str, second_datetime: str) -> int:
        first_datetime = Utils.convert_createdTime_into_datetime_module_format(first_datetime)
        second_datetime = Utils.convert_createdTime_into_datetime_module_format(second_datetime)
        dateTime_delta = datetime.strptime(str(second_datetime), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(first_datetime), '%Y-%m-%d %H:%M:%S')
        return int(dateTime_delta.total_seconds())

    def read_json() -> list[str]:
        if path.isfile("src/lib/lib_plugins/amino/chat_notify_guard/banned.json") != True:
            Utils.write_json(list())
        with open("src/lib/lib_plugins/amino/chat_notify_guard/banned.json") as jsonFile:
            jsonFileIncludes: dict = json.load(jsonFile)
            return jsonFileIncludes.get("banned")

    def write_json(bannedList: list[str]) -> None:
        with open("src/lib/lib_plugins/amino/chat_notify_guard/banned.json", "w") as jsonFile:
            json.dump({"banned":bannedList}, jsonFile)
