# coding=utf-8
import os
import re
import time
import random
from bs4 import BeautifulSoup

from request_utils import request_util
from logger import logger
from save_file import save_file
from spider_config import spider_config
from proxy_utils import proxies


class Spider:

    def __init__(self):
        # 已经爬取完成的商店id
        self.shopid_file = spider_config.shopid_file
        self.shop_ids = []

        self.stop_review = False
        self.result_file = spider_config.result_file
        self.year_limit = spider_config.year_limit
        self.url = spider_config.url
        self.cookie = spider_config.cookie
        self.user_agent = spider_config.user_agent
        self.host = spider_config.host

        self.headers = {
            'User-Agent': self.user_agent,
            'Cookie': self.cookie,
            "Host": self.host
        }

        # 加载已经爬取完成的商店id
        self.load_shopid()

    def load_shopid(self):
        if not os.path.exists(self.shopid_file):
            return []

        with open(self.shopid_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                self.shop_ids.append(line.strip())

    def get_css_content(self, html, url):
        # 获取保存字体信息的css链接
        css_links = re.search(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.net/v1/.*?.css)">', html)

        if css_links is None:
            logger.error("获取css内容失败！请检查链接：%s" % url)
            print("验证完成后请输入任意字符继续")
            input()
            while True:
                print("是否更新一下内容？0 不更新 1 cookie 2 user-agent")
                ipt = input().strip()
                if ipt == "0":
                    break
                elif ipt == "1":
                    self.headers["Cookie"] = input().strip()
                elif ipt == "2":
                    self.headers["User-Agent"] = input().strip()
            return None, None

        css_link = "http:%s" % css_links.group(1)

        css_content = request_util.get(css_link, headers=self.headers)

        return css_link, css_content.text

    def get_font_library(self, css_content, css_link):
        # 获取字体库链接
        svg_links = re.search(r'svgmtsi.*?(//s3plus.meituan.net/v1.*?svg)\);', css_content)

        if svg_links is None:
            logger.error("查找字体库失败！请检查css链接:%s" % css_link)
            input()
            return None, None

        svg_link = "http:%s" % svg_links.group(1)

        svg_html = request_util.get(svg_link, headers=self.headers)
        svg_text = svg_html.text

        save_file.save_message("./tmp/svg.svg", svg_text)

        y_list = re.findall('<text x="0" y="(.*?)"', svg_text)
        text_list = re.findall('<text x="0" y=".*?">(.*?)</text>', svg_text)
        font_size = re.findall(r'font-size:(.*?)px;fill:#333;}', svg_text)[0]
        font_size = int(font_size)

        font_dict = {}
        for i in range(0, len(y_list)):
            for index, word in enumerate(text_list[i]):
                x = index * font_size
                y = int(y_list[i]) - 23
                font_dict["%s,%s" % (str(x), str(y))] = word

        return font_dict

    def get_review_detail(self, html):
        reviews_info = []
        page_review = BeautifulSoup(html, "html.parser")

        main_reviews = page_review.find_all("div", class_="main-review")
        for main_review in main_reviews:
            # 用户名
            user_name = main_review.find("div", class_="dper-info").text.strip()

            print("爬取用户: %s 的评论" % user_name)

            # 时间
            review_time = main_review.find(class_="time")
            review_time = re.sub("\\s+", " ", review_time.text).strip()
            sp = review_time.split("-")
            if int(sp[0]) < self.year_limit:
                self.stop_review = True
                break

            # 评论内容
            review_words = main_review.find("div", class_="review-words Hide")
            # 评论没有隐藏内容
            if review_words is None:
                review_words = main_review.find(class_="review-words").text
                review_words = review_words.strip()
            else:
                # 删除“收起评论”以及空白字符
                review_words = review_words.text.strip()[:-4].strip()

            # 评论的长度
            review_len = len(review_words)

            # 是否提到“霸王餐”或“免费体验”
            free_trial = 0
            if "霸王餐" in review_words or "免费体验" in review_words:
                free_trial = 1

            # 是否为“免费体验后评价”
            rich_title = main_review.find("div", class_="richtitle")
            if rich_title is not None and "免费体验后评价" in rich_title:
                rich_title = 1
            else:
                rich_title = 0

            # “喜欢的菜”数量
            review_recommend_num = 0
            review_recommend = main_review.find("div", class_="review-recommend")
            if review_recommend is not None:
                a_recommend = review_recommend.find_all("a")
                review_recommend_num = len(a_recommend)

            # 评论总打分、分维度评分
            review_rank = main_review.find("div", class_="review-rank")
            score_star = re.findall('<span class="sml-rank-stars sml-str(.*?) star"></span>', str(review_rank))
            score_star = float(score_star[0]) / 10
            score_dim = re.sub("\\s+", " ", review_rank.text).strip()

            # 点赞、回应、收藏数
            num_prf = [0, 0, 0]
            actions_contents = main_review.find("span", class_="actions").contents
            i = -1
            for ac in actions_contents:
                if ac.name != "a" and ac.name != "em":
                    continue

                if ac.name == "a":
                    i += 1

                if ac.name == "em":
                    num_prf[i] = int(ac.text.strip()[1:-1])

                if i > 3:
                    break

            # 评论图片数
            picture_num = 0
            review_pictures = main_review.find(class_="review-pictures")
            if review_pictures is not None:
                a_num = review_pictures.find_all("a")
                picture_num = int(len(a_num))

            reviews_info.append([user_name, review_words, rich_title, free_trial,
                                 review_recommend_num, score_star, score_dim, review_len,
                                 picture_num] + num_prf + [review_time])

        return reviews_info

    def get_shop_info(self, html):
        page = BeautifulSoup(html, "html.parser")

        page_shop = page.find("div", class_="review-shop-wrap")

        # 商家名
        shop_info_clearfix = page_shop.find("div", class_="shop-info clearfix")
        shop_name = shop_info_clearfix.text.strip()

        rank_info = page_shop.find("div", class_="rank-info")

        # 商家总评分
        score_star = re.findall('<div class="star_score.*?">(.*?)</div>', str(rank_info))
        score_star = float(score_star[0])

        # 分维度评分
        score = rank_info.find(class_="score")
        score_dim = re.sub("\\s+", " ", score.text).strip()

        # 评论总数
        reviews = rank_info.find(class_="reviews")
        review_num = re.findall('([0-9]+)', str(reviews.text))
        review_num = int(review_num[0])

        # 价格
        price_tag = rank_info.find(class_="price")
        price = re.findall("([0-9]+)", str(price_tag.text))
        price = int(price[0])

        return [shop_name, score_star, score_dim, price, review_num]

    def each_review_page(self, review_url):
        # self.headers["Referer"] = shop_url

        css_link, css_content = None, None
        # 获取css信息失败后，需要在浏览器验证后重新请求
        while css_content is None:
            r = request_util.get(review_url, headers=self.headers)
            html = r.text

            css_link, css_content = self.get_css_content(html, review_url)

        save_file.save_message("./tmp/css.css", css_content)

        font_dict = self.get_font_library(css_content, css_link)

        # 将加密的字体替换成正常文字
        font_keys = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', html)
        for fk in font_keys:
            pos_key = re.findall(r'.' + fk + '{background:-(.*?).0px -(.*?).0px;}', css_content)
            x = pos_key[0][0]
            y = pos_key[0][1]
            html = html.replace('<svgmtsi class="' + fk + '"></svgmtsi>', font_dict[x + ',' + y])

        save_file.save_message("./tmp/page.html", html)

        shop_info = self.get_shop_info(html)
        reviews_info = self.get_review_detail(html)

        for i, ri in enumerate(reviews_info):
            reviews_info[i] = shop_info + ri

        save_file.write_csv_rows(self.result_file, reviews_info)

    def each_shop_review(self, shop_url):
        allreview_url = "%s/%s" % (shop_url, "review_all")

        r = request_util.get(allreview_url, headers=self.headers)
        page = BeautifulSoup(r.text, "html.parser")

        page_count = 0
        page_links = page.find_all("a", class_="PageLink")

        # 获取店铺网页的页数
        for p in page_links:
            if str.isdigit(p.text):
                page_count = page_count if page_count > int(p.text) else int(p.text)

        # 处理每个评论页
        for i in range(1, page_count):
            review_url = "%s/%s" % (allreview_url, "p" + str(i))

            print("爬取网页: %s" % review_url)
            time.sleep(5 + random.randint(2, 4))

            self.stop_review = False
            self.each_review_page(review_url)

            if self.stop_review:
                break

    def each_page(self, page_url):
        r = request_util.get(page_url, headers=self.headers)

        page = BeautifulSoup(r.text, "html.parser")
        shop_all_list = page.find(id="shop-all-list")
        tit_div = shop_all_list.find_all("div", class_="tit")

        # 爬取每家店的评论
        for t in tit_div:
            shop_url = t.a["href"]

            sp = shop_url.split("/")
            shop_id = sp[len(sp) - 1].strip()

            if shop_id in self.shop_ids:
                continue

            self.shop_ids.append(shop_id)
            save_file.save_message(self.shopid_file, shop_id + "\n", mode="a")

            self.each_shop_review(shop_url=shop_url)

    def spider(self):
        r = request_util.get(self.url, headers=self.headers)
        save_file.save_message("./tmp/spider.html", r.text, encoding=r.encoding)

        page = BeautifulSoup(r.text, "html.parser")

        page_count = 0
        page_div = page.find("div", class_="page")
        page_link = page_div.find_all(class_="PageLink")

        for p in page_link:
            if str.isdigit(p.text):
                page_count = page_count if page_count > int(p.text) else int(p.text)

        for i in range(1, page_count):
            page_url = "%s/%s" % (self.url, "p" + str(i))
            self.each_page(page_url)


if __name__ == "__main__":
    print("是否覆盖结果文件： 0 不覆盖 1 覆盖")
    mode = input().strip()

    if mode == "1" and os.path.exists(spider_config.result_file):
        os.remove(spider_config.result_file)

        # 在开头写入utf-8编码的bom，防止excel双击打开时乱码
        csv_titles = ['\ufeff' + "商家名", "商家的总评分", "商家的分维度评分", "商家的人均价格", "商家被评论总数",
                      "用户名", "每条评论的内容", "该评论是否为“免费体验后评价“", "该评论内容中是否提到“霸王餐”或“免费体验”",
                      "评论中“喜欢的菜”的数量", "每条评论的总打分", "每条评论的分维度评分", "每条评论的长度",
                      "每条评论的配图数", "每条评论的点赞数量", "每条评论的回应数量", "每条评论的收藏数量", "评论时间"]

        save_file.write_csv_row(spider_config.result_file, csv_titles)

    save_file.mkdir("./tmp")

    Spider().spider()