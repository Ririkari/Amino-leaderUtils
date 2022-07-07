class Amino_ban:
    def __init__(self, sub_client) -> None:
        self.sub_client = sub_client

    def get_id(self, link: str) -> str:
        try:
            response = self.sub_client.get_from_code(link).objectId
            return response
        except:
            return ""

    def ban(self, link: str, reason: str) -> str:
        userId: str = self.get_id(link)
        if userId != "":
            try:
                self.sub_client.ban(userId= userId, reason= reason)
                return str(f"Successfully banned :- [{userId}]")
            except:
                return str(f"Ban failed, cannot ban:- [{userId}]")
        else:
            return "Ban failed, cannot get userId"

    def unban(self, link: str, reason: str) -> str:
        userId: str = self.get_id(link)
        if userId != "":
            try:
                self.sub_client.unban(userId= userId, reason= reason)
                return str(f"Successfully unbanned :- [{userId}]")
            except:
                return str(f"Unban failed, cannot ban:- [{userId}]")
        else:
            return "Unban failed, cannot get userId"
    
    def ban_recent_users(self, quantity: int= 0) -> str:
        try:
            recent_user: list[dict] = self.sub_client.get_all_users(size=100).profile.json
        except:
            return "Ban failed, cannot get recent users"
        if quantity == 0:
            return "U forgot give quantity of users wich must be banned"
        else:
            for user in recent_user:
                if recent_user.index(user)+1 <= quantity:
                    uid = user.get("uid")
                    try:
                        self.sub_client.ban(uid, "чистка")
                        print(f"banned :- [{uid}]")
                    except:
                        pass
                else:
                    print("done")
                    return str(f"{quantity} users was successfully banned")
