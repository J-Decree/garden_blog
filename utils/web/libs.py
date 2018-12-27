import datetime
import json


def get_article_action_count(queryset):
    """
    :param queryset: <QuerySet [{'count': 1}]>
    :return: 1
    """
    queryset = list(queryset)
    ret = 0 if not queryset else  queryset[0]['count']
    return ret


class ArticleReaderHandler(object):
    config_name = 'read_config'
    config_type = 'cookie'  # cookie or session
    expires = 30  # 设置超时为30天

    def __init__(self, request, req):
        self.request = request
        self.req = req
        self.config = None
        self.__init_config()

    def __init_config(self):
        if self.config_type == 'cookie':
            config = self.request.COOKIES.get(self.config_name)
        elif self.config_type == 'session':
            config = self.request.session.get(self.config_name)
        self.config = json.loads(config) if config else {}

    @property
    def is_config_null(self):
        return len(self.config) == 0

    def set_config(self):
        config = json.dumps(self.config)
        if self.config_type == 'cookie':
            self.req.set_cookie(self.config_name, config)
        elif self.config_type == 'session':
            self.request.session[self.config_name] = config

    def write_now(self, article_id):
        self.config[article_id] = datetime.datetime.now(). \
            strftime("%Y-%m-%d %H:%M:%S")
        self.set_config()

    def check_article_been_read(self, article_id):
        """
               self.config: {1:'2018-9-8 22:10:2'),2:'2018-9-8 22:10:30'}
               :return: 
        """
        if self.is_config_null or article_id not in self.config:
            # 不在配置里面,写入当前时间
            self.write_now(article_id)
            return False
        else:
            # 存在，判断是否超时
            ago = datetime.datetime.strptime(self.config[article_id], "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            expires = datetime.timedelta(days=30)
            if now - ago > expires:
                # 超过时间
                self.config.pop(article_id)
                self.write_now(article_id)
                return False
            else:
                return True
