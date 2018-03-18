from blob_utils import core
from google.appengine.api import images

def store_image_to_blobstore(imgurl):
    if not imgurl:
        return False
    
    # retry 3 times max
    for i in range(0,3):
        try:
            # img is google.appengine.ext.blobstore.blobstore.BlobInfo object
            img, blob_key, width, height = core.url_upload(imgurl, imgurl)
            logging.info('core.url_upload success!')
            # if fetch success, jump out forloop(to prevent from urlfetch fail)
            break
        except:
            logging.info('core.url_upload fail!')
            img, blob_key, width, height = core.url_upload(imgurl, imgurl)

    # get picasa url
    result = images.get_serving_url(img)

    logging.info('img width: %s, img height: %s' % (width, height))

    # convert width and height from float(possible) to int
    width = int(width)
    height = int(height)

    if width > height:
        result = result + '=s' + str(width)
    else:
        result = result + '=s' + str(height)

    logging.info("New imgurl: %s" % result)

    return result, blob_key, width, height