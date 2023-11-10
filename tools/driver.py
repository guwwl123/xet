"""
selenium driver 再次封装模块
"""
import json
import os
import re
import time
from time import sleep

import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from tools.log import logger

cookies1 = []


# browser = Browser()


class ProjectPath:
    project_path = r'C:\Users\wanligu\Documents\GG'


def mock(return_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return return_value

        return wrapper

    return decorator


def wrapper(func):
    """装饰器函数"""

    def inner(*args, **kwargs):
        self = args[0]
        if self.driver_log_switch:
            try:
                strFuncName = func.__name__
                self.log("Call %s%s" % (strFuncName, args[1:]))
            except:
                pass
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            self.print_screen()

    return inner


class Browser:
    """ 浏览器类 , 对 selenium 驱动再次封装"""

    def __init__(self, log_func=print, driver_log_switch=True, driver=None):
        """
       log_func: 日志处理函数
       driver_log_switch：debug日志开关,如果不想看到driver日志,可以屏蔽掉(改为False)
       """
        self.log = log_func
        self.driver_log_switch = driver_log_switch
        self.driver = driver if driver else None

        # 获取当前项目目录
        current_path = ProjectPath.project_path
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        # 保存截图的路径
        self.dir4save = os.path.join(current_path, 'pictures')
        self.pic_name = '%s.png' % current_time
        # 判断是否已存在文件夹
        if not os.path.exists(self.dir4save):
            os.makedirs(self.dir4save)

        self.pic_path = os.path.join(self.dir4save, self.pic_name)

    @wrapper
    def print_screen(self, name=''):
        """
        截图,保存当前浏览器界面
        :param name: 自定义照片名称
        :return: None
        """
        # 默认照片名称
        pic_path = self.pic_path
        # 自定义照片名称
        if name:
            name += '.png'
            pic_path = os.path.join(self.dir4save, name)
        self.driver.save_screenshot(pic_path)

    @wrapper
    def open(self, url, browser_type='chrome'):
        """
        用浏览器打开指定URL
        :param url: 网址
        :param browser_type: 浏览器种类(需要提前安装驱动)
        :return:None
        """
        if not self.driver:
            if browser_type == 'chrome':
                self.driver = webdriver.Chrome()
            elif browser_type == 'firefox':
                self.driver = webdriver.Firefox()
            elif browser_type == 'ie':
                self.driver = webdriver.Ie()
            else:
                self.log('未安装此(:%s)浏览器驱动,将使用默认driver' % browser_type)
                self.driver = webdriver.Chrome()

        self.driver.get(url)
        self.driver.maximize_window()
        self.wait(3)

    @wrapper
    def quit(self):
        """Quits the driver and closes every associated window."""
        self.driver.quit()

    @wrapper
    def close(self):
        """ Closes the current window."""
        self.driver.close()

    @wrapper
    def clear(self, operand, by='xpath'):
        """
        清除输入框内容
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).clear()

    @wrapper
    def input(self, operand, value, by='xpath'):
        """
        向输入框输入内容
        :param operand:操作对象
        :param value:
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).send_keys(value)

    @wrapper
    def click(self, operand, by='xpath'):
        """
        点击
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).click()

    @wrapper
    def mousedown(self, operand, by='xpath'):
        """
        按下鼠标左键不放,Holds down the left mouse button on an element.
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:
        """
        ActionChains(self.driver).click_and_hold(self.driver.find_element(by, operand)).perform()

    @wrapper
    def wait(self, seconds):
        """
        等待
        :param seconds:等待时间(秒)
        :return:None
        """
        sleep(int(seconds))

    @wrapper
    def waitAppear(self, operand, timeout=60, by='xpath'):
        """
        等待控件出现
        :param operand:操作对象
        :param timeout:超时时间
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        timeout = int(timeout)
        while timeout > 0:
            if self.isElementPresent(operand, by):
                return True
            timeout -= 1
            self.wait(1)
        return False

    @wrapper
    def waitDisappear(self, operand, timeout=60, by='xpath'):
        """
        等待控件消失
        :param operand:操作对象
        :param timeout:超时时间
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        timeout = int(timeout)
        while timeout > 0:
            if not self.isElementPresent(operand, by):
                return True
            timeout -= 1
            self.wait(1)
        return False

    @wrapper
    def isElementPresent(self, operand, by='xpath'):
        """
        判断控件是否存在
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        try:
            self.driver.find_element(by, operand)
            return True
        except:
            return False

    @wrapper
    def getElementCount(self, operand, by='xpath'):
        """
        统计控件个数
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:控件个数
        """
        count = len(self.driver.find_elements(by, operand))
        return count

    @wrapper
    def getAttribute(self, operand, attribute, by='xpath'):
        """
        获取控件属性
        :param operand:操作对象
        :param attribute:属性名称
        :param by:查找控件的方式,默认xpath
        :return:控件属性
        """
        return self.driver.find_element(by, operand).get_attribute(attribute)

    @wrapper
    def getValue(self, operand, by='xpath'):
        """
        获取控件的value
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:字段value的值
        """
        return self.getAttribute(operand, 'value', by)

    @wrapper
    def refresh(self):
        """刷新"""
        self.driver.refresh()

    @wrapper
    def switch_to_window(self, Index=-1):
        """
        切换操作浏览器窗口
        :param Index: # 0表示跳回原窗口,负数的绝对值越小离原窗口越近,正数越小离原窗口越远
        :return:None
        """
        # 获得当前浏览器所有窗口
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[Index])

    @wrapper
    def switch_to_frame(self):
        """Switch focus to the default frame."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element('xpath', '/html/body/iframe'))

    @wrapper
    def click_hold(self, operand, by='xpath'):
        """用于拖动(如淘宝等)验证滑块"""
        action = ActionChains(self.driver)
        attrible = self.driver.find_element(by, operand)
        action.click_and_hold(attrible)
        action.move_by_offset(308, 44)
        action.release().perform()

    @wrapper
    def change_attribute_value(self, operand, types, value, by='xpath'):
        """
        改变元素属性
        :param operand:操作对象
        :param types:属性类型
        :param value:值
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        ele1 = self.driver.find_element(by, operand)
        self.driver.execute_script("arguments[0].%s='%s'" % (types, value), ele1)


def shop_get():
    url = "https://study.xiaoe-tech.com/xe.learn-pc/my_attend_normal_list.get/1.0.1"

    payload = json.dumps({
        "page_size": 16,
        "page": 1,
        "agent_type": 7,
        "resource_type": [
            "0"
        ]
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/json',
        'Cookie': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # logger.info(json.dumps(response.json()['data']['list'], ensure_ascii=False))
    res = response.json()['data']['list']

    return list(
        filter(lambda x: x['resource_type'] == 6 and x['resource_count'] > 0, res))


def _course_get(app_id, resource_id, index=1, size=10):
    url = f"https://{app_id}.h5.xiaoeknow.com/xe.course.business.column.items.get/2.0.0"

    payload = f"bizData%5Bcolumn_id%5D={resource_id}&bizData%5Bpage_index%5D={index}&bizData%5Bpage_size%5D={size}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Cookie': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        # logger.info(json.dumps(response.json()['data']['list'], ensure_ascii=False))
        return response.json()['data']['list']
    except:
        raise Exception(f'接口调用失败: {url}')


def course_get(app_id, resource_id, size=100):
    res = []
    index = 1
    while True:
        resp = _course_get(app_id, resource_id, index, size)
        res.extend(resp)
        index += 1
        if not resp:
            break
    return res


def get_all_course_urls(all_course: list[dict], product_id):
    for course in all_course:
        url = f'https://{course["app_id"]}.h5.xiaoeknow.com/p/course/video/{course["resource_id"]}?product_id={product_id}'
        course['url'] = url
    # logger.info(all_course)
    return all_course


def _setup():
    server = Server(r"D:\learn\xet\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
    try:
        server.stop()
    except:
        pass
    server.start()
    proxy = server.create_proxy()

    # 配置Proxy启动WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # 解决 您的连接不是私密连接问题
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-urlfetcher-cert-requests')

    driver = webdriver.Chrome(options=chrome_options)

    browser = Browser(driver_log_switch=False, driver=driver)
    browser.open('https://study.xiaoe-tech.com/t_l/learnIndex#/muti_index')

    # 将cookie添加到WebDriver的cookie集合中
    for cookie in cookies1:
        browser.driver.add_cookie(cookie)

    return browser, server, proxy


def get_m3u8_urls(shop_info, course_urls, browser, proxy):
    browser.open('https://study.xiaoe-tech.com/t_l/learnIndex#/muti_index')
    btn2 = f'//*[@id="common_template_mounted_el_container"]//div[contains(text(),"{shop_info["title"]}")]'
    browser.waitAppear(btn2)
    browser.click(btn2)
    browser.wait(3)

    all_window_handles = browser.driver.window_handles
    browser.close()
    browser.driver.switch_to.window(all_window_handles[1])

    m3u8_urls = {}
    m3u8_urls_retry = {}
    # for course_url_info in course_urls[:2]:
    for course_url_info in course_urls:
        proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
        # browser.open('https://appic0e5vkp6806.h5.xiaoeknow.com/p/course/column/p_639aa079e4b02685a4282aa1')
        browser.open(course_url_info['url'])
        logger.debug(course_url_info['resource_title'])
        #  browser.wait(3)
        # bnt = '//*[@id="comments_list"]/div[1]/div/div[1]/div[1]/span[contains(text(),"01.剪映界面介绍·上")]'
        # browser.waitAppear(bnt)
        # browser.click(bnt)
        # browser.driver.implicitly_wait(5)
        browser.wait(5)
        result = proxy.har

        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # logger.info(_url)
            # if 'm3u8' in _url or 'drm' in _url:
            if '.ts?' in _url:
                # response = entry['response']
                url = entry['request']['url']
                logger.debug(url)
                m3u8_urls[course_url_info['resource_title']] = url
                break
        else:
            m3u8_urls_retry[course_url_info['resource_title']] = course_url_info['url']

    if len(course_urls) == len(m3u8_urls.keys()):
        logger.info(f'收集完成的如下: {m3u8_urls}')
    else:
        logger.info(f'收集失败的如下: {m3u8_urls_retry}\n收集完成的如下: {m3u8_urls}')

    return m3u8_urls, m3u8_urls_retry


def m3u8_make(m3u8_urls: dict):
    m3u8_urls = {name: re.sub(r"(_0.ts|\.ts)", ".m3u8", m3u8_urls[name]) for name in m3u8_urls}
    return {name: re.sub(r"start=\d*&end=\d*", "", m3u8_urls[name]) for name in m3u8_urls}


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"目录 {path} 创建成功")
    else:
        logger.info(f"目录 {path} 已存在")


def download(url, video_name, work_dir, shop_name, course_name):
    tool_path = r'C:\Users\wanligu\Documents\GG\code_learning\tools\N_m3u8DL-CLI_v3.0.2\N_m3u8DL-CLI_v3.0.2.exe'
    shop_folder = os.path.join(work_dir, shop_name)
    video_folder = os.path.join(shop_folder, course_name)
    create_directory(video_folder)
    cmd = f'{tool_path} "{url}" --workDir {video_folder} --saveName {video_name} --enableDelAfterDone'
    logger.info(cmd)
    # res = os.popen(cmd)
    # logger.info(res)
