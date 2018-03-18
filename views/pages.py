# -*- coding: utf-8 -*-
from libs.handlers import *
from db.models import *
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import logging
from datetime import timedelta, datetime, date

from blob_utils import core
from google.appengine.api import files, images
import random

'''
class sendMailPage(DirectHandler):
    def get(self):


        #sendMail(receiver='zouber129@gmail.com', subject=u'由GAE mail api 寄出的信', msg='<img src="http://lh5.ggpht.com/16JxmvwdCDNKtmUdjwi6I7fZnB8RX1x0N6ciRLYjwCufWYr_6OymINDlXOkNARemM4unvXvCFEeUPL_UTqbWZLO5X8_5" />')
'''

class ViewsPhotoPage(DirectHandler):
    def get(self):
        self.HtmlResponse('ViewsPhotoPage.html', {})

class BananaVsTomato(DirectHandler):
    def get(self):
        self.HtmlResponse('BananaVsTomato.html', {})

class BananaVsTomatoRules(DirectHandler):
    def get(self):
        self.HtmlResponse('BananaVsTomatoRules.html', {})

class BananaVsTomatoPlay(DirectHandler):
    def get(self):
        original_remain_time = 15
        self.HtmlResponse('BananaVsTomatoPlay.html', {'original_remain_time': original_remain_time})

class BananaVsTomatoResult(DirectHandler):
    def get(self):
        level = self.request.get('level')
        score = self.request.get('score')

        if level not in ['gold', 'silver', 'copper', 'finish']:
            level = 'finish'

        if not score:
            score = '0'

        if level == 'gold':
            level_prompt = score + u'分！你真是名副其實的番茄知識王！'
            level_name = u'金牌'
        elif level == 'silver':
            level_prompt = score + u'分！學識淵博，再加油一下就能奪得金牌！'
            level_name = u'銀牌'
        elif level == 'copper':
            level_prompt = score + u'分！有慧根，稍加練習一定不得了～'
            level_name = u'銅牌'
        else:
            level_prompt = u'恭喜完賽，請再接再厲！'
            level_name = u'完賽證明'


        self.HtmlResponse('BananaVsTomatoResult.html', {'level': level, 'level_name': level_name, 'level_prompt': level_prompt})
        
class BananaCameraPage(DirectHandler):
    def get(self):
        ua_string = self.request.headers['User-Agent']
        ua = parse(ua_string)

        desktop = self.request.get('desktop').lower()

        logging.info(desktop)
        logging.info(type(desktop))

        if desktop == 'true':
            # for testing
            self.HtmlResponse('DesktopBananaCameraPage.html', {})
        else:
            if ua.is_mobile or ua.is_tablet:
                self.HtmlResponse('MobileBananaCameraPage.html', {})
            else:
                self.HtmlResponse('PleaseOpenWithMobilePromptPage.html', {})
                #self.HtmlResponse('DesktopBananaCameraPage.html', {})

class BananaHoroscopePage(DirectHandler):
    def get(self):
        ua_string = self.request.headers['User-Agent']
        ua = parse(ua_string)

        desktop = self.request.get('desktop').lower()

        logging.info(desktop)
        logging.info(type(desktop))

        
        if desktop == 'true':
            # for testing
            self.HtmlResponse('DesktopBananaHoroscope.html', {})
        else:
            if ua.is_mobile or ua.is_tablet:
                self.HtmlResponse('MobileBananaHoroscope.html', {})
            else:
                #self.HtmlResponse('PleaseOpenWithMobilePromptPage.html', {})
                self.HtmlResponse('DesktopBananaHoroscope.html', {})

    def post(self):
        import urllib
        from libs.horoscope import *
        name = self.request.get('name')

        acc = 0
        for i in range(0, len(name)):
            acc = acc + ord(name[i])

        today = datetime.today()
        plus_8_hours = timedelta(hours=+8)
        # convert to GMT+8 time zone
        today = today + plus_8_hours

        year = today.year
        month = today.month
        day = today.day

        acc = acc + year + month + day

        how_many_result = len(horoscope_result)
        #result_index = random.randint(0,how_many_result-1)

        result_index = acc % how_many_result
        
        self.redirect('/banana_horoscope_result?result_index=%s&user_name=%s' % (result_index, urllib.quote(name.encode('utf-8'))))
        #self.redirect('/banana_horoscope_result?result_index=%s&user_name=%s' % (result_index, urllib.quote(name.encode('utf-8'))))

class BananaHoroscopeResultPage(DirectHandler):
    def get(self):
        from libs.horoscope import *

        ua_string = self.request.headers['User-Agent']
        ua = parse(ua_string)
        desktop = self.request.get('desktop').lower()

        user_name = self.request.get('user_name')
        result_index = self.request.get('result_index')

        try:
            result_index = int(result_index)
        except:
            result_index = 0

        result = horoscope_result[result_index]

        today = datetime.today()
        plus_8_hours = timedelta(hours=+8)
        # convert to GMT+8 time zone
        today = today + plus_8_hours

        year = today.year
        month = today.month
        day = today.day

        week_day_mapping = [u'一', u'二', u'三', u'四', u'五', u'六', u'日']
        weekday = week_day_mapping[today.weekday()]
        date_string = '%s/%s/%s(%s)' % (year, month, day, weekday)

        result['date_string'] = date_string

        if desktop == 'true':
            # for testing
            self.HtmlResponse('DesktopBananaHoroscopeResultPage.html', {'result': result, 'user_name': user_name})
        else:
            if ua.is_mobile or ua.is_tablet:
                self.HtmlResponse('MobileBananaHoroscopeResultPage.html', {'result': result, 'user_name': user_name})
            else:
                #self.HtmlResponse('PleaseOpenWithMobilePromptPage.html', {})
                self.HtmlResponse('DesktopBananaHoroscopeResultPage.html', {'result': result, 'user_name': user_name})

class DownloadPhotoPage(DirectHandler):
    def get(self):
        imgurl = self.request.get('imgurl')
        self.HtmlResponse('DownloadPhotoPage.html', {'imgurl': imgurl})

class GetPhotoPage(DirectHandler):
    def get(self):
        ua_string = self.request.headers['User-Agent']
        ua = parse(ua_string)
        logging.info(ua.is_mobile)

        if ua.is_mobile or ua.is_tablet:
            logging.info('mobile')
            self.HtmlResponse('MobileGetPhotoPage.html', {})
        else:
            logging.info('not mobile')
            #self.HtmlResponse('MobileGetPhotoPage.html', {})
            self.HtmlResponse('DesktopGetPhotoPage.html', {})

class GetPhotoDirectPage(DirectHandler):
    def get(self):
        self.HtmlResponse('GetPhotoDirectPage.html', {})

class Fetch(DirectHandler):
    def get(self):
        message = Message.get_by_id(5652786310021120)
        logging.info(message.name)

class EditItemPage(DirectHandler):
    def get(self):
        class_name = self.request.get('class_name')
        key_id = self.request.get('key_id')

        mobile_desktop_catalog = []
        pc_desktop_catalog = []

        if not class_name or not key_id:
            random_pic_num = random.randint(1,5)
            self.HtmlResponse('NotFoundPage.html', {'random_pic_num': random_pic_num, 'page_name': u'此頁面不存在喔～'})
        else:
            if class_name == 'News':
                item = News.get_by_id(int(key_id))
            elif class_name == 'Post':
                item = Post.get_by_id(int(key_id))
            elif class_name == 'EGoodie':
                mobile_desktop_catalog = DownloadItemCatalog.query(DownloadItemCatalog.category == 'mobile_desktop').fetch(30)
                pc_desktop_catalog = DownloadItemCatalog.query(DownloadItemCatalog.category == 'pc_desktop').fetch(30)
                item = EGoodie.get_by_id(int(key_id))
            elif class_name == 'DownloadItemCatalog':
                item = DownloadItemCatalog.get_by_id(int(key_id))
            elif class_name == 'Product':
                item = Product.get_by_id(int(key_id))
            elif class_name == 'Cooperation':
                item = Cooperation.get_by_id(int(key_id))
            else:
                item = None

            self.HtmlResponse('EditItemPage.html', {'page_name': 'EditItemPage', 'item': item, 'mobile_desktop_catalog': mobile_desktop_catalog, 'pc_desktop_catalog': pc_desktop_catalog})

class SiteMapPage(DirectHandler):
    def get(self):
        self.HtmlResponse('SiteMapPage.html', {'page_name': 'SiteMapPage'})

class NotFoundPage(DirectHandler):
    def get(self, **args):
        random_pic_num = random.randint(1,5)
        self.HtmlResponse('NotFoundPage.html', {'random_pic_num': random_pic_num, 'page_name': u'此頁面不存在喔～'})
        
class MainPage(DirectHandler):
    def get(self):
        news = News.query().order(-News.news_time).fetch(2)
        self.HtmlResponse('MainPage.html', {'page_name': 'MainPage', 'news': news})

class AboutUsPage(DirectHandler):
    def get(self):
        self.HtmlResponse('AboutUsPage.html', {'page_name': 'AboutUsPage'})

class NewsPage(DirectHandler):
    def get(self):
        '''
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        
        hot_news = News.query(ndb.AND(News.category == 'news', News.news_time >= today)).order(-News.news_time).fetch(20)
        past_news = News.query(ndb.AND(News.category == 'news', News.news_time < today)).order(-News.news_time).fetch(20)
        media_report = News.query(News.category == 'report').order(-News.news_time).fetch(20)
        self.HtmlResponse('NewsPage.html', {'page_name': 'NewsPage', 'hot_news': hot_news, 'past_news': past_news, 'media_report': media_report})
        '''

        news = News.query().order(-News.news_time).fetch(100)
        self.HtmlResponse('NewsPage.html', {'page_name': 'NewsPage', 'news': news})

class StoryPage(DirectHandler):
    def get(self):
        story = Post.query(Post.category == 'story').order(Post.build_time).fetch(30)
        sd_media_image = EGoodie.query(ndb.AND(EGoodie.category == 'sd_media', EGoodie.file_type == 'image')).order(EGoodie.build_time).fetch(100)
        sd_media_video = EGoodie.query(ndb.AND(EGoodie.category == 'sd_media', EGoodie.file_type == 'video')).order(EGoodie.build_time).fetch(100)
        self.HtmlResponse('StoryPage.html', {'page_name': 'StoryPage', 'story': story, 'sd_media_image': sd_media_image, 'sd_media_video': sd_media_video})

class ProductPage(DirectHandler):
    def get(self):
        '''
        virtual_product = Product.query(Product.type == 'virtual').fetch(200)
        physical_product = Product.query(Product.type == 'physical').fetch(200)

        
        category_list = ['life', 'cloth', 'accessory', 'stationery', 'kitchen', 'decoration', '3c', 'toy', 'food']
        product_data = {}

        for cate in category_list:
            product_data[cate] = Product.query(ndb.AND(Product.type == 'physical', Product.category == cate)).fetch(20)
        self.HtmlResponse('ProductPage.html', {'page_name': 'ProductPage', 'virtual_product': virtual_product, 'product_data': product_data, 'category_list': category_list})
        '''

        products = Product.query().order(Product.show_priority, -Product.build_time).fetch(500)
        self.HtmlResponse('ProductPage.html', {'page_name': 'ProductPage', 'products': products})
        

class DownloadPage(DirectHandler):
    def get(self):
        gifs = EGoodie.query(EGoodie.category == 'gif').fetch(30)
        fb_banners = EGoodie.query(EGoodie.category == 'fb_banner').fetch(30)
        mobile_desktop = DownloadItemCatalog.query(DownloadItemCatalog.category == 'mobile_desktop').order(-DownloadItemCatalog.build_time).fetch(50)
        pc_desktop = DownloadItemCatalog.query(DownloadItemCatalog.category == 'pc_desktop').order(-DownloadItemCatalog.build_time).fetch(50)
        self.HtmlResponse('DownloadPage.html', {'page_name': 'DownloadPage', 'gifs': gifs, 'fb_banners': fb_banners, 'mobile_desktop': mobile_desktop, 'pc_desktop': pc_desktop})

class CooperationPage(DirectHandler):
    def get(self):
        cooperations = Cooperation.query().order(-Cooperation.event_time).fetch(30)
        self.HtmlResponse('CooperationPage.html', {'page_name': 'CooperationPage', 'cooperations': cooperations, 'page_type': 'normal'})

class ViewDownloadFilePage(DirectHandler):
    def get(self):
        name = self.request.get('name')
        category = self.request.get('category')
        catalog_name = self.request.get('catalog_name')
        width = self.request.get('width')
        height = self.request.get('height')
        image = EGoodie.query(ndb.AND(EGoodie.category == category, EGoodie.catalog_name == catalog_name, EGoodie.width == width, EGoodie.height == height, EGoodie.name == name)).fetch(1)

        if len(image) > 0:
            image = image[0]
            img_width = int(image.width)
            img_height = int(image.height)

            image_container_size = img_height
            if img_width > img_height:
                image_container_size = img_width
        else:
            image = None

        self.HtmlResponse('ViewDownloadFilePage.html', {'page_name': 'ViewDownloadFilePage', 'image': image, 'image_container_size': image_container_size})

class ContactUsSubmit(DirectHandler):
    def post(self):
        name = self.request.get('name')
        tel = self.request.get('tel')
        email = self.request.get('email')
        company = self.request.get('company')
        company_desc = self.request.get('company_desc')
        title = self.request.get('title')
        proposal = self.request.get('proposal')

        proposal = proposal.replace('\n', '<br/>')

        Message.add_item(name=name, tel=tel, email=email, company=company, company_desc=company_desc, title=title, proposal=proposal)

        cooperations = Cooperation.query().order(-Cooperation.event_time).fetch(30)

        # notify admin
        self.proposal_notification(name, tel, email, company, proposal)

        self.HtmlResponse('CooperationPage.html', {'page_name': 'CooperationPage', 'cooperations': cooperations, 'page_type': 'after_submit'})

class NewsBrowsePage(DirectHandler):
    def get(self):
        news = News.query().order(-News.news_time).fetch(10)
        self.HtmlResponse('NewsBrowsePage.html', {'news': news})

class DataUpdate(DirectHandler, blobstore_handlers.BlobstoreUploadHandler):
    def update_news(self):
        DEFAULT_CATEGORY = 'news'
        key_id = self.request.get('key_id')
        category = self.request.get('category', DEFAULT_CATEGORY)
        title = self.request.get('title')
        subtitle = self.request.get('subtitle')
        location = self.request.get('location')
        description = self.request.get('description')
        media_name = self.request.get('media_name')

        news_year = int(self.request.get('news_year'))
        news_month = int(self.request.get('news_month'))
        news_day = int(self.request.get('news_day'))

        news_time = datetime(news_year, news_month, news_day)

        description = description.replace('\n', '<br/>')

        DEFAULT_THUMB_URL = '/media/img/sambardeer_logo_1.png'
        
        img_blob = self.request.get('thumb')
        
        if img_blob:
            try:
                logging.info(type(img_blob))
                img_obj = images.Image(img_blob)
                logging.info(img_obj)
                logging.info(img_obj.width)
                #img_obj.im_feeling_lucky()
                #png_binary = img_obj.execute_transforms(output_encoding=images.PNG)

                #output_obj = images.Image(png_binary)
                #logging.info(type(output_obj))
                img, blob_key, width, height = core.blob_upload(img_blob, 'thumb', 'image/png')

                upload_result_url = images.get_serving_url(img)

                logging.info(upload_result_url)
            except:
                upload_result_url = DEFAULT_THUMB_URL
        else:
            # default thumb
            upload_result_url = DEFAULT_THUMB_URL

        # if update mode without new image upload
        if key_id and not img_blob:
            upload_result_url = self.request.get('thumb_url')

        # update(with entity key)
        if key_id:
            News.update_item(key_id=key_id, category=category, title=title, subtitle=subtitle, location=location, description=description, media_name=media_name, thumb_url=upload_result_url, news_time=news_time)
        else:
            News.add_item(category=category, title=title, subtitle=subtitle, location=location, description=description, media_name=media_name, thumb_url=upload_result_url, news_time=news_time)

    def update_story(self):
        DEFAULT_CATEGORY = 'story'
        key_id = self.request.get('key_id')
        category = self.request.get('category', DEFAULT_CATEGORY)
        title = self.request.get('title')
        content = self.request.get('content')
        content = content.replace('\n', '<br/>')

        DEFAULT_THUMB_URL = '/media/img/sambardeer_logo_1.png'
        
        img_blob = self.request.get('image')
        
        if img_blob:
            try:
                img_obj = images.Image(img_blob)
                img, blob_key, width, height = core.blob_upload(img_blob, 'thumb', 'image/png')

                upload_result_url = images.get_serving_url(img)
            except:
                upload_result_url = DEFAULT_THUMB_URL
        else:
            # default thumb
            upload_result_url = DEFAULT_THUMB_URL

        # if update mode without new image upload
        if key_id and not img_blob:
            upload_result_url = self.request.get('thumb_url')

        # update(with entity key)
        if key_id:
            Post.update_item(key_id=key_id, category=category, title=title, content=content, image=upload_result_url)
        else:
            Post.add_item(category=category, title=title, content=content, image=upload_result_url)

    def update_character(self):
        name = self.request.get('name')

        birthday_year = int(self.request.get('birthday_year'))
        birthday_month = int(self.request.get('birthday_month'))
        birthday_day = int(self.request.get('birthday_day'))
        birthday = datetime(birthday_year, birthday_month, birthday_day)

        pet_phrase = self.request.get('pet_phrase')
        personality = self.request.get('personality')
        super_power = self.request.get('super_power')
        occupation = self.request.get('occupation')
        like = self.request.get('like')
        hate = self.request.get('hate')

        Character.add_item(name=name, birthday=birthday, pet_phrase=pet_phrase, personality=personality, super_power=super_power, occupation=occupation, like=like, hate=hate)

    def update_egoodie(self):
        key_id = self.request.get('key_id')
        item_type = self.request.get('item_type')
        name = self.request.get('name')
        category = self.request.get('category')
        width = self.request.get('width')
        height = self.request.get('height')
        video_url = self.request.get('video_url')
        img_blob = self.request.get('image_file')

        if category == 'mobile_desktop':
            catalog_name = self.request.get('mobile_catalog_name')
        elif category == 'pc_desktop':
            catalog_name = self.request.get('pc_catalog_name')
        elif category == 'gif':
            catalog_name = self.request.get('gif_catalog_name')
        else:
            catalog_name = ''

        if item_type == 'image':
            if img_blob:
                try:
                    img_obj = images.Image(img_blob)
                    img, blob_key, img_width, img_height = core.blob_upload(img_blob, 'thumb', 'image/png')
                    upload_result_url = images.get_serving_url(img)
                except:
                    upload_result_url = self.request.get('thumb_url')
            else:
                upload_result_url = self.request.get('thumb_url')

        logging.info(upload_result_url)

        # update item(with entity key)
        if key_id:
            logging.info('update case')
            if item_type == 'image':
                EGoodie.update_item(key_id=key_id, file_type=item_type, name=name, category=category, width=width, height=height, file_url=upload_result_url, catalog_name=catalog_name)
            elif item_type == 'video':
                EGoodie.update_item(key_id=key_id, file_type=item_type, name=name, category=category, width=width, height=height, file_url=video_url, catalog_name=catalog_name)
        # add item
        else:
            if item_type == 'image':
                EGoodie.add_item(file_type=item_type, name=name, category=category, width=width, height=height, file_url=upload_result_url, catalog_name=catalog_name)
            else:
                EGoodie.add_item(file_type=item_type, name=name, category=category, width=width, height=height, file_url=video_url, catalog_name=catalog_name)

    def write_blob(self, data, info):
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
        )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)
        return files.blobstore.get_blob_key(blob)

    def get_file_size(self, file):
        file.seek(0, 2)  # Seek to the end of the file
        size = file.tell()  # Get the position of EOF
        file.seek(0)  # Reset the file position to the beginning
        return size

    def update_product(self):
        DEFAULT_THUMB_URL = '/media/img/sambardeer_logo_1.png'
        key_id = self.request.get('key_id')
        item_type = self.request.get('item_type')
        product_name = self.request.get('name')
        category = self.request.get('category')
        description = self.request.get('description')
        description = description.replace('\n', '<br/>')
        where_to_buy = self.request.get('where_to_buy')
        upload_result_urls = []

        import re
        for name, fieldStorage in self.request.POST.items():
            #logging.info(name) --> 欄位名稱
            #logging.info(fieldStorage) --> 欄位內容(值或是檔案), 檔案print 出來類似 FieldStorage(u'image_files', u'105705.jpg')

            if type(fieldStorage) is not unicode:
                #logging.info(fieldStorage.file) --> ex: <cStringIO.StringO object at 0xfbc1fba0>

                result = {}
                result['name'] = re.sub(
                    r'^.*\\',
                    '',
                    fieldStorage.filename
                )
                result['type'] = fieldStorage.type
                result['size'] = self.get_file_size(fieldStorage.file)

                blob_key = str(
                    self.write_blob(fieldStorage.value, result)
                )

                upload_result_urls.append(images.get_serving_url(blob_key))

        if key_id:
            # if update mode without new image upload
            if len(upload_result_urls) == 0:
                temp = self.request.get('thumb_urls').split(',')
                for url in temp:
                    upload_result_urls.append(url)
            Product.update_item(key_id=key_id, type=item_type, name=product_name, category=category, description=description, where_to_buy=where_to_buy, image_urls=upload_result_urls)
        else:
            if len(upload_result_urls) == 0:
                upload_result_urls.append(DEFAULT_THUMB_URL)

            Product.add_item(type=item_type, name=product_name, category=category, description=description, where_to_buy=where_to_buy, image_urls=upload_result_urls)

    def update_download_item_catalog(self):
        DEFAULT_THUMB_URL = '/media/img/sambardeer_logo_1.png'
        key_id = self.request.get('key_id')
        name = self.request.get('name')
        category = self.request.get('category')

        upload_result_url = DEFAULT_THUMB_URL

        img_blob = self.request.get('cover_image')
        if img_blob:
            try:
                img_obj = images.Image(img_blob)
                img, blob_key, img_width, img_height = core.blob_upload(img_blob, 'thumb', 'image/png')
                upload_result_url = images.get_serving_url(img)
            except:
                upload_result_url = ''

        # if update mode without new image upload
        if key_id and not img_blob:
            upload_result_url = self.request.get('thumb_url')

        # update(with entity key)
        if key_id:
            DownloadItemCatalog.update_item(key_id=key_id, name=name, category=category, cover_image=upload_result_url)
        else:
            DownloadItemCatalog.add_item(name=name, category=category, cover_image=upload_result_url)

    def update_cooperation(self):
        DEFAULT_THUMB_URL = '/media/img/sambardeer_logo_1.png'
        key_id = self.request.get('key_id')
        cooperation_name = self.request.get('name')
        subtitle = self.request.get('subtitle')
        partner = self.request.get('partner')
        location = self.request.get('location')
        description = self.request.get('description')
        description = description.replace('\n', '<br/>')
        
        event_year = int(self.request.get('event_year'))
        event_month = int(self.request.get('event_month'))
        event_day = int(self.request.get('event_day'))
        event_hour = int(self.request.get('event_hour'))
        event_minute = int(self.request.get('event_minute'))
        event_time = datetime(event_year, event_month, event_day, event_hour, event_minute)
        upload_result_urls = []

        import re
        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is not unicode:
                result = {}
                result['name'] = re.sub(
                    r'^.*\\',
                    '',
                    fieldStorage.filename
                )
                result['type'] = fieldStorage.type
                result['size'] = self.get_file_size(fieldStorage.file)

                blob_key = str(
                    self.write_blob(fieldStorage.value, result)
                )

                upload_result_urls.append(images.get_serving_url(blob_key))

        # update case
        if key_id:
            # if update mode without new image upload
            if len(upload_result_urls) == 0:
                temp = self.request.get('thumb_urls').split(',')
                for url in temp:
                    upload_result_urls.append(url)
            Cooperation.update_item(key_id=key_id, name=cooperation_name, subtitle=subtitle, partner=partner, location=location, description=description, event_time=event_time, image_urls=upload_result_urls)
        else:
            if len(upload_result_urls) == 0:
                upload_result_urls.append(DEFAULT_THUMB_URL)

            Cooperation.add_item(name=cooperation_name, subtitle=subtitle, partner=partner, location=location, description=description, event_time=event_time, image_urls=upload_result_urls)

    def post(self):
        item_class = self.request.get('item_class', 'news')

        if item_class == 'news':
            self.update_news()
        elif item_class == 'character':
            self.update_character()
        elif item_class == 'egoodie':
            self.update_egoodie()
        elif item_class == 'product':
            self.update_product()
        elif item_class == 'cooperation':
            self.update_cooperation()
        elif item_class == 'story':
            self.update_story()
        elif item_class == 'download_item_catalog':
            self.update_download_item_catalog()

        self.HtmlResponse('DataUpdateCompletePage.html', {'msg': u'資料更新完成！'})

class BackendPage(DirectHandler):
    def get(self):
        from google.appengine.api import users

        user = users.get_current_user()
        if user:
            user_mail = user.email()

            if user_mail in ADMIN_MEMBERS:
                news = News.query().order(-News.build_time).fetch(500)
                posts = Post.query().order(-Post.build_time).fetch(500)

                mobile_desktop_catalog = DownloadItemCatalog.query(DownloadItemCatalog.category == 'mobile_desktop').order(-DownloadItemCatalog.build_time).fetch(100)
                pc_desktop_catalog = DownloadItemCatalog.query(DownloadItemCatalog.category == 'pc_desktop').order(-DownloadItemCatalog.build_time).fetch(100)
                
                messages = Message.query().order(-Message.build_time).fetch(300)

                egoodies = EGoodie.query().order(-EGoodie.build_time).fetch(300)

                download_item_catalogs = DownloadItemCatalog.query().order(-DownloadItemCatalog.build_time).fetch(100)

                products = Product.query().order(Product.show_priority, -Product.build_time).fetch(500)
                #products = Product.query().fetch(500)

                cooperations = Cooperation.query().order(-Cooperation.build_time).fetch(300)

                self.HtmlResponse('BackendPage.html', {'page_name': 'BackendPage', 'mobile_desktop_catalog': mobile_desktop_catalog, 'pc_desktop_catalog': pc_desktop_catalog, 'messages': messages, 'news': news, 'posts': posts, 'egoodies': egoodies, 'download_item_catalogs': download_item_catalogs, 'products': products, 'pds': products, 'cooperations': cooperations})
            else:
                import random
                random_pic_num = random.randint(1,5)
                self.HtmlResponse('NotFoundPage.html', {'random_pic_num': random_pic_num, 'page_name': u'此頁面不存在喔～'})
        else:
            self.redirect(users.create_login_url(self.request.uri))

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)

class UploadHandlerPage(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/file_upload_test')

        template = '''
            <form method="post" action="%s" enctype="multipart/form-data">
                <input type="file" name="default">
                <input type="submit">
            </form>
        '''% (upload_url)

        self.response.out.write(template)

        '''
        for b in blobstore.BlobInfo.all():
            logging.info(str(b.key()))
            logging.info(type(b.filename))
            logging.info(str(b.filename.encode('utf-8')))
            

            #logging.info( str(b.key()) + '/' + str(b.filename.encode('utf-8')) )
            #self.response.out.write('<li><a href="/serve/%s' % str(b.key()) + '">' + str(b.filename.encode('utf-8')) + '</a>')
        '''

    def post(self):
        #logging.info(type(self.get_uploads('default')))
        #logging.info(type(self.get_uploads('default')[0]))
        upload_file_type = self.get_uploads('default')[0].content_type

        # image
        if 'image' in upload_file_type:
            from google.appengine.api import images
            img = self.get_uploads('default')[0]
            result = images.get_serving_url(img)
        # other file type
        else:
            upload_files = self.get_uploads('default')  # 'file' is file upload field in the form
            blob_info = upload_files[0]
            result = '/serve/%s' % blob_info.key()
        
        self.response.out.write(result)