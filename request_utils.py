import sys
import requests

from logger import logger
from proxy_utils import proxies


class RequestUtils:

    def __init__(self):
        pass

    def get(self, url, headers):
        # print(url)
        try:
            r = requests.get(url, headers=headers)

            # 需要验证
            while "验证中心" in r.text or "页面不存在" in r.text:
                logger.warning("请复制连接 %s 到浏览器进行验证" % url)
                input()
                r = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            logger.error("%s 网络连接失败！" % url)
            sys.exit()

        if r.status_code != 200:
            logger.error("响应码不是200")
            print(r.status_code)
            print(r.content)

        return r


request_util = RequestUtils()