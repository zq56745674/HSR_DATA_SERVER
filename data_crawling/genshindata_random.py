import requests
from fake_useragent import UserAgent
import time
import random
import pymysql

# 全局变量
not_found_count = 0

def print_dict_differences(dict1, dict2):
    result = []
    before_info = {}
    after_info = {}
    for key in dict1:
        v1 = dict1[key]
        v2 = dict2[key]
        if key == 'platform':
            v2 = str(dict2[key])
        if v1 != v2:
            before_info[key] = v1
            after_info[key] = v2
    if before_info:
        result.append(before_info)
        result.append(after_info)
    else:
        print('两个字典相同')
    return result

def get_database_connection():
    dbhost = 'rm-uf6n58p87aw72940u3o.mysql.rds.aliyuncs.com'
    dbuser = 'zzm'
    dbpass = 'Zq56745674'
    dbname = 'my_data'
    try:
        db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        print("数据库连接成功")
        return db
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
        return None

def log_request_failure(cursor, uid, status_code, error_desc=None):
    try:
        if error_desc:
            return
            # fail_sql = "INSERT INTO sr_user_info_fail_record (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) VALUES (%s, %s, %s, now())"
            # cursor.execute(fail_sql, (uid, status_code, error_desc))
        else:
            insert_sql = "INSERT INTO gi_user_info (UID, CREATE_TIME, remark) VALUES (%s, now(), %s)"
            cursor.execute(insert_sql, (uid, status_code))
    except pymysql.MySQLError as e:
        print(f"数据库操作失败：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

def fetch_data_from_api(url, headers, uid, db, cursor):
    global not_found_count
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            not_found_count += 1
            print(f"请求失败，状态码：{response.status_code}，404计数：{not_found_count}")
            log_request_failure(cursor, uid, response.status_code)
            db.commit()
            return None
        elif response.status_code == 429:
            print(f"请求失败，状态码：{response.status_code}")
            time.sleep(10)
            return None
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求异常：{e}")
        # log_request_failure(cursor, uid, 'RequestException', str(e))
        # db.commit()
        return None

def process_user_data(uid, data):
    uid = uid
    nickname = None
    level = None
    worldLevel = None
    nameCardId = None
    finishAchievementNum = None
    towerFloorIndex = None
    theaterActIndex = None
    theaterModeIndex = None
    fetterCount = None
    towerStarIndex = None
    if data and data[1]:
        if data[1].get("nickname") != None:
            nickname = data[data[1].get("nickname")]
        if data[1].get("level") != None:
            level = data[data[1].get("level")]
        if data[1].get("worldLevel") != None:
            worldLevel = data[data[1].get("worldLevel")]
        if data[1].get("nameCardId") != None:
            nameCardId = data[data[1].get("nameCardId")]
        if data[1].get("finishAchievementNum") != None:
            finishAchievementNum = data[data[1].get("finishAchievementNum")]
        if data[1].get("towerFloorIndex") != None:
            towerFloorIndex = data[data[1].get("towerFloorIndex")]
        if data[1].get("theaterActIndex") != None:
            theaterActIndex = data[data[1].get("theaterActIndex")]
        if data[1].get("theaterModeIndex") != None:
            theaterModeIndex = data[data[1].get("theaterModeIndex")]
        if data[1].get("fetterCount") != None:
            fetterCount = data[data[1].get("fetterCount")]
        if data[1].get("towerStarIndex") != None:
            towerStarIndex = data[data[1].get("towerStarIndex")]
    print(f"uid: {uid} nickname: {nickname} level: {level} worldLevel: {worldLevel} nameCardId: {nameCardId} finishAchievementNum: {finishAchievementNum} towerFloorIndex: {towerFloorIndex} theaterActIndex: {theaterActIndex} theaterModeIndex: {theaterModeIndex} fetterCount: {fetterCount} towerStarIndex: {towerStarIndex}")
    return uid, nickname, level, worldLevel, nameCardId, finishAchievementNum, towerFloorIndex, theaterActIndex, theaterModeIndex, fetterCount, towerStarIndex

def main():
    db = get_database_connection()
    if not db:
        return

    cursor = db.cursor()

    loop_limit = 70
    rest_time = 5
    counter = 0
    i = 0

    while i < 3000:
        # 国服
        # randomNum = random.randint(1, 212170000) + 100000009
        # B服 532532012
        # randomNum = random.randint(1, 4001000) + 500000001
        # 美服 678492367
        # randomNum = random.randint(1, 78400000) + 600000006
        # 欧服 773749735
        randomNum = random.randint(1, 73700000) + 700000001
        # 亚服 898200000 1808038141
        # randomNum = random.randint(1, 98200000) + 800000002
        # 港澳台 908750955
        # randomNum = random.randint(1, 1098000) + 900000001
        # if counter >= loop_limit:
        #     print(f"已达到循环次数限制，休息 {rest_time} 秒....................................")
        #     time.sleep(rest_time)
        #     counter = 0

        counter += 1
        i += 1
        uid = str(randomNum)

        url = f"https://enka.network/u/{uid}/__data.json?x-sveltekit-invalidated=01"
        print(f"i {i} url: {url}")
        user_agents = UserAgent().chrome
        headers = {"User-Agent": user_agents}
        data = fetch_data_from_api(url, headers, uid, db, cursor)
        if not data:
            continue
        
        # print(data)
        data = data.get("nodes")[1].get("data")

        user_data = process_user_data(randomNum, data)
        uid, nickname, level, worldLevel, nameCardId, finishAchievementNum, towerFloorIndex, theaterActIndex, theaterModeIndex, fetterCount, towerStarIndex = user_data
        # # print(f"uid: {uid} activity_user: {activity_user}")
        # if activity_user:
        #     print(f"uid: {uid} platform: {platform} signature: {signature} nickname: {nickname} level: {level} friendCount: {friendCount} maxRogueChallengeScore: {maxRogueChallengeScore} achievementCount: {achievementCount} equipmentCount: {equipmentCount} avatarCount: {avatarCount} headIcon: {headIcon} relicCount: {relicCount} bookCount: {bookCount} musicCount: {musicCount} remark: {remark}")
        # qry_sql = "select `UID`, `signature`, `platform`, `nickname`, `level`, `friend_count`, `max_rogue_challenge_score`, `achievement_count`, `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, `book_count`, `music_count` from sr_user_info where uid = %s"
        # cursor.execute(qry_sql, (uid,))
        # exist = cursor.fetchone()
        # if exist:
        #     dict1 = {'platform': exist[2], 'signature': exist[1], 'nickname': exist[3], 'level': exist[4],
        #                 'friendCount': exist[5], 'maxRogueChallengeScore': exist[6], 'achievementCount': exist[7],
        #                 'equipmentCount': exist[8], 'avatarCount': exist[9], 'headIcon': exist[10], 'relicCount': exist[11],
        #                 'bookCount': exist[12], 'musicCount': exist[13]}
        #     dict2 = {'platform': platform, 'signature': signature, 'nickname': nickname, 'level': level,
        #                 'friendCount': friendCount, 'maxRogueChallengeScore': maxRogueChallengeScore, 'achievementCount': achievementCount,
        #                 'equipmentCount': equipmentCount, 'avatarCount': avatarCount, 'headIcon': headIcon, 'relicCount': relicCount, 
        #                 'bookCount': bookCount, 'musicCount': musicCount}
        #     differences = print_dict_differences(dict1, dict2)
        #     if differences:
        #         update_sql = "UPDATE sr_user_info SET UID=%s, signature=%s, platform=%s, nickname=%s, `level`=%s, friend_count=%s, max_rogue_challenge_score=%s, achievement_count=%s, equipment_count=%s, avatar_count=%s, head_icon=%s, remark=%s, relic_count=%s, book_count=%s, music_count=%s, LAST_UPDATE_TIME=now() WHERE UID=%s"
        #         cursor.execute(update_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, uid))
        #         insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
        #         cursor.execute(insert_record_sql, (uid, json.dumps(differences[0]), json.dumps(differences[1])))
        # else:

        insert_sql = "INSERT INTO `gi_user_info` (`UID`, `nickname`, `level`, `worldLevel`, `nameCardId`, `finishAchievementNum`, `towerFloorIndex`, `theaterActIndex`, `theaterModeIndex`, `fetterCount`, `towerStarIndex`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, (uid, nickname, level, worldLevel, nameCardId, finishAchievementNum, towerFloorIndex, theaterActIndex, theaterModeIndex, fetterCount, towerStarIndex))
        db.commit()

        # 随机延迟
        random_delay = random.uniform(1.5, 1.8)
        print(f"随机延迟 {random_delay} 秒...")
        time.sleep(random_delay)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()