from .plugins.amino import Ban, Category, Chat_notify_guard, Community_join_requests, Login
from .plugins.google import Sheets
from .lib.lib_core import messages

class Core:
    def __init__(self) -> None:
        self.terminal_session: bool = False
        self.auth()
        self.modules_init()

    def auth(self) -> None:
        amino = Login.Amino_login()
        self.sub_client = amino.sub_client
        self.botId: str = amino.botId

    def modules_init(self) -> None:
        self.amino_modules_init()
        self.google_modules_init()

    def amino_modules_init(self) -> None:
        self.Amino_ban = Ban.Amino_ban(self.sub_client)
        self.Amino_category = Category.Amino_category(sub_client=self.sub_client, botId=self.botId)
        self.Amino_chat_notify_guard = Chat_notify_guard.Chat_notify_guard(sub_client= self.sub_client)
        self.Amino_community_join_requests = Community_join_requests.Amino_community_join_requests(self.sub_client)

    def google_modules_init(self) -> None:
        self.Sheets = Sheets.Sheets()

    def transponder(self, answer: str) -> None | str:
        if self.terminal_session == True:
            print(answer)
        else:
            return answer

    def selector(self, args: str | None) -> None:
        self.args = None
        if self.terminal_session == True:
            command: str | bool = input("COMMAND: ")
            args: list[str] = command.split()
        else: args = args.split()
        module: str = args[0]
        key: str | None = args[1] if len(args) > 1 else None
        answer: str = str()
        match module:
            case "/help":
                match key:
                    case None:
                        answer = messages.HELP
                    case "ban":
                        answer = messages.HELP_BAN
                    case "category":
                        answer = messages.HELP_CATEGORY
                    case "join_requests":
                        answer = str()
                    case "sheets":
                        answer = messages.HELP_SHEETS
                    case "chat_notify_guard":
                        answer = messages.HELP_CHAT_NOTIFY_GUARD
                    case _:
                        answer = messages.HELP_EXCEPT
            case "/ban":
                reason: str = Utils.get_args_string(args, 3) if len(args) > 2 else "Забанен через тг"
                match key:
                    case "ban":
                        answer = self.Amino_ban.ban(link=args[2], reason= reason)
                    case "unban":
                        answer = self.Amino_ban.unban(link=args[2], reason= reason)
                    case _:
                        answer = messages.HELP_EXCEPT
            case "/category":
                match key:
                    case "start":
                        answer = self.Amino_category.start()
                    case "stop":
                        answer = self.Amino_category.stop()
                    case "restart":
                        answer = self.Amino_category.restart()
                    case _:
                        answer = messages.HELP_EXCEPT
            case "/chat_notify_guard":
                match key:
                    case "get":
                        answer = self.Amino_chat_notify_guard.get_chats()
                    case "update":
                        answer = self.Amino_chat_notify_guard.update_current_public_chats()
                    case "set":
                        answer = self.Amino_chat_notify_guard.select_chats_for_protect(Utils.get_args_subList(args, 2))
                    case "clear":
                        answer = self.Amino_chat_notify_guard.clear_chat_selector()
                    case "start":
                        answer = self.Amino_chat_notify_guard.start()
                    case "stop":
                        answer = self.Amino_chat_notify_guard.stop()
                    case "restart":
                        answer = self.Amino_chat_notify_guard.restart()
                    case _:
                        answer = messages.HELP_EXCEPT
            case "/join_requests":
                match key:
                    case "get":
                        answer = self.Amino_community_join_requests.get_join_requests()
                    case _:
                        answer = messages.HELP_EXCEPT
            case "/sheets":
                match key:
                    case "init":
                        if len(args) == 2:
                            answer = self.Sheets.start()
                        elif len(args) == 3:
                            answer = self.Sheets.start(Utils.get_args_string(args, 2))
                        else:
                            answer = messages.HELP_EXCEPT
                    case "get":
                        if len(args) == 3:
                            answer = self.Sheets.read_sheet(whichDate= args[2])
                        elif (len(args) == 3) & (args[2] == "today"):
                            answer = self.Sheets.read_sheet(whichDate= "today")
                        elif len(args) == 2:
                            answer = self.Sheets.read_sheet()
                        else:
                            answer = messages.HELP_EXCEPT
                    case "write":
                        answer = self.Sheets.write_sheet(Utils.get_args_subList(args, 2))
                    case _:
                        answer = messages.HELP_EXCEPT
            case _:
                answer = messages.HELP_EXCEPT
        return self.transponder(answer)


class Utils:
    def get_args_string(args: list, first_index: int, last_index: int | None= None) -> str:
        args_subList = Utils.get_args_subList(args, first_index, last_index)
        args_string: str = str()
        for arg in args_subList:
            args_string += arg
        return args_string

    def get_args_subList(args: list, first_index: int, last_index: int | None= None) -> list:
        args_subList: list = list()
        last_index: int = len(args) if last_index == None else last_index
        for arg in args:
            if (args.index(arg) >= first_index) & (arg.index(arg) <= last_index):
                args_subList.append(arg)
        return args_subList
