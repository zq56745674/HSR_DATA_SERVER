import pymysql
import logging
import threading
import queue
from typing import Optional, Tuple, Any, List

logger = logging.getLogger(__name__)

_local = threading.local()


def get_cursor(db: pymysql.Connection):
    """Return a reusable thread-local cursor for the given connection."""
    cache = getattr(_local, 'cursor_cache', None)
    if cache is None:
        cache = {}
        _local.cursor_cache = cache
    key = id(db)
    cursor = cache.get(key)
    if cursor is None:
        cursor = db.cursor()
        cache[key] = cursor
    return cursor


def get_database_connection(host: str, user: str, password: str, database: str) -> Optional[pymysql.Connection]:
    """Create and return a database connection.
    
    Args:
        host: Database host
        user: Database user
        password: Database password
        database: Database name
        
    Returns:
        Database connection or None if failed
    """
    try:
        if not password:
            db = pymysql.connect(host=host, user=user, database=database, autocommit=True)
        else:
            db = pymysql.connect(host=host, user=user, password=password, database=database, autocommit=True)
        logger.info("Database connected successfully")
        return db
    except pymysql.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None


def close_database_connection(db: Optional[pymysql.Connection]) -> None:
    """Close database connection safely."""
    if db:
        try:
            db.close()
            logger.info("Database connection closed")
        except pymysql.Error as e:
            logger.error(f"Error closing database: {e}")


def clone_connection(db: pymysql.Connection) -> pymysql.Connection:
    """Create a new independent connection using an existing connection's parameters."""
    password = db.password
    if isinstance(password, bytes):
        password = password.decode()
    return pymysql.connect(
        host=db.host,
        port=db.port,
        user=db.user,
        password=password or '',
        database=db.db,
        autocommit=False,
    )


class ConnectionPool:
    """A minimal thread-safe connection pool with stale-connection recovery."""

    def __init__(self, maxsize: int = 5):
        self._maxsize = maxsize
        self._idle = queue.Queue()
        self._lock = threading.Lock()
        self._total = 0

    def get(self, template_db: pymysql.Connection) -> pymysql.Connection:
        """Acquire a connection, creating or reconnecting as needed."""
        try:
            conn = self._idle.get_nowait()
        except queue.Empty:
            with self._lock:
                if self._total < self._maxsize:
                    self._total += 1
                    return clone_connection(template_db)
            conn = self._idle.get()
        try:
            conn.ping(reconnect=True)
            return conn
        except Exception:
            conn.close()
            return clone_connection(template_db)

    def put(self, conn: Optional[pymysql.Connection]) -> None:
        """Return a connection to the pool."""
        if conn is not None:
            self._idle.put(conn)

    def close_all(self) -> None:
        """Close all idle connections in the pool."""
        while True:
            try:
                conn = self._idle.get_nowait()
                conn.close()
            except queue.Empty:
                break


_pool: Optional[ConnectionPool] = None
_pool_lock = threading.Lock()


def get_connection_pool(maxsize: int = 5) -> ConnectionPool:
    """Return the process-wide connection pool (created lazily)."""
    global _pool
    with _pool_lock:
        if _pool is None:
            _pool = ConnectionPool(maxsize)
        return _pool


def reconnect_database(db: pymysql.Connection) -> None:
    """Reconnect to database."""
    try:
        db.ping(reconnect=True)
        logger.info("Database reconnected")
    except pymysql.Error as e:
        logger.error(f"Database reconnection failed: {e}")


def get_max_uid(db: pymysql.Connection) -> List[Tuple[Any]]:
    """Get maximum UID for each server.
    
    Args:
        db: Database connection
        
    Returns:
        List of tuples containing UIDs
    """
    query = "SELECT uid FROM sr_max_uid"
    db.commit()
    cursor = get_cursor(db)
    cursor.execute(query)
    return cursor.fetchall()


def log_request_failure(
    db: pymysql.Connection,
    uid: str,
    status_code: int,
    table_name: str,
    error_desc: Optional[str] = None
) -> None:
    """Log failed request to database.
    
    Args:
        db: Database connection
        uid: User ID
        status_code: HTTP status code
        table_name: Target table name
        error_desc: Error description
    """
    try:
        cursor = get_cursor(db)
        if error_desc:
            query = """
                INSERT INTO sr_user_info_fail_record 
                (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) 
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (uid, status_code, error_desc))
        else:
            query = f"""
                INSERT IGNORE INTO {table_name} 
                (UID, CREATE_TIME, remark) 
                VALUES (%s, NOW(), %s)
            """
            cursor.execute(query, (uid, status_code))
    except pymysql.MySQLError as e:
        logger.error(f"Database operation failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


def get_user_info_by_uid(
    db: pymysql.Connection,
    uid: str,
    table_name: str
) -> Optional[Tuple]:
    """Get user information by UID.
    
    Args:
        db: Database connection
        uid: User ID
        table_name: Table name
        
    Returns:
        User info tuple or None
    """
    query = f"""
        SELECT `UID`, `signature`, `platform`, `nickname`, `level`, 
               `friend_count`, `max_rogue_challenge_score`, `achievement_count`, 
               `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, 
               `book_count`, `music_count`, goldNum 
        FROM {table_name} 
        WHERE uid = %s
    """
    cursor = get_cursor(db)
    cursor.execute(query, (uid,))
    return cursor.fetchone()


def upsert_user_info(
    db: pymysql.Connection,
    uid: str,
    table_name: str,
    signature: str,
    platform: str,
    nickname: str,
    level: int,
    friend_count: int,
    max_rogue_challenge_score: int,
    achievement_count: int,
    equipment_count: int,
    avatar_count: int,
    head_icon: str,
    remark: str,
    relic_count: int,
    book_count: int,
    music_count: int,
    gold_num: str,
    eventTime: str,
    eventType: str
) -> int:
    """Insert or update user information with a single UPSERT statement.

    Returns:
        Affected row count (1 = inserted, 2 = updated, 0 = unchanged).
    """
    query = f"""
        INSERT INTO {table_name} 
        (UID, signature, platform, nickname, `level`, friend_count, 
         max_rogue_challenge_score, achievement_count, equipment_count, 
         avatar_count, head_icon, CREATE_TIME, remark, relic_count, 
         book_count, music_count, goldNum, eventTime, eventType) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            signature=VALUES(signature), platform=VALUES(platform), nickname=VALUES(nickname),
            `level`=VALUES(`level`), friend_count=VALUES(friend_count),
            max_rogue_challenge_score=VALUES(max_rogue_challenge_score),
            achievement_count=VALUES(achievement_count), equipment_count=VALUES(equipment_count),
            avatar_count=VALUES(avatar_count), head_icon=VALUES(head_icon), remark=VALUES(remark),
            relic_count=VALUES(relic_count), book_count=VALUES(book_count), music_count=VALUES(music_count),
            goldNum=VALUES(goldNum), eventTime=VALUES(eventTime), eventType=VALUES(eventType),
            LAST_UPDATE_TIME=NOW()
    """
    cursor = get_cursor(db)
    cursor.execute(query, (
        uid, signature, platform, nickname, level, friend_count,
        max_rogue_challenge_score, achievement_count, equipment_count,
        avatar_count, head_icon, remark, relic_count, book_count,
        music_count, gold_num, eventTime, eventType
    ))
    return cursor.rowcount


def insert_user_info_upd_record(
    db: pymysql.Connection,
    uid: str,
    before_info: str,
    after_info: str
) -> None:
    """Insert user information update record.
    
    Args:
        db: Database connection
        uid: User ID
        before_info: Previous information
        after_info: Updated information
    """
    query = """
        INSERT INTO `sr_user_info_upd_record` 
        (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) 
        VALUES (%s, NOW(), %s, %s, NOW())
    """
    cursor = get_cursor(db)
    cursor.execute(query, (uid, before_info, after_info))


