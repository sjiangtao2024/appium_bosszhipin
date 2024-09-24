from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from .scrollups import scroll_up
# def scroll_up(driver,card_element,expected_height=262,screen_size={'width':720,'height':1600}):
#     #获取卡片当前的位置和大小
#     card_location = card_element.location
#     card_size = card_element.size
#     #计算需要滚动的距离
#     scroll_distance = expected_height - card_size['height']
#     #确保滚动距离不会超出屏幕范围
#     max_scroll = card_location['y'] - (screen_size['height']*0.1) #留出10%的顶部空间
#     scroll_distance = min(scroll_distance,max_scroll)
#     #计算滑动的起点和终点
#     start_x = screen_size['width']*0.5
#     start_y = screen_size['height']*0.8
#     end_y = start_y - scroll_distance
#     #执行滑动操作
#     # driver.swipe(start_x, start_y, start_x, end_y, 500)
#     actions = ActionChains(driver)
#     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#     actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
#     actions.w3c_actions.pointer_action.pointer_down()
#     actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
#     actions.w3c_actions.pointer_action.release()
#     actions.perform()
#     #等待一段时间，以便页面滚动完成，确保页面已经重新渲染
#     driver.implicitly_wait(1)
#     #再次检查卡片大小，如果还不是预期大小，可以再次尝试滚动
#     updated_card_size = card_element.size
#     if updated_card_size['height'] < expected_height:
#         scroll_up(driver,card_element,expected_height,screen_size)
def get_job_cards(driver):
    try:
        elements = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located(
              (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.hpbr.bosszhipin:id/view_job_card")')  
            )
        )
        #定义误差值，以便判断卡片是否已经完全显示
        tolerance = 30
        for index,element in enumerate(elements):
            print(f'职位卡片{index+1}')
            #将第一个职位卡片的高度作为基准，计算需要滚动的距离
            if index == 0:
                card_height_std = element.size['height']
            try:
                card_height = element.size['height']
                if card_height > card_height_std + tolerance or card_height < card_height_std - tolerance:
                    scroll_up(driver,element,card_height_std,driver.get_window_size())
                position_name = element.find_element(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_position_name").text
                salary = element.find_element(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_salary_statue").text
                company_name = element.find_element(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_company_name").text
                scales = element.find_elements(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_scale")
                if len(scales) == 0:
                    scale = "无"
                else:
                    scale = scales[0].text
                stages = element.find_elements(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_stage")
                if len(stages) == 0:
                    stage = "无"
                else:
                    stage = stages[0].text
                #现在开始求职者要求
                try:
                    fl_require = element.find_element(AppiumBy.ID, "com.hpbr.bosszhipin:id/fl_require_info")
                    #收集所有求职者要求
                    fl_require_list = []
                    fl_require_infos = fl_require.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
                    for fl_require_info in fl_require_infos:
                        fl_require_list.append(fl_require_info.text)
                    if len(fl_require_list) > 0:
                        print(f'求职者要求列表:{fl_require_list}')
                except Exception as e:
                    print(f'获取求职者要求失败，错误信息：{e}')
                employers = element.find_elements(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_employer")
                if len(employers) == 0:
                    employer = "无"
                else:
                    employer = employers[0].text
                active_statuss = element.find_elements(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_active_status")
                if len(active_statuss) == 0:
                    active_status = "无"
                else:
                    active_status = active_statuss[0].text
                distances = element.find_elements(AppiumBy.ID, "com.hpbr.bosszhipin:id/tv_distance")
                if len(distances) == 0:
                    distance = "无"
                else:
                    distance = distances[0].text
                print(f'推荐职位:{position_name}, 薪资:{salary}')
                print(f'公司:{company_name}')
                print(f'公司规模:{scale}, 公司融资:{stage}')
                print(f'公司招聘人员信息:{employer}, 活跃程度:{active_status}')
                print(f'公司所在位置:{distance}')
            except NoSuchElementException as e:
                print(f"获取推荐职位信息失败,需要滚动元素重新获取元素所有属性")
            sleep(1)
    except TimeoutException as e:
        print(f"获取推荐职位卡片超时,错误信息：{e}")
def get_expected_jobs(driver):
    try:
        expected_position_location = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/title_container"))
        )
        expected_positions = expected_position_location.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        for position_element in expected_positions:
            print(f'期望职位：{position_element.text}')
            position_element.click()
            sleep(1)
            get_job_cards(driver)
    except Exception as e:
        print(f"获取期望职位失败，错误信息：{e}")
        