# -*- coding: UTF-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_decode, BucketManager
from BucketTool import BucketTool
import DBHelper

#get buckets
def getBucketList(ak,sk):
    authResult = Auth(ak, sk) #auth qiniu account
    bucketTool = BucketTool(authResult)
    return bucketTool.getBucketList()

#store image
def sendImage(username,image):
    pass
    # 生成上传 Token

    # token = q.upload_token(bucket_name, key, 3600)
    # # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)

def main():
    list = getBucketList('34lHs_MrDWgH8ldjkpjHRfzXn589tr57PUf6NLpO','-GPhLVzIMcyrZVuD3zrSDKAtv6AAI_5l4dZsKwg9')
    print(len(list))
    for i in list:
        print(i)

if __name__ == '__main__':
    main()