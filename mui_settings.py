from pymongo import MongoClient

myapp_client = MongoClient("172.16.53.130", 27017)
db = myapp_client["myApp"]