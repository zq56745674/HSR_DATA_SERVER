import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 打印两个字典的不同
def print_dict_differences(dict1, dict2):
    result = None
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
        result = []
        result.append(before_info)
        result.append(after_info)
    else:
        logging.info('两个字典相同')
    return result

# 生成备注
def generate_remark(assist_avatar_list, avatar_detail_list):
    remark = ""
    # 2.X版本新增的角色
    # 1220 飞霄 1222 灵砂 1223 貊泽
    avatarIdList = [8005, 8006, 1315, 1314, 1312, 1310, 1309, 1308, 1307, 1306, 1305, 1304, 1303, 1302, 1301, 1224, 1221, 1218, 1220, 1222, 1223]
    if assist_avatar_list:
        for avatar in assist_avatar_list:
            if avatar.get('avatarId') and avatar.get('avatarId') in avatarIdList:
                remark += f"{avatar.get('avatarId')}|{avatar.get('rank') or 0}|{avatar.get('equipment').get('tid') if avatar.get('equipment') else ''}#"
    if avatar_detail_list:
        for avatar in avatar_detail_list:
            if avatar.get('avatarId') and str(avatar.get('avatarId')) not in remark and avatar.get('avatarId') in avatarIdList:
                remark += f"{avatar.get('avatarId')}|{avatar.get('rank') or 0}|{avatar.get('equipment').get('tid') if avatar.get('equipment') else ''}#"
    return remark

def create_dict_from_db(exist):
    return {
        'platform': exist[2], 'signature': exist[1], 'nickname': exist[3], 'level': exist[4],
        'friendCount': exist[5], 'maxRogueChallengeScore': exist[6], 'achievementCount': exist[7],
        'equipmentCount': exist[8], 'avatarCount': exist[9], 'headIcon': exist[10], 'relicCount': exist[11],
        'bookCount': exist[12], 'musicCount': exist[13]
    }

def create_dict_from_response(platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount):
    return {
        'platform': platform, 'signature': signature, 'nickname': nickname, 'level': level,
        'friendCount': friendCount, 'maxRogueChallengeScore': maxRogueChallengeScore, 'achievementCount': achievementCount,
        'equipmentCount': equipmentCount, 'avatarCount': avatarCount, 'headIcon': headIcon, 'relicCount': relicCount, 
        'bookCount': bookCount, 'musicCount': musicCount
    }