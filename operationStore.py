# -*- coding: UTF-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_decode, BucketManager
from qiniuBucket import BucketTool


#config key
access_key = '34lHs_MrDWgH8ldjkpjHRfzXn589tr57PUf6NLpO'
secret_key = '-GPhLVzIMcyrZVuD3zrSDKAtv6AAI_5l4dZsKwg9'

#Return Auth account object
authResult = Auth(access_key,secret_key)

#set store sapce
bucket_name = 'qingliu'

#get buckets
buketBuckTool = BucketTool(authResult)
bucketList = buketBuckTool.getBucketList()

#operation buckets
for buket in bucketList :
    result = buketBuckTool.list(buket)[0]
    for fileName in result['items']:
        if fileName['key'] != '':
            print(fileName['key'])
