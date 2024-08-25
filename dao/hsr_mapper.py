import pymysql
import logging
from contextlib import contextmanager
# 崩坏星穹铁道数据库操作类

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取数据库连接
def get_database_connection(dbhost, dbuser, dbpass, dbname):
    try:
        if dbpass == "" or dbpass == None:
            db = pymysql.connect(host=dbhost, user=dbuser, database=dbname)
        else:
            db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        logging.info("数据库连接成功")
        return db
    except pymysql.Error as e:
        logging.error("数据库连接失败：" + str(e))
        return None

# 关闭数据库
def close_database_connection(db):
    if db:
        db.close()
        logging.info("数据库连接已关闭")

# 获取游标
@contextmanager
def get_cursor(db):
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

# 获取各服务器最大UID
def get_max_uid(db):
    qry_sql = "select uid from sr_max_uid"
    with get_cursor(db) as cursor:
        cursor.execute(qry_sql)
        return cursor.fetchall()

# 获取数据失败记录
def log_request_failure(db, uid, status_code, table_name, error_desc=None):
    try:
        with get_cursor(db) as cursor:
            if error_desc:
                fail_sql = "INSERT INTO sr_user_info_fail_record (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) VALUES (%s, %s, %s, now())"
                cursor.execute(fail_sql, (uid, status_code, error_desc))
            else:
                insert_sql = "INSERT INTO " + table_name + " (UID, CREATE_TIME, remark) VALUES (%s, now(), %s)"
                cursor.execute(insert_sql, (uid, status_code))
            db.commit()
    except pymysql.MySQLError as e:
        logging.error(f"数据库操作失败：{e}")
    except Exception as e:
        logging.error(f"发生未知错误：{e}")

# 根据UID获取用户信息
def get_user_info_by_uid(db, uid, table_name):
    qry_sql = "select `UID`, `signature`, `platform`, `nickname`, `level`, `friend_count`, `max_rogue_challenge_score`, `achievement_count`, `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, `book_count`, `music_count` from " + table_name + " where uid = %s"
    with get_cursor(db) as cursor:
        cursor.execute(qry_sql, (uid,))
        return cursor.fetchone()

# 更新用户信息
def update_user_info(db, uid, table_name, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, before_info, after_info):
    update_sql = "UPDATE " + table_name + " SET UID=%s, signature=%s, platform=%s, nickname=%s, `level`=%s, friend_count=%s, max_rogue_challenge_score=%s, achievement_count=%s, equipment_count=%s, avatar_count=%s, head_icon=%s, remark=%s, relic_count=%s, book_count=%s, music_count=%s, LAST_UPDATE_TIME=now() WHERE UID=%s"
    # 插入用户信息更新记录
    insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
    with get_cursor(db) as cursor:
        cursor.execute(update_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, uid))
        cursor.execute(insert_record_sql, (uid, before_info, after_info))
        db.commit()

# 插入用户信息
def insert_user_info(db, uid, table_name, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount):
    insert_sql = "INSERT INTO " + table_name + " (UID, signature, platform, nickname, `level`, friend_count, max_rogue_challenge_score, achievement_count, equipment_count, avatar_count, head_icon, CREATE_TIME, remark, relic_count, book_count, music_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s)" 
    with get_cursor(db) as cursor:
        cursor.execute(insert_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount))
        db.commit()