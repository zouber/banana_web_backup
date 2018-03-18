# -*- coding: utf-8 -*-
from libs.handlers import *
from db.models import *
import logging
import urllib, base64
from google.appengine.api import urlfetch

NEWSLEOPARD_DOMAIN = 'https://www.newsleopard.com'

class FakeAPI(DirectHandler):
    def get(self):
        import json

        res = {"id":111,"event_id":7,"user_id":2349,"text":"text","like_num":0,"share_num":0,"photo":"/system/event_posts/photos/000/000/111/original/photo.jpeg?1395652177","created_at":"2014-03-24T09:09:39.000Z","updated_at":"2014-05-05T15:58:24.000Z"}

        callback = self.request.get("callback")
        if callback:
            self.response.write("%s(%s)" % (callback, json.dumps(res, indent=4, sort_keys=True, separators=(',', ': '))))
        else:
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(json.dumps(res, indent=4, sort_keys=True, separators=(',', ': ')))

class AddStatusAPI(DirectHandler):
    def get(self):
        import json

        device_id = self.request.get('device_id')
        key = self.request.get('key')
        time = self.request.get('time')

        status = False

        if not device_id:
            res = {'msg': 'DEVICE_ID_NOT_GIVEN'}
        elif not key:
            res = {'msg': 'KEY_NOT_GIVEN'}
        elif not time:
            res = {'msg': 'TIME_NOT_GIVEN'}
        elif key not in ['start', 'job_done', 'stop', 'happy']:
            res = {'msg': 'INVALID_KEY'}
        else:
            try:
                time = int(time)
                status = True
                TomatoRecord.add_record(device_id, key, time)
                res = {'msg': 'OK'}
            except:
                res = {'msg': 'INVALID_TIME'}

        self.JsonResponse(status, res)

class GetStatusAPI(DirectHandler):
    def get(self):
        import json

        para_error = False
        status = False

        device_id = self.request.get('device_id')
        page = self.request.get('page')
        page_size = self.request.get('page_size')
        start_time = self.request.get('start_time')
        end_time = self.request.get('end_time')

        logging.info(start_time)
        logging.info(type(start_time))

        if not page:
            page = 1
        if not page_size:
            page_size = 100

        try:
            page = int(page)
        except:
            para_error = True
            res = {'msg': 'INVALID_PAGE_NUMBER'}

        try:
            page_size = int(page_size)
        except:
            para_error = True
            res = {'msg': 'INVALID_PAGE_SIZE'}

        if not device_id:
            res = {'msg': 'DEVICE_ID_NOT_GIVEN'}
        elif para_error:
            pass
        else:
            if page < 1:
                res = {'msg': 'INVALID_PAGE_NUMBER'}
            elif page_size > 1000 or page_size < 1:
                res = {'msg': 'INVALID_PAGE_SIZE'}
            else:
                try:
                    start_time = int(start_time)
                except:
                    res = {'msg': 'INVALID_START_TIME'}
                    start_time = None

                try:
                    end_time = int(end_time)
                except:
                    res = {'msg': 'INVALID_START_TIME'}
                    end_time = None

                result = TomatoRecord.query_record(device_id, page, page_size, start_time=start_time, end_time=end_time)
                records = []
                for item in result:
                    records.append({'key': item.action, 'time': item.time})

                status = True
                res = {'msg': 'OK', 'records': records, 'device_id': device_id}

        self.JsonResponse(status, res)


class AddSubscribeMember(DirectHandler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        response = {}

        if not email:
            status = False
            response['msg'] = 'input not complete'
        else:
            if not name:
                name = u'香蕉人粉絲'

            AuthAccount = 'api'
            AuthKey = 'key-bwbn7zckdeag6o6npuruaqawkstmnlah'

            base64string = base64.encodestring('%s:%s' % (AuthAccount, AuthKey)).replace('\n', '')
            Authorization = "Basic %s" % base64string   

            RequestURL = NEWSLEOPARD_DOMAIN + '/services/lists/members'

            form_fields = {
              # 寄件人群組名稱
              "list_name": "SambarDeer Website",
              "member": email.encode("utf-8") + ',' + name.encode("utf-8") + ',None'
            }
            form_data = urllib.urlencode(form_fields)
            result = urlfetch.fetch(url=RequestURL,
                payload=form_data,
                method=urlfetch.POST,
                headers={'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': Authorization})

            # urlfetch document: https://cloud.google.com/appengine/docs/python/urlfetch/
            # response object document: https://cloud.google.com/appengine/docs/python/urlfetch/responseobjects
            # simple auth implement: http://stackoverflow.com/questions/635113/python-urllib2-basic-http-authentication-and-tr-im
            '''
            logging.info(result.content)
            logging.info(result.status_code)
            logging.info(result.headers)
            '''

            status = True
            response['data'] = {'email': email}

        self.JsonResponse(status, response)

class ChangeProductOrderAPI(DirectHandler):
    def post(self):
        response = {}
        response['msg'] = ''
        response['data'] = []

        status = False

        keys = self.request.get('keys')

        keys = keys.split(',')

        index = 1

        for key in keys:
            if key:
                item = Product.get_by_id(int(key))
                if item:
                    item.show_priority = index
                    item.put()
                    response['data'].append({str(index): key})
                    index = index + 1
                else:
                    response['msg'] = response['msg'] + 'there is entity not found: %s,' % key
            
            status = True

        self.JsonResponse(status, response)

class RemoveItemAPI(DirectHandler):
    def post(self):
        response = {}
        status = False
        key_id = self.request.get('key_id')
        class_name = self.request.get('class_name')

        response['data'] = {'key_id': key_id, 'class_name': class_name}

        if class_name == 'News':
            item = News.get_by_id(int(key_id))
        elif class_name == 'Post':
            item = Post.get_by_id(int(key_id))
        elif class_name == 'EGoodie':
            item = EGoodie.get_by_id(int(key_id))
        elif class_name == 'DownloadItemCatalog':
            item = DownloadItemCatalog.get_by_id(int(key_id))
        elif class_name == 'Product':
            item = Product.get_by_id(int(key_id))
        elif class_name == 'Cooperation':
            item = Cooperation.get_by_id(int(key_id))
        else:
            item = None
            response['msg'] = 'no such db class'

        if item:
            if class_name == 'EGoodie':
                # delete copy of this item in egoodie catalog
                DownloadItemCatalog.delete_contain_item(item.catalog_name, item.category, item.name, item.width, item.height)
            item.key.delete()
            status = True
            response['msg'] = 'success'
        else:
            response['msg'] = 'no such entity'

        self.JsonResponse(status, response)

class MarkMessageAsReplyAPI(DirectHandler):
    def post(self):
        response = {}
        message_sn = self.request.get('message_sn')
        reply = self.request.get('reply')

        logging.info(reply)

        if reply == 'true':
            reply = True
        elif reply == 'false':
            reply = False
        else:
            reply = True

        if not message_sn:
            status = False
            response['msg'] = 'input not complete'
        else:
            message = Message.query(Message.sn == message_sn).fetch(1)

            if len(message) > 0:
                message = message[0]
                message.reply = reply
                message.put()

                logging.info(message.key.id())
                logging.info(type(message.key.id()))

                status = True
                response['msg'] = 'success'
                response['data'] = {'message_sn': message_sn}
            else:
                status = False
                response['msg'] = 'no such message'
                response['data'] = {'message_sn': message_sn}

        self.JsonResponse(status, response)