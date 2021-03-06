#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
from ..common import open_gps_database
from ..common import fixup_encode
from ..common import logger

def open_database():
    return open_gps_database()

area_alias = [
    ["武当","武当山"],
    ["牙山","牙山湾"],
    ["少林寺","少林寺寺内"],
    ["少林","少林寺寺内"],
    ["白驼山","白驼"],
    ["小山村","华山村"],
    ["福州","闽南"],
    ["杭州提督府","临安提督府"],
    ["杭州","临安府"],
    ["大理城中","大理城"],
    ["大理","大理城"],
    ["西湖梅庄","梅庄"],
    ["西湖","临安府西湖"],
    ["桃源","桃源县"],
    ["全真","全真教"],
    ["苏州","苏州城"],
    ["扬州","扬州城"],
    ["晋阳","晋阳城"],
    ["镇江","镇江府"],
    ["北京","北京城内城"],
    ["姑苏慕容","慕容"],
    ["建康府南城","建康府南"],
    ["建康府北城","建康府北"],
    ["建康府","建康府北"],
    ["长江南岸","长江南岸"],
    ["长江北岸","长江北岸"],
    ["长江","长江南岸"],
    ["黄河南岸","黄河南岸"],
    ["黄河北岸","黄河北岸"],
    ["黄河","黄河南岸"],
    ["峨嵋后山","峨嵋后山"],
    ["峨嵋","峨嵋派"],
    ["洛阳","洛阳城"],
    ["长安","长安城"],
    ["镇江","镇江府"],    
]

room_alias = {
    "襄阳官道":498,
    "古墓墓道":1036,
    "丐帮暗道":1484,
    "扬州城暗道":1484,
    "杀手帮消魂屋":400,
    "华山寝室":1107,
    "无量山书房":3478,
    "华山村小棚子":1067,
    "慕容小路":2665,
    "中原大驿道":718,
    "桃花岛小木屋":2618,
    "曲阜大驿道":661,
    "峨嵋派洞穴":1731,
    "泉州杂货铺":2120,
    "灵州车马店二楼":1366,
    "建康府北长江渡口":2580,
    "归云庄马房":2350,
    "闽南密道":2157,
    "闽南密室":2157,
    "闽南密室房梁":2157,
    "成都川西土路":1528,
    "南昌山路":2061,
    "襄阳民宅":458,
    "苏州城客店二楼":2287,
    "昆明客店内室":1948,
    "全真教浴堂":1143,
    "白驼武器库":3002,
    "张家口天字号房":2887,
    "张家口地字号房":2887,
    "江州客店内室":2064,
    "中原客店二楼":714,
    "南昌客店内室":2082,
    "镇江府客店内室":2424,
    "洛阳城大官道":817,
    "丝绸之路莫高窟":2778,
    "建康府南江南小道":3713,
    "大理城茶花院":1889,
    "南昌山路":2112,
    "岳阳车马行":2015,
    "建康府北车马行":2578,
    "北京城内城土路":2796,
}

def fixup_area(desc):
    for [k,v] in area_alias:
        if re.match("^%s"%(k),desc):
            if not re.match("^%s"%(v),desc) or k.startswith(v):
                desc = "%s%s"%(v,desc[len(k):])
                break
    return desc

def fixup_room(room):
    if re.match(".*泥人.*",room):
        room = "泥人铺"
    elif re.match(".*储物柜.*",room):
        room = "储物柜"

    return room

def get_zone(conn, room):
    sql = "select zone from mud_room where roomno = %d" % (room)
    row = conn.execute(sql).fetchone()
    if row:
        return row[0]
    else:
        return "nil"
