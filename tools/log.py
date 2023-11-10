import logging
import os
import time

PROJECT_PATH = fr'D:\learn\github\xet'


class MyFormatter(logging.Formatter):
    """带颜色的格式化器"""

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)
        self.colors = {
            'DEBUG': '\033[1;37;40m',  # 白色
            'INFO': '\033[1;32;40m',  # 绿色
            'WARNING': '\033[1;33;40m',  # 黄色
            'ERROR': '\033[1;31;40m',  # 红色
            'CRITICAL': '\033[1;35;40m',  # 紫色
        }

    def format(self, record):
        """重载 format 方法，使用 LogRecord 的 __repr__ 方法添加颜色"""
        message = super().format(record)
        levelname = record.levelname
        color = self.colors.get(levelname, '')
        return f"{color}{message}\033[0m"  # 添加颜色和重置颜色的代码


class Logger:
    def __init__(self, name, log_file, level=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level or logging.INFO)
        self.logger.propagate = True
        formatter = MyFormatter(
            "%(asctime)s %(levelname)s [%(processName)s:%(process)d][%(threadName)s:%(thread)d] [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
        # create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s [%(processName)s:%(process)d][%(threadName)s:%(thread)d] [%(module)s:%(funcName)s:%(lineno)d] %(message)s'))

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


logger = Logger('GG', os.path.join(PROJECT_PATH,
                                   f'log/log_{time.strftime("%Y_%m_%d", time.localtime(time.time()))}.log'),
                level=logging.DEBUG).logger
