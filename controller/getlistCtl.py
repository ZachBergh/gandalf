#coding: utf-8
from bson.objectid import ObjectId
from config import config
import common
import json
import response

def index(obj):
    result = []
    cursor = config.mongo.find("tasks")
    for i in cursor:
        data = common.transfer(i)
        result.append(data)
    response.Response(obj, 200, "success", result)

def getById(obj):
    taskId = obj.get_argument("id")
    result = []
    if taskId:
        cursor = config.mongo.find("tasks", {"_id": ObjectId(taskId)})
        for i in cursor:
            i["_id"] = str(i["_id"])
            i["create_time"] = int(i["create_time"])
            result.append(i)
    response.Response(obj, 200, "success", result)

def getLog(obj):
    status = obj.get_argument("status")
    page = int(obj.get_argument("page"))
    size = int(obj.get_argument("size"))
    limit = size

    if page > 1:
        skip = (page - 1) * size
    else:
        skip = 0
    result = []
    if status:
        cursor = config.mongo.find("log", {"status": status}, "start_time", "DESC", limit, skip)
        for i in cursor:
            i["_id"] = str(i["_id"])
            i["task_id"] = str(i["task_id"])
            i["start_time"] = int(i["start_time"])
            result.append(i)
    response.Response(obj, 200, "success", result)