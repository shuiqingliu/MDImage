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
def sendImage(ak,sk,bucket,filename,url):
    auth = Auth(ak, sk)
    bucketManager = BucketManager(auth)
    print(url + ':' + bucket +  ':' + filename)
    ret, info = bucketManager.fetch(url, bucket, filename)
    print(info)
    if ret['key'] == filename:
        return  True
    else:
        return False

def sendImageFromLocal(ak,sk,bucket,filename):
    auth = Auth(ak, sk)
    # 生成上传 Token，可以指定过期时间等
    token = auth.upload_token(bucket, filename, 3600)
    # 要上传文件的本地路径
    localfile = './image/{}'.format(filename)
    ret, info = put_file(token, filename, localfile)
    print(info)
    if ret['key'] == filename:
        return True
    else:
        return False

def main():
    list = getBucketList('34lHs_MrDWgH8ldjkpjHRfzXn589tr57PUf6NLpO','-GPhLVzIMcyrZVuD3zrSDKAtv6AAI_5l4dZsKwg9') #Fake token
    print(len(list))
    for i in list:
        print(i)

if __name__ == '__main__':
    main()