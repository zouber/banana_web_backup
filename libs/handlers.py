# -*- coding: utf-8 -*-
import os
import urllib
import webapp2
import jinja2
import logging
from libs.config import *
from libs.dictionary import *
#import sys
import re
from google.appengine.api import mail
from user_agents.parsers import *


ADMIN_MEMBERS = [
    'mrbbstartup@gmail.com'
    #'salendia@gmail.com',
    #'zouber129@gmail.com'
    #'finyao1214@gmail.com'
]

PAGE_CHINESE_NAME = {
    'MainPage': u'首頁',
    'NewsPage': u'香蕉新聞',
    'AboutUsPage': u'關於我們',
    'StoryPage': u'故事介紹',
    'ProductPage': u'好物',
    'DownloadPage': u'下載',
    'CooperationPage': u'合作',
    'SiteMapPage': u'網站地圖'
}

NOTIFY_MAIL_TEMPLATE = u'''
    <div style="font-size: 10pt; line-height: 18px">
        Dear 管理員，提案資訊如下：
        <br/>
        <table style="min-width: 400px; border: 1px solid black; border-collapse: collapse; margin-bottom: 5px; margin-top: 5px">
            <tr style="background-color: #f2f2f2">
                <td style="padding: 10px">姓名</td>
                <td style="padding: 10px">${name}</td>
            </tr>
            <tr>
                <td style="padding: 10px">電話</td>
                <td style="padding: 10px">${tel}</td>
            </tr>
            <tr style="background-color: #f2f2f2">
                <td style="padding: 10px">電子郵件</td>
                <td style="padding: 10px">${email}</td>
            </tr>
            <tr>
                <td style="padding: 10px">單位</td>
                <td style="padding: 10px">${company}</td>
            </tr>
            <tr style="background-color: #f2f2f2">
                <td style="padding: 10px">合作內容</td>
                <td style="padding: 10px">${proposal}</td>
            </tr>
        </table>
        請儘速討論回覆～ 加油！<br/>
        或到 <a href="http://www.sambardeer.co/backend">管理後台</a> 
        <br/><br/>
        三博鹿小幫手
    </div>
'''

def datetimeformat(datetime):
    # 參考 http://mymissionlog.blogspot.tw/2015/01/google-app-engine.html
    #logging.info( type(datetime.strftime('%Y/%m/%d') ) )
    #return datetime.strftime('%Y/%m/%d')

    return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日'

def transfer_single_url_into_hyperlink(match_gp):
    url = match_gp.group(0)
    return '<a href="%s" target="_blank" class="content_hyperlink">%s</a>' % (url, url)

def url_to_hyperlink(content):
    return re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', transfer_single_url_into_hyperlink, content)

def br_to_slash_n(content):
    return content.replace('<br/>', '\n')

def get_page_name(ent_name):
    if PAGE_CHINESE_NAME.has_key(ent_name):
        return PAGE_CHINESE_NAME[ent_name]
    else:
        return ''

def datetimeformat_withhour(datetime):
    if datetime.hour == 0 and datetime.minute == 0:
        return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日'
    else:
        return str(datetime.year) + u'年' + str(datetime.month) + u'月' + str(datetime.day) + u'日 ' + '%02d' % datetime.hour + u'：' + '%02d' % datetime.minute

def decide_header_icon_class(page_name, item_number):
    if page_name == 'MainPage' and item_number == 1:
        return 'header_icon_focus'
    elif page_name == 'NewsPage' and item_number == 2:
        return 'header_icon_focus'
    elif page_name == 'AboutUsPage' and item_number == 3:
        return 'header_icon_focus'
    elif page_name == 'StoryPage' and item_number == 4:
        return 'header_icon_focus'
    elif page_name == 'ProductPage' and item_number == 5:
        return 'header_icon_focus'
    elif page_name == 'DownloadPage' and item_number == 6:
        return 'header_icon_focus'
    elif page_name == 'CooperationPage' and item_number == 7:
        return 'header_icon_focus'
    else:
        return 'header_icon'

def translation(lang, string):
    if not lang or not string:
        return False
    else:
        if DICTIONARY.has_key(lang):
            if DICTIONARY[lang].has_key(string):
                return DICTIONARY[lang][string]
            else:
                return string
        else:
            return string


def generate_video_frame_html(url, width, height):
    if 'www.youtube.com' in url:
        video_id = url.replace('https://www.youtube.com/watch?v=', '')
        return u'<iframe width="%s" height="%s" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % (width, height, video_id)
    elif 'vimeo.com' in url:
        video_id = url.replace('https://vimeo.com/', '')
        return u'<iframe src="//player.vimeo.com/video/%s" width="%s" height="%s" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>' % (video_id, width, height)
    elif url is None:
        return 'None'
    else:
        return u'<div style="width: %spx, height: %spx">查無此影片格式</div>' % (width, height)

def convert_image_url(url, frame_size):
    if 'ggpht.com' in url:
        return url + '=s%s' % frame_size
    else:
        return url

def convert_item_category_to_chinese(category, class_name):
    CATEGORY_MAPPING = {
        'News': {
            'news': u'消息',
            'report': u'媒體報導'
        },
        'Post': {
            'story': u'故事介紹',
            'about_us': u'關於我們'
        },
        'EGoodie': {
            'image': u'圖片',
            'video': u'影片',
            'sd_media': u'SD 遊樂園',
            'fb_banner': u'FB封面',
            'pc_desktop': u'電腦桌布',
            'mobile_desktop': u'手機桌布'
        },
        'DownloadItemCatalog': {
            'mobile_desktop': u'手機桌布',
            'pc_desktop': u'電腦桌布'
        },
        'Product': {
            'virtual': u'虛擬商品',
            'physical': u'實體商品',
            'life': u'生活',
            'cloth': u'服飾',
            'accessory': u'配件',
            'stationery': u'文件',
            'kitchen': u'餐廚',
            'decoration': u'家飾',
            '3c': u'3C',
            'toy': u'玩具',
            'food': u'食品'
        }
    }
    
    if CATEGORY_MAPPING.has_key(class_name):
        if CATEGORY_MAPPING[class_name].has_key(category):
            return CATEGORY_MAPPING[class_name][category]

    return category


JINJA_ENVIRONMENT = jinja2.Environment(
    #loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    loader=jinja2.FileSystemLoader('template'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.filters['datetimeformat'] = datetimeformat
JINJA_ENVIRONMENT.filters['datetimeformat_withhour'] = datetimeformat_withhour
JINJA_ENVIRONMENT.filters['decide_header_icon_class'] = decide_header_icon_class
JINJA_ENVIRONMENT.filters['generate_video_frame_html'] = generate_video_frame_html
JINJA_ENVIRONMENT.filters['get_page_name'] = get_page_name
JINJA_ENVIRONMENT.filters['br_to_slash_n'] = br_to_slash_n
JINJA_ENVIRONMENT.filters['convert_item_category_to_chinese'] = convert_item_category_to_chinese
JINJA_ENVIRONMENT.filters['convert_image_url'] = convert_image_url
JINJA_ENVIRONMENT.filters['url_to_hyperlink'] = url_to_hyperlink
JINJA_ENVIRONMENT.filters['translation'] = translation

def sendMail(**args):
    if args.has_key('msg'):
        msg = args['msg']
    else:
        msg = ''

    if args.has_key('receiver'):
        receiver = args['receiver']
    else:
        receiver = ''

    if args.has_key('subject'):
        subject = args['subject']
    else:
        subject = ''

    if not msg or not receiver or not subject:
        return False
    else:
        sender_address = "三博鹿小幫手<zouber129@gmail.com>"
        message = mail.EmailMessage(sender=sender_address, subject=subject)
        message.to = receiver
        message.html = msg
        message.send()

class DirectHandler(webapp2.RequestHandler):
    def get_host(self):
        from urlparse import urlparse
        return urlparse(self.request.url).netloc

    def get_path(self):
        from urlparse import urlparse
        return urlparse(self.request.url).path

    def checkSuperAdmin(self):
        host = self.get_host()
        if host == 'www.fanshop.tw' or host == 'showtime-taipei.appspot.com/':
            # for online machine, the administrator identity assignment will be more strict
            return super_administrator_for_online_machine
        else:
            return list(set(super_administrator_for_testing_machine)|set(super_administrator_for_online_machine))

    def proposal_notification(self, name, tel, email, company, proposal):
        import string
        subject = u'鐺鐺鐺～ 有合作提案來囉！'

        receiver = ','.join(ADMIN_MEMBERS)

        #receiver = 'zouber129@gmail.com,zouber@tagtoo.org'
        tmp = string.Template(NOTIFY_MAIL_TEMPLATE)
        msg = tmp.safe_substitute(name=name, tel=tel, email=email, company=company, proposal=proposal)
        sendMail(receiver=receiver, subject=subject, msg=msg)

    def HtmlResponse(self, template_name, template_values):
        logging.info(self.request.headers['User-Agent'])

        ua_string = self.request.headers['User-Agent']
        ua = parse(ua_string)
        logging.info(ua.is_mobile)

        #logging.info('Cookie: %s' % self.request.cookies.get('lang'))

        lang = self.request.cookies.get('lang')
        if not lang:
            lang = 'tw'

        if not DICTIONARY.has_key(lang):
            lang = 'tw'
        template_values['dict'] = DICTIONARY[lang]

        template_values['version'] = os.environ['CURRENT_VERSION_ID']

        template_values['lang'] = lang

        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        logging.info(os.path.dirname(__file__))
        #template_path = os.path.join(os.path.dirname(__file__), 'template', template_name)
        template_path = template_name
        template = JINJA_ENVIRONMENT.get_template(template_path)
        template_values['host'] = self.request.host
        template_values['path'] = self.get_path()
        self.response.write(template.render(template_values))

    def JsonResponse(self, status, value):
        import json

        callback = self.request.get("callback")

        value['status'] = status
        value['callback'] = callback
        # http://webapp-improved.appspot.com/guide/request.html#common-request-attributes
        value['host'] = self.request.host
        logging.info('host url: %s' % self.request.host_url)

        self.response.headers["Content-Type"] = "application/x-javascript"
        
        if callback:
            self.response.write("%s(%s)" % (callback, json.dumps(value, indent=4, sort_keys=True, separators=(',', ': '))))
        else:
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(json.dumps(value, indent=4, sort_keys=True, separators=(',', ': ')))
            # don't raise "Internal Server Error(500)" when encounter status == False
            #if not status:
            #    self.response.set_status(500)