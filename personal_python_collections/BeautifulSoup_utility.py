from bs4 import BeautifulSoup
from bs4 import ResultSet
from bs4 import element
import shlex


# [API] https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html


class BeautifulSoupManager:
    def __init__(self, text, features='html.parser'):
        self.__soup = BeautifulSoup(text, features)

    @property
    def soup(self):
        """BeautifulSoup对象
        :return: :class:`BeautifulSoup <BeautifulSoup>` object
        :rtype: BeautifulSoup
        """

        return self.__soup

    def find_all(self, attribute_name=None, string=None):
        """查询出来的结果集合
        :return: :class:`ResultSet <ResultSet>` object
        :rtype: ResultSet
        """

        if string is None:
            return self.__soup.find_all(name=attribute_name)
        else:
            item_list = string.split('=')
            key = item_list[0].strip()
            values_string_list = shlex.split(item_list[1].strip())
            return self.__soup.find_all(name=attribute_name, attrs={key: values_string_list})


class BeautifulSoupElement:

    def __init__(self, item):
        self.__item = item

    @property
    def is_Tag(self):
        """是否是Tag对象
        :return: :class:`bool <bool>` object
        :rtype: bool
        """
        return isinstance(self.__item, element.Tag)

    @property
    def is_NavigableString(self):
        """是否是NavigableString对象
        :return: :class:`bool <bool>` object
        :rtype: bool
        """
        return isinstance(self.__item, element.NavigableString)

    @property
    def is_Comment(self):
        """是否是Comment对象
        :return: :class:`bool <bool>` object
        :rtype: bool
        """
        return isinstance(self.__item, element.Comment)

    def is_match(self, attribute_name, string=None):
        """是否符合查询条件,例如,attribute_name='div' string='class=download_pic'
        :return: :class:`bool <bool>` object
        :rtype: bool
        """

        if string is None:
            return self.__item.name == attribute_name
        else:
            item_list = string.split('=')
            key = item_list[0].strip()
            values_string_list = shlex.split(item_list[1].strip())
            return self.__item.name == attribute_name and self.__item.attrs == {key: values_string_list}
