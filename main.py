from tools.driver import shop_get, _setup, course_get, get_all_course_urls, get_m3u8_urls, m3u8_make
from tools.log import logger

if __name__ == '__main__':
    work_dir = fr'D:\videos'
    # 1.获取所有课堂信息course_info,包括( app_id 和 resource_id )
    # shop_infos = shop_get()[:1]
    shop_infos = shop_get()
    # logger.info(json.dumps(shop_get(), ensure_ascii=False))
    browser, server, proxy = _setup()
    ok = []
    retry = []
    for shop_info in shop_infos:
        # 2.获取指定课堂的课程信息,根据shop_info中的 app_id 和 resource_id
        course_info = course_get(shop_info['app_id'], shop_info['resource_id'])
        # logger.info(course_info)
        # 3.根据course_info拼接出每个课堂的每个课程的url
        course_info_with_url = get_all_course_urls(course_info, shop_info['resource_id'])
        # logger.info(course_info_with_url)
        # logger.info(len(course_info_with_url))
        # 4.根据course_info_with_url 模拟点击后, 获取m3u8 url
        m3u8_url_dict, m3u8_urls_retry = get_m3u8_urls(shop_info, course_info_with_url, browser, proxy)
        m3u8_urls = m3u8_make(m3u8_url_dict)
        # logger.info(m3u8_urls)
        ok.append(m3u8_urls)
        retry.append(m3u8_urls_retry)
        # # 5.根据 m3u8_urls 下载
        # for name, url in m3u8_urls.items():
        #     download(url, name, work_dir, shop_info['shop_name'], shop_info['title'])
    server.stop()
    logger.info(f'OK:\n{ok}')
    logger.info(f'RETRY:\n{retry}')
