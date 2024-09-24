import time
from .app_log import BossLog
def timer(func):
    logger = BossLog(log_name='timer')
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)
        end_time = time.time()    # 记录结束时间
        execution_time_minutes = round((end_time - start_time) / 60, 2)
        logger.info(f"{func.__name__} 函数运行时间: {execution_time_minutes} 分钟")
        return result
    return wrapper