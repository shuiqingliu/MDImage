# -*- coding: UTF-8 -*-

from qiniu import  BucketManager

class BucketTool():

    def __init__(self, auth):
        self.__auth = auth
        self.__bucketManager = BucketManager(self.__auth)

    def getBucketList(self):
        bucketList = self.__bucketManager.buckets()
        return bucketList[0]

    def list(self,bucket):
        return self.__bucketManager.list(bucket,limit=20)