from threading import Thread


class Amino_category():
    def __init__(self, sub_client, botId: str) -> None:
        self.isStarted: bool = False
        self.sub_client = sub_client
        self.botId: str = botId

    def check_recent_blogs(self) -> None:
        while self.isStarted == True:
            if self.isStarted == False:
                return
            try:
                blogs = self.sub_client.get_recent_blogs(size= 100).json
            except:
                continue
            for data in blogs:
                blog_type_data: str = data.get('strategyInfo')
                story_type: int = blog_type_data.find('"objectSubType": "story"')
                crossPost_type: int = blog_type_data.find('"objectSubType": "crossPost"')
                if (story_type == -1) and (crossPost_type == -1):
                    author = data.get("author")
                    blogId = data.get("blogId")
                    nickname = author.get("nickname")
                    try:
                        blog_data = self.sub_client.get_blog_info(blogId= blogId).json
                    except:
                        continue
                    category = blog_data.get("taggedBlogCategoryList")
                    if category == None: #==
                        try:
                            self.sub_client.comment(
                                        blogId= blogId,
                                        message= str(f"""
                                            Здравствуйте, {nickname}, ваш пост скрыт из-за отсутствия категории. Этим самым Вы нарушили пункт 2.7 правил нашего сообщества амино. Ознакомьтесь, пожалуйста, с правилами, там есть инструкция с картинками о том, как это сделать. После установки категории, ваш пост автоматически откроется и станет вновь доступным.
                                        """)
                                    )
                        except:
                            pass
                        try:
                            self.sub_client.hide(blogId= blogId, reason= "2.7 - Отсутствие категории")
                            print(f"[{blogId}] - hide")
                        except:
                            continue

    def check_hidden_blogs(self) -> None:
        while self.isStarted == True:
            if self.isStarted == False:
                return
            try:
                blogs = self.sub_client.get_hidden_blogs(size= 100).json
            except:
                continue
            for data in blogs:
                author = data.get("author")
                blogId = data.get("blogId")
                nickname = author.get("nickname")
                try:
                    blog_data = self.sub_client.get_blog_info(blogId= blogId).json
                except:
                    continue
                category = blog_data.get("taggedBlogCategoryList")
                if category != None: #!=
                    try:
                        blog_comments = self.sub_client.get_blog_comments(blogId= blogId).author.userId
                    except:
                        continue
                    if (self.botId in blog_comments) == True:
                        try:
                            self.sub_client.unhide(blogId= blogId, reason= "Категория была установлена")
                            print(f"[{blogId}] - unhide")
                        except:
                            continue
                        try:
                            self.sub_client.comment(
                                    blogId= blogId,
                                    message= str(f"""
                                        {nickname}, большое спасибо! Ваш пост вновь доступен!
                                    """)
                                    )
                        except:
                            pass

    def start(self) -> str:
        if self.isStarted == False:
            self.isStarted = True
            self.recentBlogs_thread = Thread(target= self.check_recent_blogs, args=())
            self.hiddenBlogs_thread = Thread(target= self.check_hidden_blogs, args=())

            self.recentBlogs_thread.start()
            self.hiddenBlogs_thread.start()
            answer: str = "Amino category module is started"
            print(answer)
            return answer
        else:
            answer: str = 'Amino category module is already started'
            print(answer)
            return answer

    def stop(self) -> str:
        if self.isStarted == True:
            self.isStarted = False
            del self.recentBlogs_thread
            del self.hiddenBlogs_thread
            answer: str = 'Amino category module is stoped'
            print(answer)
            return answer
        else:
            answer: str = 'Amino category module is already stoped'
            print(answer)
            return answer

    def restart(self) -> str:
        if self.isStarted == False:
            answer: str = "Amino category wasn't started for restarting. Cannot restart"
            print(answer)
            return answer
        else:
            self.stop()
            self.start()
            answer: str ='Amino category module was restarted'
            print(answer)
            return answer

    def list(self, needHiden= False) -> str:
        if needHiden == True:
            return self.needHiden()
        else:
            return "Неопределенная ошибка"

    def needHiden(self) -> str:
        try:
            hiden_blogs: list[dict] = self.sub_client.get_hidden_blogs(size= 100).json
        except:
            return "Не получилось получить данные с сервера"
        answer: str = str("[HIDEN BLOGS]:\n\n")
        for index, blog_data in enumerate(hiden_blogs):
            author: dict | None = blog_data.get("author")
            answer += str(
f"""
        [{index}]: blog_data.get("title")
[AUTHOR NICKNAME]: {author.get("nickname")},
[AUTHOR UID]: {blog_data.get("uid")}
[BLOG ID]: {blog_data.get("blogId")}.
\n
""")
        return answer
