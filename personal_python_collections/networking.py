
import requests
import urllib.request


class Networking:

    def __init__(self, url, download_file_path=None, reporthook=None):
        """ 网络初始化

        :param url: 网络地址
        :param download_file_path: 本地文件路径,调用urlretrieve方法时有用,也可以不设置
        :param reporthook: 下载信息的回调
        """

        # 网址
        self.url = url

        # 设置本地存储路径,可以不设置
        self.download_file_path = download_file_path

        # 设置下载进度回调
        self.reporthook = reporthook

        # 下载完信息后返回的路径
        self.__file_path = None

        # 下载完后获取的信息
        self.__message = None

        # requests请求的response对象
        self.__response = None

    # Property
    # ---------------------------------------

    @property
    def response(self):
        """ Get the Response object.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.__response

    @property
    def file_path(self):
        """ 文件路径

        :return: :class:`web_str <web_str>` object
        :rtype: str
        """

        return self.__file_path

    @property
    def message(self):
        """ 文件路径

        :return: :class:`HTTPMessage <HTTPMessage>` object
        :rtype: http.client.HTTPMessage
        """

        return self.__message

    # Public method
    # ---------------------------------------

    def get(self, params=None, **kwargs):
        """ Sends a GET request.

        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Networking <Networking>` object
        :rtype: Networking
        """

        self.__response = requests.get(self.url, params=params, **kwargs)
        return self

    def post(self, data=None, json=None, **kwargs):
        """Sends a POST request.

        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Networking <Networking>` object
        :rtype: Networking
        """

        self.__response = requests.post(self.url, data=data, json=json, **kwargs)
        return self

    def download(self, data=None):

        self.__file_path, self.__message = urllib.request.urlretrieve(self.url,
                                                                      self.download_file_path,
                                                                      self.reporthook,
                                                                      data)

        return self
