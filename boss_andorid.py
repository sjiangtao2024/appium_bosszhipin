import json,os
from time import sleep
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from appium import webdriver
from boss_funcs import BossLog,retrive_expected_jobs

load_dotenv()
logger = BossLog(log_name="boss_andorid")
REMOTE_URL = os.getenv("REMOTE_URL")
CAPABILITIES_FILE_NAME = os.getenv("CAPABILITIES_FILE_NAME")
JOB_NUM = os.getenv("JOB_NUM")
logger.debug(f'JOB_NUM:{JOB_NUM}')
logger.debug(f'CAPABILITIES_FILE_NAME:{CAPABILITIES_FILE_NAME}')
logger.debug("正在初始化Appium")
logger.debug(f"REMOTE_URL:{REMOTE_URL}")
with open(CAPABILITIES_FILE_NAME, "r", encoding="utf-8") as file:
    capablities = json.load(file)
logger.debug(f"desired capabilities:{capablities}")
options = AppiumOptions()
options.load_capabilities(capablities)
driver = webdriver.Remote(f"{REMOTE_URL}", options=options)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "com.hihonor.android.launcher:id/launcher_root_view"))
    )
    logger.info("手机设备已就绪")
    logger.debug("启动Boss直聘APP")
    driver.execute_script('mobile: shell', {
        'command': 'monkey',
        'args': ['-p', 'com.hpbr.bosszhipin', '-c', 'android.intent.category.LAUNCHER', '1']
    })
    sleep(1)
    current_package = driver.current_package
    logger.info(f"当前APP包名:{current_package}")
    if current_package == "com.hpbr.bosszhipin":
        logger.info("Boss 直聘 App 已启动")
    else:
        logger.error("启动 Boss 直聘 App 失败")
    sleep(1)

    logger.info("开始执行手机任务")
    retrive_expected_jobs(driver,JOB_NUM)

except TimeoutException as e:
    logger.error(f'Error:主页面加载超时: {e}')

finally:
    try:
        initial_page = driver.current_package
        driver.press_keycode(AndroidKey.BACK)
        logger.info("按下第一次返回键")
        sleep(1)
        driver.press_keycode(AndroidKey.BACK)
        logger.info("按下第二次返回键")
        sleep(1)
        current_package = driver.current_package
        if current_package != initial_page:
            logger.info(f"已回到初始页面,当前前台应用为{current_package}")
        else:
            driver.press_keycode(AndroidKey.HOME)
            logger.info("已回到桌面")
            sleep(2)
    except Exception as e:
        logger.error(f"Error: 模拟Home键失败:{e}")
    driver.quit()