# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from datetime import timedelta, datetime
import logging

class TomatoRecord(ndb.Model):
    device_id = ndb.StringProperty()
    action = ndb.StringProperty()
    time = ndb.IntegerProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_record(cls, device_id, action, time):
        if not device_id or not action or not time:
            return False
        else:            
            record = TomatoRecord(device_id=device_id,
                action=action,
                time=int(time)
                )
            record.put()
            return True

    @classmethod
    def query_record(cls, device_id, page, page_size, **args):
        if not page:
            page = 1

        if not page_size:
            page_size = 100

        page_offset = page_size*(page-1)
        if not device_id:
            logging.info('no device_id')
        else:
            qry = cls.query()
            qry = qry.filter(TomatoRecord.device_id == device_id)

            start_time = None
            end_time = None
            if args.has_key('start_time'):
                start_time = args['start_time']
                logging.info(start_time)

            if args.has_key('end_time'):
                end_time = args['end_time']
                logging.info(end_time)

            #Account.query(Account.userid >= 40, Account.userid < 50)

            if start_time:
                logging.info('start_time')
                qry = qry.filter(TomatoRecord.time >= int(start_time))
            if end_time:
                logging.info('end_time')
                qry = qry.filter(TomatoRecord.time < int(end_time))

            qry = qry.order(-cls.time)
            return qry.fetch(page_size, offset=page_offset)

News_item_properties = {'category': '', 'title': '', 'subtitle': '', 'location': '', 'description': u'', 'news_time': None, 'media_name': '', 'thumb_url': ''}

class News(ndb.Model):
    category = ndb.StringProperty()
    title = ndb.StringProperty()
    subtitle = ndb.StringProperty()
    location = ndb.StringProperty()
    description = ndb.TextProperty()
    news_time = ndb.DateTimeProperty()
    media_name = ndb.StringProperty()
    thumb_url = ndb.StringProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_by_cate(cls, category, amount):
        if not category or not amount:
            return None
        else:
            try:
                amount = int(amount)
            except:
                amount = 10

            try:
                category = str(category)
            except:
                category = 'news'
            return cls.query(category=category).order(-cls.news_time).fetch(amount)

    @classmethod
    def update_item(cls, **args):
        item_data = News_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                item.category = item_data['category']
                item.title = item_data['title']
                item.subtitle = item_data['subtitle']
                item.location = item_data['location']
                item.description = item_data['description']
                item.news_time = item_data['news_time']
                item.media_name=item_data['media_name']
                item.thumb_url=item_data['thumb_url']
                item.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = News_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        news = News(category=item_data['category'],
              title=item_data['title'],
              subtitle=item_data['subtitle'],
              location=item_data['location'],
              description=item_data['description'],
              news_time = item_data['news_time'],
              media_name=item_data['media_name'],
              thumb_url=item_data['thumb_url'])

        news.put()

Post_item_properties = {'category': '', 'title': '', 'content': u'', 'image': ''}

class Post(ndb.Model):
    category = ndb.StringProperty()
    title = ndb.StringProperty()
    image = ndb.StringProperty()
    content = ndb.TextProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def update_item(cls, **args):
        item_data = Post_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                item.category = item_data['category']
                item.title = item_data['title']
                item.content = item_data['content']
                item.image = item_data['image']
                item.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = Post_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        post = Post(category=item_data['category'],
              title=item_data['title'],
              content=item_data['content'],
              image = item_data['image'])

        post.put()

class Character(ndb.Model):
    name = ndb.StringProperty()
    birthday = ndb.DateTimeProperty()
    pet_phrase = ndb.StringProperty() # 口頭禪
    personality = ndb.StringProperty()
    super_power = ndb.StringProperty()
    occupation = ndb.StringProperty()
    like = ndb.StringProperty()
    hate = ndb.StringProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_item(cls, **args):
        item_data = {'name': '', 'pet_phrase': '', 'personality': '', 'super_power': '', 'occupation': '', 'birthday': None, 'like': '', 'hate': ''}

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        character = Character(name=item_data['name'],
              pet_phrase=item_data['pet_phrase'],
              personality=item_data['personality'],
              super_power=item_data['super_power'],
              occupation=item_data['occupation'],
              birthday = item_data['birthday'],
              like=item_data['like'],
              hate=item_data['hate'])

        character.put()

EGoodie_item_properties = {'name': '', 'file_type': '', 'catalog_name': '', 'category': '', 'file_url': '', 'width': '', 'height': ''}
class EGoodie(ndb.Model):
    name = ndb.StringProperty()
    # video or image
    file_type = ndb.StringProperty()
    # SD 遊樂園、下載(手機桌布、電腦桌布、FB封面)
    category = ndb.StringProperty()
    # if this egoodie contains in one catalog, store it
    catalog_name = ndb.StringProperty()
    file_url = ndb.StringProperty()
    width = ndb.StringProperty()
    height = ndb.StringProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def update_item(cls, **args):
        item_data = EGoodie_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                # only when update pc_desktop or mobile_desktop(image file type) should consider this case(update catalog contain item)
                old_data = {'name': item.name, 'width': item.width, 'height': item.height}
                new_data = {'name': item_data['name'], 'file_type': item_data['file_type'], 'catalog_name': item_data['catalog_name'], 'category': item_data['category'], 'file_url': item_data['file_url'], 'width': item_data['width'], 'height': item_data['height'], 'access_time': item.access_time}
                DownloadItemCatalog.update_contain_item(item.catalog_name, item.category, old_data, new_data)

                item.name = item_data['name']
                item.file_type = item_data['file_type']
                item.catalog_name = item_data['catalog_name']
                item.category = item_data['category']
                item.file_url = item_data['file_url']
                item.width = item_data['width']
                item.height=item_data['height']
                item.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = EGoodie_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        egoodie = EGoodie.query(ndb.AND(EGoodie.name == item_data['name'], EGoodie.file_type == item_data['file_type'], EGoodie.category == item_data['category'], EGoodie.catalog_name == item_data['catalog_name'], EGoodie.width == item_data['width'], EGoodie.height == item_data['height'])).fetch(1)

        if len(egoodie) > 0:
            # the same item already exist
            logging.info('上傳物件重複')
            pass
        else:
            egoodie = EGoodie(name=item_data['name'],
                  file_type=item_data['file_type'],
                  category=item_data['category'],
                  file_url=item_data['file_url'],
                  width=item_data['width'],
                  height=item_data['height'],
                  catalog_name=item_data['catalog_name'])

            egoodie.put()

            catalog = DownloadItemCatalog.query(ndb.AND(DownloadItemCatalog.name == item_data['catalog_name'], DownloadItemCatalog.category == item_data['category'])).fetch(1)

            if len(catalog) > 0:
                catalog = catalog[0]
                # append this item into corresponding catalog
                catalog.download_items.append(egoodie)
                catalog.put()


DownloadItemCatalog_item_properties = {'name': '', 'category': '', 'cover_image': ''}
# 收納下載圖檔的目錄
class DownloadItemCatalog(ndb.Model):
    name = ndb.StringProperty()
    # 手機桌布 or 電腦桌布(mobile_desktop or pc_desktop)
    category = ndb.StringProperty()
    cover_image = ndb.StringProperty()
    # append after this catalog created
    download_items = ndb.StructuredProperty(EGoodie, repeated=True)
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    # catalog_name to identify which catalog, width and height to identify which egoodie should be removed
    @classmethod
    def delete_contain_item(cls, catalog_name, category, item_name, width, height):
        if not catalog_name or not category or not item_name or not width or not height:
            return False
        else:
            '''
            logging.info('------------------------')
            logging.info(catalog_name)
            logging.info(category)

            logging.info(item_name)
            logging.info(width)
            logging.info(height)
            '''

            catalog = cls.query(ndb.AND(cls.name == catalog_name, cls.category == category)).fetch(1)

            if len(catalog) > 0:
                catalog = catalog[0]
                item_index = None

                forloop_index = 0
                # linear search(list contains less then 10 items)
                for item in catalog.download_items:
                    '''
                    logging.info(item.name)
                    logging.info(item.width)
                    logging.info(item.height)
                    '''
                    if item.name == item_name and item.width == str(width) and item.height == str(height):
                        item_index = forloop_index
                        break
                    forloop_index = forloop_index + 1

                logging.info(item_index)

                if item_index != None:
                    catalog.download_items.pop(item_index)
                    catalog.put()
                return True
            else:
                return False

    @classmethod
    def update_contain_item(cls, catalog_name, category, old_data, new_data):
        if not catalog_name or not category:
            return False
        else:
            catalog = cls.query(ndb.AND(cls.name == catalog_name, cls.category == category)).fetch(1)

            if len(catalog) > 0:
                catalog = catalog[0]
                item_index = None

                forloop_index = 0
                # linear search(list contains less then 10 items)
                for item in catalog.download_items:
                    # search by name or width x height
                    if item.name == old_data['name'] or ( item.width == str(old_data['width']) and item.height == str(old_data['height']) ):
                        item_index = forloop_index
                    forloop_index = forloop_index + 1
                if item_index:
                    update_item = catalog.download_items[item_index]
                    update_item.name = new_data['name']
                    update_item.file_type = new_data['file_type']
                    update_item.catalog_name = new_data['catalog_name']
                    update_item.category = new_data['category']
                    update_item.file_url = new_data['file_url']
                    update_item.width = new_data['width']
                    update_item.height = new_data['height']
                    update_item.access_time = new_data['access_time']
                    catalog.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = DownloadItemCatalog_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        catalog = DownloadItemCatalog(name=item_data['name'],
              category=item_data['category'],
              cover_image=item_data['cover_image'])

        catalog.put()

    @classmethod
    def update_item(cls, **args):
        item_data = DownloadItemCatalog_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                item.category = item_data['category']
                item.name = item_data['name']
                item.cover_image = item_data['cover_image']
                item.put()
                return True
            else:
                return False


Product_item_properties = {'type': '', 'name': '', 'category': '', 'description': '', 'image_urls': '', 'where_to_buy': ''}
class Product(ndb.Model):
    type = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    category = ndb.StringProperty()
    image_urls = ndb.StringProperty(repeated=True)
    where_to_buy = ndb.StringProperty()
    show_priority = ndb.IntegerProperty(default=1)
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def update_item(cls, **args):
        item_data = Product_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                item.type = item_data['type']
                item.name = item_data['name']
                item.description = item_data['description']
                item.category = item_data['category']
                item.image_urls = item_data['image_urls']
                item.where_to_buy = item_data['where_to_buy']
                item.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = Product_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        product = Product(type=item_data['type'],
              name=item_data['name'],
              category=item_data['category'],
              description=item_data['description'],
              image_urls=item_data['image_urls'],
              where_to_buy = item_data['where_to_buy'])

        product.put()

Cooperation_item_properties = {'name': '', 'subtitle': '', 'location': '', 'partner': '', 'image_urls': '', 'description': '', 'image_url': '', 'event_time': None}
class Cooperation(ndb.Model):
    name = ndb.StringProperty()
    subtitle = ndb.StringProperty()
    partner = ndb.StringProperty()
    description = ndb.StringProperty()
    location = ndb.StringProperty()
    image_urls = ndb.StringProperty(repeated=True)
    event_time = ndb.DateTimeProperty()
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def update_item(cls, **args):
        item_data = Cooperation_item_properties

        if not args.has_key('key_id'):
            return False
        else:
            key_id = int(args['key_id'])

            for index in item_data:
                if args.has_key(index):
                    item_data[index] = args[index]

            item = cls.get_by_id(key_id)
            if item:
                item.name = item_data['name']
                item.subtitle = item_data['subtitle']
                item.partner = item_data['partner']
                item.description = item_data['description']
                item.location = item_data['location']
                item.image_urls = item_data['image_urls']
                item.event_time = item_data['event_time']
                item.put()
                return True
            else:
                return False

    @classmethod
    def add_item(cls, **args):
        item_data = Cooperation_item_properties

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        cooperation = Cooperation(name=item_data['name'],
              subtitle=item_data['subtitle'],
              partner=item_data['partner'],
              location=item_data['location'],
              description=item_data['description'],
              image_urls=item_data['image_urls'],
              event_time = item_data['event_time'])

        cooperation.put()

class Message(ndb.Model):
    # 訊息序號
    sn = ndb.StringProperty()
    name = ndb.StringProperty()
    tel = ndb.StringProperty()
    email = ndb.StringProperty()
    company = ndb.StringProperty()
    company_desc = ndb.StringProperty()
    title = ndb.StringProperty()
    proposal = ndb.TextProperty()
    # 是否已回覆
    reply = ndb.BooleanProperty(default=False)
    access_time = ndb.DateTimeProperty(auto_now=True)
    build_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_current_sn(cls):
        message = Message.query().order(-Message.build_time).fetch(1)
        if len(message) > 0:
            message = message[0]
            return message.sn
        else:
            return '0'

    @classmethod
    def add_item(cls, **args):

        current_sn = int(cls.get_current_sn())

        # 序號範例：000000000002
        new_sn = '%012d' % (current_sn + 1)

        item_data = {'name': '', 'tel': '', 'email': '', 'company': '', 'company_desc': '', 'title': '', 'proposal': ''}

        for index in item_data:
            if args.has_key(index):
                item_data[index] = args[index]

        message = Message(sn=new_sn,
              name=item_data['name'],
              tel=item_data['tel'],
              email=item_data['email'],
              company=item_data['company'],
              company_desc=item_data['company_desc'],
              title=item_data['title'],
              proposal = item_data['proposal'])

        message.put()