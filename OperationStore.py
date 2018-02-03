# -*- coding: UTF-8 -*-

from qiniu import Auth, put_file, etag, urlsafe_base64_decode, BucketManager
from BucketTool import BucketTool

#get buckets
def getBucketList(ak,sk):
    authResult = Auth(ak, sk) #auth qiniu account
    bucketTool = BucketTool(authResult)
    return bucketTool.getBucketList()

#operation buckets
def bucketOper(bucket):
    pass
    # for buket in bucketList :
    #     bucketResult = [] #bucket temp
    #     result = buketBuckTool.list(buket)[0]
    #     #get re
    #     for fileName in result['items']:
    #         if fileName['key'] != '':
    #             bucketResult.append(fileName['key'])
    #     return

def main():
    list = getBucketList('34lHs_MrDWgH8ldjkpjHRfzXn589tr57PUf6NLpO','-GPhLVzIMcyrZVuD3zrSDKAtv6AAI_5l4dZsKwg9')
    print(len(list))
    for i in list:
        print(i)

if __name__ == '__main__':
    main()