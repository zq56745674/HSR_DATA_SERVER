import logging
import datetime
from typing import Dict, List, Optional, Tuple, Any

logger = logging.getLogger(__name__)

# 2.X版本新增的角色ID
NEW_AVATAR_IDS = [8005, 8006, 1315, 1314, 1312, 1310, 1309, 1308, 1307, 1306,
                  1305, 1304, 1303, 1302, 1301, 1224, 1221, 1218, 1220, 1222, 1223]

# 金标角色ID
GOLD_AVATAR_IDS = [1005, 1006, 1102, 1112, 1203, 1204, 1205, 1208, 1212, 1213,
                   1217, 1218, 1221, 1302, 1303, 1304, 1305, 1306, 1307, 1308,
                   1309, 1310, 1314, 1315, 1220, 1222]

# 普通角色ID
COMMON_AVATAR_IDS = [1003, 1004, 1101, 1104, 1107, 1209, 1211]


def print_dict_differences(dict1: Dict, dict2: Dict) -> Optional[List[Dict]]:
    """Compare two dictionaries and return differences.
    
    Args:
        dict1: First dictionary (from DB)
        dict2: Second dictionary (from API response)
        
    Returns:
        [before_info, after_info] if differences found, else None
    """
    before_info: Dict[str, Any] = {}
    after_info: Dict[str, Any] = {}
    
    for key in dict1:
        v1 = dict1[key]
        v2 = dict2[key]
        if key == 'platform' and v2 is not None:
            v2 = str(v2)
        if str(v1) != str(v2):
            before_info[key] = v1
            after_info[key] = v2
    
    if before_info:
        return [before_info, after_info]
    
    logger.info('两个字典相同')
    return None


def _get_equipment_id(avatar: Dict) -> str:
    """Get equipment ID from avatar dict, or empty string."""
    equipment = avatar.get('equipment')
    if equipment:
        return str(equipment.get('tid'))
    return ''


def generate_remark(
    assist_avatar_list: Optional[List[Dict]],
    avatar_detail_list: Optional[List[Dict]]
) -> Tuple[str, str]:
    """Generate remark string and gold number from avatar lists.
    
    Args:
        assist_avatar_list: List of assist avatar data
        avatar_detail_list: List of avatar detail data
        
    Returns:
        Tuple of (remark, goldNum)
    """
    remark = ''
    
    if assist_avatar_list:
        for avatar in assist_avatar_list:
            avatar_id = avatar.get('avatarId')
            if avatar_id and avatar_id in NEW_AVATAR_IDS:
                rank = avatar.get('rank') or 0
                remark += f"{avatar_id}|{rank}|{_get_equipment_id(avatar)}#"
    
    if avatar_detail_list:
        for avatar in avatar_detail_list:
            avatar_id = avatar.get('avatarId')
            if avatar_id and str(avatar_id) not in remark and avatar_id in NEW_AVATAR_IDS:
                rank = avatar.get('rank') or 0
                remark += f"{avatar_id}|{rank}|{_get_equipment_id(avatar)}#"
    
    avatar_rank_sum, common_avatar_rank_sum = _calculate_avatar_rank_sums(
        assist_avatar_list, avatar_detail_list, GOLD_AVATAR_IDS, COMMON_AVATAR_IDS
    )
    
    gold_num = f"{avatar_rank_sum}|{common_avatar_rank_sum}"
    return remark, gold_num

def generate_development(
    development_info: Optional[List[Dict]]
) -> Tuple[str, str]:
    event_type = ''
    event_time = ''

    if development_info:
        # 取最后一条记录
        last_record = development_info[-1]

        # 提取 timestamp 和 type
        timestamp_str = last_record["timestamp"]
        event_type = last_record["type"]

        # 将字符串时间戳转为整数（秒级）
        ts = int(timestamp_str)

        # 转换为 datetime 对象并格式化
        dt = datetime.datetime.fromtimestamp(ts)
        event_time = dt.strftime("%Y-%m-%d %H:%M:%S")

        logger.debug(f"type: {event_type}, 转换后时间: {event_time}")
    
    return event_time, event_type

def _calculate_avatar_rank_sums(
    assist_avatar_list: Optional[List[Dict]],
    avatar_detail_list: Optional[List[Dict]],
    gold_ids: List[int],
    common_ids: List[int]
) -> Tuple[int, int]:
    """Calculate rank sums for gold and common avatars in a single pass."""
    gold_ids = set(gold_ids)
    common_ids = set(common_ids)
    gold_sum = 0
    common_sum = 0
    
    for avatar_list in (assist_avatar_list, avatar_detail_list):
        if avatar_list is None:
            continue
        for avatar in avatar_list:
            avatar_id = avatar.get('avatarId')
            if avatar_id is None:
                continue
            if avatar_id in gold_ids:
                rank = avatar.get('rank')
                gold_sum += 1 if rank is None else rank + 1
            elif avatar_id in common_ids:
                rank = avatar.get('rank')
                common_sum += 1 if rank is None else rank + 1
    
    return gold_sum, common_sum


def create_dict_from_db(exist: Tuple) -> Dict[str, Any]:
    """Create dictionary from database row.
    
    Args:
        exist: Database row tuple
        
    Returns:
        Dictionary of user info
    """
    return {
        'platform': exist[2], 'signature': exist[1], 'nickname': exist[3], 'level': exist[4],
        'friendCount': exist[5], 'maxRogueChallengeScore': exist[6], 'achievementCount': exist[7],
        'equipmentCount': exist[8], 'avatarCount': exist[9], 'headIcon': exist[10], 'relicCount': exist[11],
        'bookCount': exist[12], 'musicCount': exist[13]
    }


def create_dict_from_response(
    platform, signature, nickname, level, friend_count,
    max_rogue_challenge_score, achievement_count, equipment_count,
    avatar_count, head_icon, relic_count, book_count, music_count
) -> Dict[str, Any]:
    """Create dictionary from API response fields."""
    return {
        'platform': platform, 'signature': signature, 'nickname': nickname, 'level': level,
        'friendCount': friend_count, 'maxRogueChallengeScore': max_rogue_challenge_score,
        'achievementCount': achievement_count, 'equipmentCount': equipment_count,
        'avatarCount': avatar_count, 'headIcon': head_icon, 'relicCount': relic_count,
        'bookCount': book_count, 'musicCount': music_count
    }