import requests
import json
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
            fail_sql = "INSERT INTO sr_user_info_fail_record (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) VALUES (%s, %s, %s, now())"
            cursor.execute(fail_sql, (uid, status_code, error_desc))
        else:
            insert_sql = "INSERT INTO sr_user_info (UID, CREATE_TIME, remark) VALUES (%s, now(), %s)"
            cursor.execute(insert_sql, (uid, status_code))
    except pymysql.MySQLError as e:
        print(f"数据库操作失败：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

def fetch_data_from_api(url, headers, uid, db, cursor):
    global not_found_count
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            not_found_count += 1
            print(f"请求失败，状态码：{response.status_code}，404计数：{not_found_count}")
            # log_request_failure(cursor, uid, response.status_code)
            # db.commit()
            return None
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求异常：{e}")
        log_request_failure(cursor, uid, 'RequestException', str(e))
        db.commit()
        return None

def process_user_data(detail_info, record_info, assist_avatar_list, avatar_detail_list):
    uid = int(detail_info.get("uid"))
    platform = detail_info.get("platform")
    signature = detail_info.get("signature")
    nickname = detail_info.get("nickname")
    level = detail_info.get("level")
    friendCount = detail_info.get("friendCount")
    maxRogueChallengeScore = record_info.get("maxRogueChallengeScore")
    achievementCount = record_info.get("achievementCount")
    equipmentCount = record_info.get("equipmentCount")
    avatarCount = record_info.get("avatarCount")
    bookCount = record_info.get("bookCount")
    musicCount = record_info.get("musicCount")
    relicCount = record_info.get("relicCount") # 仪器数量
    headIcon = detail_info.get("headIcon")
    activity_user = False
    remark = ""
    # 1221 云璃 1224 巡猎三月 1218 椒丘
    # avatarIdList = [8005, 8006, 1315, 1314, 1312, 1310, 1309, 1308, 1307, 1306, 1305, 1304, 1303, 1302, 1224, 1221, 1218]
    avatarIdList = [1221, 1224]
    if assist_avatar_list is not None:
        for avatar in assist_avatar_list:
            if avatar.get('avatarId') is not None and avatar.get('avatarId') in avatarIdList:
                # print(f"assistAvatarList avatarId: {avatar.get('avatarId')}")
                remark += str(avatar.get('avatarId')) + "|"
                remark += str(avatar.get('rank') or 0) + "|"
                remark += str(avatar.get('equipment').get('tid') if avatar.get('equipment') else "") + "#"
                activity_user = True

    if avatar_detail_list is not None:
        for avatar in avatar_detail_list:
            if avatar.get('avatarId') is not None and str(avatar.get('avatarId')) not in remark and avatar.get('avatarId') in avatarIdList:
                # print(f"avatarDetailList avatarId: {avatar.get('avatarId')}")
                remark += str(avatar.get('avatarId')) + "|"
                remark += str(avatar.get('rank') or 0) + "|"
                remark += str(avatar.get('equipment').get('tid') if avatar.get('equipment') else "") + "#"
                activity_user = True
    # 2.4上半最大角色数52
    if avatarCount >= 52:
        activity_user = True
    if bookCount is not None and bookCount > 298:
        activity_user = True
    if musicCount is not None and musicCount >= 112:
        activity_user = True
    # if platform is not None and platform != '' and relicCount is not None:
    #     activity_user = True

    return uid, platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, activity_user, remark, relicCount, bookCount, musicCount

def main():
    db = get_database_connection()
    if not db:
        return

    cursor = db.cursor()
    endpoint = "https://api.mihomo.me/sr_info/"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    ]
    selected_user_agent = user_agents[0]
    loop_limit = 70
    rest_time = 5
    counter = 0
    i = 0

    while i < 2000:
        # 国服
        randomNum = random.randint(1, 57150000) + 100000009
        # B服
        # randomNum = random.randint(1, 4001000) + 500000001
        # 美服
        # randomNum = random.randint(1, 20200000) + 600000006
        # 欧服 19790000
        # randomNum = random.randint(2000001, 3000000) + 700000001
        # 亚服 36060000
        # randomNum = random.randint(1000001, 2000000) + 800000002
        # 港澳台
        # randomNum = random.randint(1, 1098000) + 900000001
        if counter >= loop_limit:
            print(f"已达到循环次数限制，休息 {rest_time} 秒....................................")
            time.sleep(rest_time)
            counter = 0

        counter += 1
        i += 1
        uid = str(randomNum)
        url = endpoint + uid
        print(f"i {i} url: {url}")

        headers = {"User-Agent": selected_user_agent}
        data = fetch_data_from_api(url, headers, uid, db, cursor)
        if not data:
            continue

        detail_info = data.get("detailInfo")
        record_info = detail_info.get("recordInfo")
        assist_avatar_list = detail_info.get("assistAvatarList")
        avatar_detail_list = detail_info.get("avatarDetailList")

        user_data = process_user_data(detail_info, record_info, assist_avatar_list, avatar_detail_list)
        uid, platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, activity_user, remark, relicCount, bookCount, musicCount = user_data
        # print(f"uid: {uid} activity_user: {activity_user}")
        if activity_user:
            print(f"uid: {uid} platform: {platform} signature: {signature} nickname: {nickname} level: {level} friendCount: {friendCount} maxRogueChallengeScore: {maxRogueChallengeScore} achievementCount: {achievementCount} equipmentCount: {equipmentCount} avatarCount: {avatarCount} headIcon: {headIcon} relicCount: {relicCount} bookCount: {bookCount} musicCount: {musicCount} remark: {remark}")
            qry_sql = "select `UID`, `signature`, `platform`, `nickname`, `level`, `friend_count`, `max_rogue_challenge_score`, `achievement_count`, `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, `book_count`, `music_count` from sr_user_info where uid = %s"
            cursor.execute(qry_sql, (uid,))
            exist = cursor.fetchone()
            if exist:
                dict1 = {'platform': exist[2], 'signature': exist[1], 'nickname': exist[3], 'level': exist[4],
                            'friendCount': exist[5], 'maxRogueChallengeScore': exist[6], 'achievementCount': exist[7],
                            'equipmentCount': exist[8], 'avatarCount': exist[9], 'headIcon': exist[10], 'relicCount': exist[11],
                            'bookCount': exist[12], 'musicCount': exist[13]}
                dict2 = {'platform': platform, 'signature': signature, 'nickname': nickname, 'level': level,
                            'friendCount': friendCount, 'maxRogueChallengeScore': maxRogueChallengeScore, 'achievementCount': achievementCount,
                            'equipmentCount': equipmentCount, 'avatarCount': avatarCount, 'headIcon': headIcon, 'relicCount': relicCount, 
                            'bookCount': bookCount, 'musicCount': musicCount}
                differences = print_dict_differences(dict1, dict2)
                if differences:
                    update_sql = "UPDATE sr_user_info SET UID=%s, signature=%s, platform=%s, nickname=%s, `level`=%s, friend_count=%s, max_rogue_challenge_score=%s, achievement_count=%s, equipment_count=%s, avatar_count=%s, head_icon=%s, remark=%s, relic_count=%s, book_count=%s, music_count=%s, LAST_UPDATE_TIME=now() WHERE UID=%s"
                    cursor.execute(update_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, uid))
                    insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
                    cursor.execute(insert_record_sql, (uid, json.dumps(differences[0]), json.dumps(differences[1])))
            else:
                insert_sql = "INSERT INTO sr_user_info (UID, signature, platform, nickname, `level`, friend_count, max_rogue_challenge_score, achievement_count, equipment_count, avatar_count, head_icon, CREATE_TIME, remark, relic_count, book_count, music_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s)"
                cursor.execute(insert_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount))
            db.commit()

        # 随机延迟0.7到0.8秒
        random_delay = random.uniform(1.1, 1.2)
        # print(f"随机延迟 {random_delay} 秒...")
        time.sleep(random_delay)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()