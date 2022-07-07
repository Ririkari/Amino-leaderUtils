class Amino_community_join_requests:
    def __init__(self, acm) -> None:
        self.acm = acm

    def get_join_requests(self) -> str | bool:
        try:
            response: dict = self.acm.get_join_requests(size= 100).json
        except:
            return "Get join requests filed, cannot get join requests"
        if type(response) is dict:
            return self.unpack_respons_data(response.get("communityMembershipRequestList"))
 
    def unpack_respons_data(self, response: list) -> str:
        requests: str = str(f'[ОБЩЕЕ КОЛ-ВО ЗАПРОСОВ]: {len(response)}\n\n')
        for i, user_request in enumerate(response):
            time_of_created_user_join_requst = user_request.get("createdTime")
            user_request_message = user_request.get("message")
            user_data = user_request.get("applicant")
            user_nickname = user_data.get("nickname")
            user_profileIcon = user_data.get("icon")
            requests += str(
f'''
    ---[{i}]---
[НИКНЕЙМ]: {user_nickname}, 
[СООБЩЕНИЕ]: {user_request_message},
[ДАТА ЗАПРОСА]: {time_of_created_user_join_requst}, 
[ИКОНКА]: {user_profileIcon}\n
''')
        return requests


'''
{'status': 1, 'requestId': 'e48ec19d-0f48-483d-b8f0-b384cf56aac5', 'modifiedTime': '2022-01-20T02:09:45Z', 'ndcId': 253410987, 'createdTime': '2022-01-20T02:09:45Z', 'message': '3\nНет \nРаньше состояла здесь и мне очень понравилось', 'applicant': {'status': 0, 'uid': '584549b3-600c-43c8-941e-737d412a84e6', 'isGlobal': True, 'role': 0, 'isStaff': None, 'nickname': 'Нитан', 'icon': 'http://pm1.narvii.com/8138/652901c9988ce25b686b429aa693441ffcaed60cr1-640-640v2_00.jpg'}, 'uid': '584549b3-600c-43c8-941e-737d412a84e6'}

'''
