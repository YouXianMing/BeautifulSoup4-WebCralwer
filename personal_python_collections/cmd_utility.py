
import subprocess


class Process:

    # http://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p06_executing_external_command_and_get_its_output.html
    # https://docs.python.org/3/library/subprocess.html

    def __init__(self, args):

        self.__args = args
        self.__output = None
        self.__error = None
        self.__return_code = None

    # Property
    # ---------------------------------------

    @property
    def output(self):
        """ 输出信息

        :return: :class:`web_str <web_str>` object
        :rtype: str
        """
        return self.__output

    @property
    def error(self):
        """ 错误信息

        :return: :class:`web_str <web_str>` object
        :rtype: str
        """
        return self.__error

    @property
    def return_code(self):
        """ 错误信息

        :return: :class:`int <int>` object
        :rtype: int
        """
        return self.__return_code

    # Public method
    # ---------------------------------------

    def run(self, timeout=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True):

        process = subprocess.Popen(self.__args, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell)

        try:

            outs, errs = process.communicate(timeout=timeout)
            self.__output = outs.decode('utf-8')
            self.__error = errs.decode('utf-8')

        except subprocess.TimeoutExpired:

            process.kill()
            outs, errs = process.communicate()
            self.__output = outs.decode('utf-8')
            self.__error = errs.decode('utf-8')

        self.__return_code = process.returncode

        return self
