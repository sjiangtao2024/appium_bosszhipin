from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .app_log import BossLog
def scroll_up(driver,card_element,expected_height=262,screen_size={'width':720,'height':1600}):
    #获取卡片当前的位置和大小
    card_location = card_element.location
    card_size = card_element.size
    #计算需要滚动的距离
    scroll_distance = expected_height - card_size['height']
    #确保滚动距离不会超出屏幕范围
    max_scroll = card_location['y'] - (screen_size['height']*0.1) #留出10%的顶部空间
    scroll_distance = min(scroll_distance,max_scroll)
    #计算滑动的起点和终点
    start_x = screen_size['width']*0.5
    start_y = screen_size['height']*0.8
    end_y = start_y - scroll_distance
    #执行滑动操作
    # driver.swipe(start_x, start_y, start_x, end_y, 500)
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    #等待一段时间，以便页面滚动完成，确保页面已经重新渲染
    driver.implicitly_wait(1)
    #再次检查卡片大小，如果还不是预期大小，可以再次尝试滚动
    updated_card_size = card_element.size
    if updated_card_size['height'] < expected_height:
        scroll_up(driver,card_element,expected_height,screen_size)

def scroll_up_cardgroup(driver,bar_height,screen_size):
    logger = BossLog(log_name='scroll_up_cardgroup')
    #计算滑动的起点和终点
    logger.debug(f'screen_size:{screen_size}')
    logger.debug(f'bar_height:{bar_height}')
    start_x = round(screen_size['width'] * 0.5)
    start_y = round(screen_size['height'] * 0.9)
    #end_y = start_y - scroll_distance #滑动距离
    end_y = start_y - bar_height * 3
    logger.debug(f'start_x:{start_x},start_y:{start_y},end_y:{end_y}')
    end_y = max(end_y,screen_size['height'] * 0.1)
    logger.debug(f'end_y:{end_y}')
    #执行滑动操作
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    # 等待页面渲染
    driver.implicitly_wait(1)
def scroll_up_job_details(driver,bar_height,cl_location_y,screen_size):
    logger = BossLog(log_name='scroll_up_job_details')
    logger.debug(f'screen_size:{screen_size}')
    logger.debug(f'bar_height:{bar_height}')
    logger.debug(f'cl_location_y:{cl_location_y}')
    start_x = round(screen_size['width'] * 0.5)
    #触点尽量向上，以免坐标与元素重合无法滑动
    start_y = cl_location_y - bar_height
    #每次移动bar_height 的距离,大约500
    end_y = start_y - bar_height * 5
    logger.debug(f'start_x:{start_x},start_y:{start_y},end_y:{end_y}')
    #防止从屏幕外滑动
    end_y = max(end_y,screen_size['height'] * 0.1)
    logger.debug(f'end_y:{end_y}')
    #执行滑动操作
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    # 等待页面渲染
    driver.implicitly_wait(1)
    #检查company的id是否出现
#向右滑动以便使期望职位的卡片移动到最初始的位置
def scroll_right_expected_job(driver,scroll_view_location,scroll_view_size):
    logger = BossLog(log_name='scroll_right_expected_job')
    logger.debug(f'scroll_view_location:{scroll_view_location},scroll_view_size:{scroll_view_size}')
    #设置滑动起点，因为是向右进行滑动，所以x坐标为滑动视图宽度的0.2,y坐标为滑动视图高度的0.5
    start_x = scroll_view_location['x'] + round(scroll_view_size['width'] * 0.2)
    start_y = scroll_view_location['y'] + round(scroll_view_size['height'] * 0.5)
    #设置滑动终点，x坐标为滑动视图宽度的0.8,y坐标为滑动视图高度的0.5
    end_x = scroll_view_location['x'] + round(scroll_view_size['width'] * 0.8)
    end_y = start_y
    logger.debug(f'start_x:{start_x},start_y:{start_y},end_x:{end_x},end_y:{end_y}')
    #执行滑动操作
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    #等待页面渲染
    driver.implicitly_wait(1)
def scroll_left_expected_job(driver,scroll_view_location,scroll_view_size):
    logger = BossLog(log_name='scroll_left_expected_job')
    logger.debug(f'scroll_view_location:{scroll_view_location},scroll_view_size:{scroll_view_size}')
    #设置滑动起点，因为是向左进行滑动，所以x坐标为滑动视图宽度的0.8,y坐标为滑动视图高度的0.5
    start_x = scroll_view_location['x'] + round(scroll_view_size['width'] * 0.8)
    start_y = scroll_view_location['y'] + round(scroll_view_size['height'] * 0.5)
    #设置滑动终点，x坐标为滑动视图宽度的0.2,y坐标为滑动视图高度的0.5
    end_x = scroll_view_location['x'] + round(scroll_view_size['width'] * 0.2)
    end_y = start_y
    logger.debug(f'start_x:{start_x},start_y:{start_y},end_x:{end_x},end_y:{end_y}')
    #执行滑动操作
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    #等待页面渲染
    driver.implicitly_wait(1)
