import sys, json
from os import path
import aminofix as amino


class Amino_login:
    def __init__(self, needACM: bool = False) -> None:
        email, password, aminoId = self.auth()
        client = amino.Client()
        print(f"Login:\n    Email: {email}\n    Password: {password}\n    Amino ID: {aminoId}")
        client.login(email, password)
        self.sub_client = amino.SubClient(aminoId= aminoId, profile= client.profile)
        if needACM == True:
            comId = amino.Client().search_community(aminoId).comId[0]
            self.acm = amino.ACM(profile= client.profile, comId= comId)
        print("Logined.")
        self.botId: str = str(self.sub_client.profile.userId)

    def init_authFile(self) -> None:
        try:
            for i in range(0,2):
                if i == 0:
                    dumpData: tuple[str, str, str] = (str(), str(), str())
                else:
                    dumpData: tuple[str, str, str] = (
                            str(input("Email: ")),
                            str(input("Password: ")), 
                            str(input("Amino ID: "))
                            )
                with open("src/lib/init/auth.json", "w", encoding= "utf-8") as File:
                    json.dump(
                            {
                                "email": dumpData[0],
                                "password": dumpData[1],
                                "aminoId": dumpData[2]
                            },
                            File
                        )         
        except OSError:
            print("@@Error! Cannot init auth file! Exit!")
            sys.exit()

    def auth(self) -> list:
        if path.isfile("src/lib/init/auth.json") == False:
            self.init_authFile()
        elif path.isfile("src/lib/init/auth.json") == True:
            is_true_auth_data: str = str()
            while (is_true_auth_data != "Y") and (is_true_auth_data != "N"):
                is_true_auth_data = input('Start with last settings?: "Y"/"N": ').upper()
                if (is_true_auth_data != "Y") and (is_true_auth_data != "N"):
                    print("Wrong input! Try again!")
            if is_true_auth_data == "N":
                self.init_authFile()
        try:
            auth = self.read_authFile()
        except OSError:
            print("@@Error! Cannot read auth file! Exit!")
            sys.exit()
        return auth

    def read_authFile(self) -> list:
        with open("src/lib/init/auth.json", "r", encoding= "utf-8") as File:
            data: dict = json.load(File)
            auth = [str(data.get("email")), str(data.get("password")), str(data.get("aminoId"))]
            for auth_data in auth:
                if auth_data == "":
                    self.init_authFile()
                    return self.read_authFile()
                if (auth.index(auth_data) == 0) and ((auth_data.find("@") == -1) | (auth_data.find(".") == -1)):
                    self.init_authFile()
                    return self.read_authFile()
                if (auth.index(auth_data) == 1) and (len(auth_data) < 6):
                    self.init_authFile()
                    return self.read_authFile()
            return auth

