'''
Created on 2018年9月18日

@author: iw12082
'''
import scrapy
import time
import json
import hmac
from twisted.python.compat import raw_input
from hashlib import sha1


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    }
    allowed_domins = ["zhihu.com"]
    
    headers = {
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
        }
    
    def start_requests(self):
        start_urls = ["https://www.zhihu.com/signup?next=%2F"]
        
        for url in start_urls:
            yield scrapy.Request(url=url, meta={'cookiejar':1}, callback=self.parse)
        
    
    
    def parse(self, response):
        cookies = response.headers.getlist('Set-Cookie')
        xsrf = cookies[2]
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',
                             headers=self.headers, meta={'cookiejar': response.meta["cookiejar"]}, callback=self.is_need_capture)
        
    def is_need_capture(self, response):
        cookies = response.headers.getlist('Set-Cookie')
        rcookies = response.request.headers.getlist('Cookie')
        yield scrapy.Request('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                             headers=self.headers, meta={'cookiejar': response.meta["cookiejar"], "resp": response}, callback=self.capture)

    def capture(self, response):
        cookies = response.headers.getlist('Set-Cookie')
        rcookies = response.request.headers.getlist('Cookie')
        with open('../di_captcha.gif', 'wb') as f:
            # 下载图片必须以二进制来传输
            f.write(response.body)
            f.close()

        need_cap = json.loads(response.meta.get("resp", "").text)["show_captcha"] # {"show_captcha":false}表示不用验证码
#         grantType = 'password'
#         clientId = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
#         source = 'com.zhihu.web'
#         timestamp = str(int(round(time.time() * 1000)))  # 毫秒级时间戳 签名只按这个时间戳变化
# 
#         post_data = {
#             "client_id": clientId,
#             "username": "15208393732",  # 输入知乎用户名
#             "password": "R393732k",  # 输入知乎密码
#             "grant_type": grantType,
#             "source": source,
#             "timestamp": timestamp,
#             "signature": self.get_signature(grantType, clientId, source, timestamp),  # 获取签名
#             "lang": "cn",
#             "ref_source": "homepage",
#             "captcha": self.get_captcha(need_cap),  # 获取图片验证码
#             "utm_source": ""
#         }
        post_data  = {
             "username": "",  # 输入知乎用户名
             "password": "",  # 输入知乎密码
             "captcha": self.get_captcha(need_cap),  # 获取图片验证码
            }
        
        return [scrapy.FormRequest(
            url="https://www.zhihu.com/api/v3/oauth/sign_in",
            formdata=post_data,
            meta={'cookiejar': response.meta["cookiejar"]},
            headers=self.headers,
            callback=self.check_login
        )]
    def err_login(self, failure):
        failure
        
    def check_login(self, response):
        # 验证是否登录成功
        print(response)
        yield scrapy.Request('https://www.zhihu.com/inbox', headers=self.headers)
        pass
    
    def get_captcha(self, need_cap):
        """处理验证码 """
        if need_cap is False:
            return ""
        # with open('tudi_captcha.gif', 'wb') as fb:
        #     fb.write(data)
        return input('captcha:')

    def get_signature(self, grantType, clientId, source, timestamp):
        """处理签名"""
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
        hm.update(str.encode(grantType))
        hm.update(str.encode(clientId))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())
