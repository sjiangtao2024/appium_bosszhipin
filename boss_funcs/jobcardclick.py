from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException,StaleElementReferenceException
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from typing import Dict,Optional
from .scrollups import scroll_up_cardgroup,scroll_up,scroll_up_job_details,scroll_right_expected_job,scroll_left_expected_job
from .app_log import BossLog
from .timer import timer
from .jobs_data import jobs_data_output
from typing import List, Dict, Union

def locate_rvlist(driver):
    logger = BossLog(log_name='locate_rvlist')
    try:
        logger.info('创建rv_list 元素列表')
        elements = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout"))
        )
        #为了避免点击返回按键后，页面重新刷新的问题，需要再次获取元素
        elements_num = len(elements)
        logger.debug(f'rv_list 元素列表长度为:{elements_num}')
        for i in range(elements_num):
            logger.debug('检索可点击职位卡片')
            element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, f"//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout[{i+1}]"))
            )
            logger.debug(f'第{i+1}个rv_list 元素:{elements[i]}')
            position_name = element.find_element(AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_position_name")
            company_name = element.find_element(AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_company_name")
            salary = element.find_element(AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_salary_statue")
            logger.info(f'{company_name.text}公司的职位 {position_name.text},薪水 {salary.text}，可点击状态为 {element.get_attribute('clickable')}')
            if element.get_attribute('clickable') == 'true':
                element.click()
                #点击后等待1秒等页面跳转
                sleep(1)
                #点击立即沟通按键后返回到职位详情页
                job_card_detail_page_click_chat(driver)
            else:
                logger.info('该职位不可点击')

    except TimeoutException:
        logger.error("TimeoutException")
    except NoSuchElementException as e:
        logger.error(f'定位职位列表失败:{e}')
    except Exception as e:
        logger.error(f'定位职位列表未知错误:{e}')
def job_card_detail_page_click_chat(driver):
    logger = BossLog(log_name='job_card_detail_page_click_chat')
    #获取立即沟通按键
    try:
        logger.debug('获取立即沟通按键')
        position_btn = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/btn_chat"))
        )
        #点击立即沟通
        position_btn.click()
        logger.info('立即沟通已点击')
        #等待页面跳转
        logger.debug('等待1秒页面跳转')
        sleep(1)
        #获取返回按键
        try:
            #因为点击沟通后进入沟通界面，需要点击两次返回职位详情页
            #back_btn = driver.find_element(AppiumBy.ID,'com.hpbr.bosszhipin:id/iv_back')
            logger.debug('获取返回按键')
            back_btn = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.ID,'com.hpbr.bosszhipin:id/iv_back'))
            )
            #第一次点击返回职位详情页
            logger.debug('第一次点击返回职位详情页')
            back_btn.click()
            sleep(1)
            #返回按键需要重新获取
            #第二次点击返回多职位列表页
            logger.debug('再次获取返回按键')
            back_btn = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.ID,'com.hpbr.bosszhipin:id/iv_back'))
            )
            logger.debug('第二次点击返回多职位卡片页')
            back_btn.click()
            sleep(1)
        except NoSuchElementException as e:
            logger.error(f'获取返回按键失败:{e}')
        except Exception as e:
            logger.error(f'返回按键未知错误:{e}')
    except TimeoutException as e:
        logger.error(f'获取立即沟通按键超时:{e}')
    except NoSuchElementException as e:
        logger.error(f'获取立即沟通按键失败:{e}')
    except Exception as e:
        logger.error(f'获取立即沟通按键未知错误:{e}')
#滑动屏幕使得第四个jobcard完全显示
def scroll_1jobcard(driver):
    #充分利用现有成果，减少代码量，窗口使用的还是driver.get_window_size(),实际上应该使用com.hpbr.bosszhipin:id/vp_fragment_tabs的尺寸
    #移动一个jobcard使其完全显示，方便移动下面4个卡片
    try:
        elements = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located(
              (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.hpbr.bosszhipin:id/view_job_card")')  
            )
        )
        #定义误差值，来判断是否需要调整卡片
        tolerance = 80
        for index,element in enumerate(elements):
            if index ==0:
                card_height_std = element.size['height']
            try:
                card_height = element.size['height']
                if card_height > card_height_std + tolerance or card_height < card_height_std - tolerance:
                    scroll_up(driver,element,card_height_std,driver.get_window_size())
            except Exception as e:
                print(f'获取第{index+1}个job card的尺寸失败:{e}')
    except TimeoutException as e:
        print(f"TimeoutException:{e}")
    except NoSuchElementException as e:
        print(f"NoSuchElementException:{e}")
    except Exception as e:
        print(f"未知错误:{e}")
#向下获取更多job cards
def scroll_4jobcards(driver):
    logger = BossLog(log_name='scroll_4jobcards')
    try:
        cards_viewgroup = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/rv_list"))
        )
        cards_viewgroup_size = cards_viewgroup.size
        #设置滑动距离，这里滑动的终点是bar的高度
        bar = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/appBarLayout"))
        )
        bar_height = bar.size['height'] 
        #滚动到顶部
        scroll_up_cardgroup(driver,bar_height,cards_viewgroup_size)
    except Exception as e:
        logger.error(f'滑动职位卡片组失败:{e}')
def scroll_jobcards(driver):
    try:
        #获取job cards组合的窗口大小
        cards_viewgroup = WebDriverWait(driver,10).until(
            #EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/vp_fragment_tabs"))
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/rv_list"))
        )
        cards_viewgroup_size = cards_viewgroup.size
        print(f'卡片集合窗口大小为:{cards_viewgroup_size}')
        #获取所有的job cards
        elements = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout"))
        )
        elements_num = len(elements)
        for i in range(elements_num):
            element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, f"//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout[{i+1}]"))
            )
            print(f'职位卡片的大小:{element.size},位置为{element.location}')
            
    except Exception as e:
        print(f'获取职位卡片位置失败:{e}')
#计算函数运行时间
@timer
def retrive_expected_jobs_test(driver):
    logger = BossLog(log_name='retrive_expected_jobs_test')
    job_results = {}

    try:
        expected_position_location = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/title_container"))
        )
        expected_positions = expected_position_location.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        for position_element in expected_positions:
            expected_position = position_element.text
            logger.info(f'期望职位：{expected_position}')
            position_element.click()
            sleep(1)
            logger.info(f'现在开始申请期望职位{expected_position}的所有职位')
            current_expected_jobs=jobs_apply(driver)
            job_results[expected_position] = current_expected_jobs
        logger.info(f'总申请职位详情:{job_results}')
    except Exception as e:
        logger.error(f"获取期望职位失败，错误信息：{e}")
@timer
def jobs_apply(driver,job_num=1) -> List[Dict[str, Union[str, None]]]:
    logger = BossLog(log_name='jobs_apply')
    try:
        #存储工作的元组
        unique_positions = set()
        while len(unique_positions) < job_num:
            try:
                logger.info('开始获取职位信息')
                elements = WebDriverWait(driver,10).until(
                    EC.presence_of_all_elements_located((AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout"))
                    )
                #为了避免点击返回按键后，页面重新刷新的问题，需要再次获取元素
                elements_num = len(elements)
                logger.info(f'职位列表长度为:{elements_num}')
                for i in range(elements_num):
                    element = WebDriverWait(driver,20).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, f"//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout[{i+1}]"))
                    )
                    if not element.is_displayed():
                        logger.info(f'第{i+1}个职位卡片不可见,等待5秒钟')
                        sleep(5)
                    if element.get_attribute('clickable') == 'true':
                        logger.info(f'现在点击第{i+1}个职位卡片')
                        element.click()
                        #点击后等待1秒等页面跳转
                        sleep(1)
                        #获取job详细信息并写入元组
                        job = job_detailed_info(driver)
                        #logger.info(f'职位详情: {job}')
                        #检查职位是否包含被禁止词，如果包含，则不点击发送简历
                        job_clickable = jobs_blocklist(job['position_name'])
                        if job_clickable:
                            logger.info(f'当前职位{job["position_name"]}包含被禁止词，不点击发送简历,点击模拟发送')
                            job_card_detail_page_click_simulate(driver)
                        else:
                            #点击立即申请按键后返回到职位详情页
                            unique_positions.add(frozenset(job.items()))
                            job_card_detail_page_click_chat(driver)
                            
                        #job_card_detail_page_click_simulate(driver)
                    else:
                        print(f'第{i+1}个职位卡片不可点击')
                
                #移动卡片
                scroll_4jobcards(driver)
                logger.info('卡片已经移动')
                logger.info(f'此时点击职位数为:{len(unique_positions)}')
                sleep(1)
            except TimeoutException as e:
                logger.error(f"TimeoutException:{e}")
            except NoSuchElementException as e:
                logger.error(f"NoSuchElementException:{e}")
            except Exception as e:
                logger.error(f"未知错误:{e}")
        logger.info(f'共找到{len(unique_positions)}个职位')
        #转换frozenset转换为字典列表
        dict_list = [dict(item) for item in unique_positions]
        logger.info(f'职位列表为:{dict_list}')
        return dict_list
        # for job in dict_list:
        #     logger.info(f'职位:{job["position_name"]},公司:{job["company_name"]},薪水:{job["salary"]}')
    except Exception as e:
        logger.error(f'未知错误:{e}')
def job_card_detail_page_click_simulate(driver):
    logger = BossLog(log_name='job_card_detail_page_click_simulate')
    try:
        position_btn = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/btn_chat"))
        )
        #position_btn.click()
        logger.info('点击了模拟立即沟通按钮')
        sleep(1)
        try:
            back_btn = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.ID,'com.hpbr.bosszhipin:id/iv_back'))
            )
            back_btn.click()
            sleep(1)
        except Exception as e:
            logger.error(f'获取返回按键失败:{e}')
    except Exception as e:
        logger.error(f'获取模拟立即沟通按钮失败:{e}')

def job_detailed_info(driver,log_level='INFO') -> Dict[str,Optional[str]]:
    logger = BossLog(log_name='job_detailed_info',log_level=log_level)
    try:
        # logger.info('选取一个职位进入职位详情')
        # element = WebDriverWait(driver,20).until(
        #     EC.presence_of_element_located((AppiumBy.XPATH, f"//androidx.recyclerview.widget.RecyclerView[@resource-id='com.hpbr.bosszhipin:id/rv_list']/android.widget.LinearLayout[1]"))
        # )
        # logger.info(f'当前卡片position:{element.location},size:{element.size}')
        # logger.info(f'driver size:{driver.get_window_size()}')
        # logger.info('点击职位卡片进入职位详情')
        # element.click()
        #点击后等待1秒等页面跳转
        sleep(1)
        #获取顶部信息条
        motion_title = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/motionLayout_title"))
        )
        logger.debug(f'职位详情页顶部信息条:{motion_title.location},{motion_title.size}')
        #获取底部的立即沟通条
        cl_action_bar = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/cl_geek_action"))
        )
        logger.debug(f'职位详情页底部立即沟通条:{cl_action_bar.location},{cl_action_bar.size}')
        logger.debug(f'当前屏幕大小:{driver.get_window_size()}')
        position_name = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_job_name"))
        )
        logger.info(f'职位名称:{position_name.text}')
        position_name_text = position_name.text
        salary = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_job_salary"))
        )
        salary_text = salary.text
        logger.info(f'薪水:{salary.text}')
        #现在开始获取公司信息
        bar_height = motion_title.size['height']
        cl_location_y = cl_action_bar.location['y']
        company_name = get_company_name_in_job_details(driver)
        logger.debug(f'首次获取公司名称:{company_name}')
        while company_name is None:
            logger.debug('公司信息未显示，尝试下拉')
            scroll_up_job_details(driver,bar_height,cl_location_y,driver.get_window_size())
            sleep(1)
            company_name = get_company_name_in_job_details(driver)
        logger.info(f'公司名称:{company_name}')
        return {'position_name':position_name_text,'salary':salary_text,'company_name':company_name}
    except Exception as e:
        logger.error(f'未知错误:{e}')
        return None
def get_company_name_in_job_details(driver) -> str:
    logger = BossLog(log_name='get_company_name_in_job_details')
    try:
        logger.debug('检查公司信息是否显示')
        company_elements = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/tv_com_name"))
        )
        if len(company_elements) != 0:
            logger.debug(f'公司信息显示正常')
            return company_elements[0].text
        else:
            logger.info(f'公司信息未显示')
            return None
    except Exception as e:
        logger.error(f'检查公司信息显示失败:{e}')
        return None
@timer
def retrive_expected_jobs(driver,job_num):
    logger = BossLog(log_name='retrive_expected_jobs')
    job_results = {}
    try:
        
        scroll_view = WebDriverWait(driver,10).until(
            #获取所有uiautomator定位的元素new UiSelector().resourceId("com.hpbr.bosszhipin:id/scroll_view").instance(0)
            #EC.presence_of_all_elements_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/scroll_view").instance'))
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/scroll_view").instance(0)'))
         )
        #初始化期望职位组的位置和大小
        logger.debug(f'滚动视图位置:{scroll_view.location},大小:{scroll_view.size}')
        #向右滑动期望职位组
        logger.debug('向右滑动期望职位组')
        scroll_right_expected_job(driver,scroll_view.location,scroll_view.size)
        expected_jobs_group_location = scroll_view.location
        expected_jobs_group_size = scroll_view.size
        logger.debug(f'期望职位组位置:{expected_jobs_group_location},大小:{expected_jobs_group_size}')
        #获取期望职位组内所有职位
        expected_positions = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/title_container"))
            ).find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        logger.debug(f'期望职位组内职位数:{len(expected_positions)}')
        #遍历期望职位组内所有职位
        for position_element in expected_positions:
            expected_position = position_element.text
            logger.info(f'期望职位：{expected_position}')
            position_element.click()
            sleep(1)
            #如果是兼职，需要进一步处理，因为兼职会有中栏的存在，需要再次点选不同的兼职期望职位
            if expected_position == '兼职':
                #检查是否存在中栏
                if check_mid_tab(driver):
                    #获取兼职期望职位下的所有职位
                    part_time_job_results =retrive_part_time_jobs(driver,job_num)
                    job_results[expected_position] = part_time_job_results
                    continue
                else:
                    logger.info(f'兼职期望职位下不存在中栏')
            else:
                logger.info(f'非兼职期望职位,不需要处理')
            #点击筛选栏中的最新职位
            logger.info(f'现在开始点击期望职位{expected_position}筛选栏中的最新职位')
            filter_latestjob(driver)
            logger.info(f'现在开始申请期望职位{expected_position}的所有职位')
            current_expected_jobs=jobs_apply(driver,job_num)
            job_results[expected_position] = current_expected_jobs
        #logger.info(f'当前期望职位{expected_position}的职位详情:{job_results}')
        #获取当前期望职位的最后一个职位
        last_expected_position = expected_positions[-1].text
        logger.debug(f'最后一个期望职位:{last_expected_position}')
        #尝试向左滑动获取更多期望职位(期望职位最多4个)
        try:
            scroll_left_expected_job(driver,expected_jobs_group_location,expected_jobs_group_size)
            logger.debug('尝试向左滑动获取更多期望职位')
            expected_positions = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.hpbr.bosszhipin:id/title_container"))
            ).find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            logger.debug(f'向左滑动后期望职位组内职位数:{len(expected_positions)}')
            #如果倒数第二个职位与之前最后一个职位相等，那么说明存在第四个期望职位
            last_expected_position_4 = expected_positions[-1].text
            logger.debug(f'向左滑动视图进行渲染后的最后一个期望职位是:{last_expected_position_4}')
            last_expected_position_3 = expected_positions[-2].text
            logger.debug(f'向左滑动视图进行渲染后的倒数第二个期望职位是:{last_expected_position_3}')
            if expected_positions[-2].text == last_expected_position:
                #点击第四个期望职位
                logger.debug('存在第四个期望职位')
                logger.debug(f'点击第四个期望职位:{expected_positions[-1].text}')
                expected_positions[-1].click()
                sleep(1)
                #此时点击筛选栏中的最新
                logger.info(f'现在开始点击职位{expected_positions[-1].text}筛选栏中的最新职位')
                filter_latestjob(driver)
                sleep(1)
                logger.info(f'现在开始申请期望职位{expected_positions[-1].text}的所有职位')
                current_expected_jobs=jobs_apply(driver,job_num)
                job_results[expected_positions[-1].text] = current_expected_jobs
                logger.info(f'当前期望职位{expected_positions[-1].text}的职位详情:{current_expected_jobs}')      
        except Exception as e:
            logger.error(f'向左滑动期望职位失败:{e}')  
        logger.info(f'总共找到{len(job_results)}个期望职位的职位详情:{job_results}')
        jobs_data_output(job_results)  
    except Exception as e:
        logger.error(f'获取期望职位失败，错误信息:{e}')

#检查期望职位为兼职时，是否存在中栏
def check_mid_tab(driver) -> bool:
    logger = BossLog(log_name='check_mid_tab')
    try:
        mid_tab = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/mid_tab"))
        )
        if len(mid_tab) == 0:
            logger.info(f'当前页面没有中栏')
            return False
        else:
            logger.info(f'当前页面有中栏')
            #检查是否有scroll_view
            scroll_view = mid_tab[0].find_elements(AppiumBy.CLASS_NAME,'android.widget.HorizontalScrollView')
            if len(scroll_view) == 0:
                logger.info(f'中栏没有scroll_view')
                return False
            else:
                logger.info(f'中栏有scroll_view')
                logger.info(f'中栏scroll_view位置:{scroll_view[0].location},大小:{scroll_view[0].size}')           
                return True
    except Exception as e:
        logger.error(f'检查中栏失败:{e}')
        return False
def retrive_part_time_jobs(driver,job_num) -> List[Dict[str,Union[str,None]]]:
    logger = BossLog(log_name='retrive_part_time_jobs')
    part_time_job_results = {}
    try:
        scroll_view = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/scroll_view").instance(1)'))
        )
        logger.debug(f'兼职视图位置:{scroll_view.location},大小:{scroll_view.size}')
        #向右滑动兼职视图
        scroll_right_expected_job(driver,scroll_view.location,scroll_view.size)
        sleep(2)
        def get_part_time_jobs():
            return WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/title_container").instance(0)'))
            ).find_elements(AppiumBy.CLASS_NAME,'android.widget.TextView')
        part_time_expected_jobs = retry_on_stale_element(get_part_time_jobs)
        # part_time_expected_jobs = WebDriverWait(driver,10).until(
        #     EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/title_container").instance(1)'))
        # ).find_elements(AppiumBy.CLASS_NAME,'android.widget.TextView')
        logger.info(f'兼职期望职位数:{len(part_time_expected_jobs)}')
        for part_time_expected_job in part_time_expected_jobs:
            try:
            #logger.info(f'兼职期望职位:{part_time_expected_job.text}')
                part_time_expected_job_text = part_time_expected_job.text
                #跳过综合期望职位
                if part_time_expected_job_text == '综合':
                    continue
                logger.info(f'兼职期望职位:{part_time_expected_job_text}')
                #点击兼职期望职位
                part_time_expected_job.click()
                sleep(1)
                #进入兼职期望职位后，点击筛选栏中的最新发布职位
                logger.info(f'现在开始点击兼职职位{part_time_expected_job_text}职位筛选中的最新发布职位')
                filter_latestjob(driver)
                sleep(1)
                #申请兼职职位
                current_part_time_expected_jobs = jobs_apply(driver,job_num)
                part_time_job_results[part_time_expected_job_text] = current_part_time_expected_jobs
                logger.info(f'当前兼职期望职位:{part_time_expected_job_text}的职位详情:{current_part_time_expected_jobs}')
            except StaleElementReferenceException as e:
                logger.warning(f'兼职期望职位:{part_time_expected_job_text}已失效,跳过当前职位')
                continue
                
        last_part_time_expected_job_position = part_time_expected_jobs[-1].text
        logger.info(f'最后一个兼职期望职位:{last_part_time_expected_job_position}')
        #尝试向左滑动兼职视图获取更多兼职期望职位(最多5个)
        try:
            scroll_left_expected_job(driver,scroll_view.location,scroll_view.size)
            logger.info('尝试向左滑动兼职视图获取更多兼职期望职位')
            part_time_expected_jobs = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.hpbr.bosszhipin:id/title_container").instance(1)'))
            ).find_elements(AppiumBy.CLASS_NAME,'android.widget.TextView')
            last_part_time_expected_job_position_1 = part_time_expected_jobs[-1].text
            logger.info(f'向左滑动兼职视图进行渲染后的最后一个兼职期望职位是:{last_part_time_expected_job_position_1}')
            if last_part_time_expected_job_position_1 != last_part_time_expected_job_position:
                #说明存在更多兼职期望职位
                part_time_expected_jobs[-1].click()
                sleep(1)
                #点击完期望职位后，需要点击筛选栏中的最新发布职位
                filter_latestjob(driver) 
                sleep(1)
                logger.info(f'最后一个兼职期望岗位{last_part_time_expected_job_position_1}已点击')
                logger.info(f'现在开始申请兼职期望职位:{last_part_time_expected_job_position_1}的所有职位')
                current_part_time_expected_jobs = jobs_apply(driver,job_num)
                part_time_job_results[last_part_time_expected_job_position_1] = current_part_time_expected_jobs
                logger.info(f'当前兼职期望职位:{last_part_time_expected_job_position_1}的职位详情:{current_part_time_expected_jobs}')
                last_part_time_expected_job_position_2 = part_time_expected_jobs[-2].text
                if last_part_time_expected_job_position_2 != last_part_time_expected_job_position:
                    part_time_expected_jobs[-2].click()
                    sleep(1)
                    #点击完期望职位后，需要点击筛选栏中的最新发布职位
                    logger.info(f'现在开始点击兼职职位{last_part_time_expected_job_position_2}职位筛选中的最新发布职位')
                    filter_latestjob(driver) 
                    sleep(1)
                    logger.info(f'倒数第二个兼职期望岗位:{last_part_time_expected_job_position_2}已点击')
                    logger.info(f'现在开始申请兼职期望职位:{last_part_time_expected_job_position_2}的所有职位')
                    current_part_time_expected_jobs = jobs_apply(driver,job_num)
                    part_time_job_results[last_part_time_expected_job_position_2] = current_part_time_expected_jobs
                    logger.info(f'当前兼职期望职位:{last_part_time_expected_job_position_2}的职位详情:{current_part_time_expected_jobs}')
                else:
                    logger.info(f'倒数第二个兼职期望岗位:{last_part_time_expected_job_position_2}与最后一个兼职期望岗位:{last_part_time_expected_job_position}相同')
            else:
                logger.info(f'向左滑动视图进行渲染后的最后一个兼职职位:{last_part_time_expected_job_position_1}与最后一个兼职职位:{last_part_time_expected_job_position}相同')
        except Exception as e:
            logger.error(f'向左滑动兼职视图失败:{e}')
        logger.info(f'总共找到{len(part_time_job_results)}个兼职期望职位的职位详情:{part_time_job_results}')
        return part_time_job_results
    except Exception as e:
        logger.error(f'获取兼职期望职位失败，错误信息:{e}')

def filter_latestjob(driver):
    logger = BossLog(log_name='filter_latestjob')
    try:
        #等待选择栏出现
        filter_bar = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((AppiumBy.ID,"com.hpbr.bosszhipin:id/ly_left"))
        )
        filter_latest = filter_bar.find_element(AppiumBy.XPATH,'//android.widget.LinearLayout[@resource-id="com.hpbr.bosszhipin:id/ly_left"]/android.widget.FrameLayout[3]')
        logger.info(f'点击筛选栏中的最新发布职位')
        filter_latest.click()
    except Exception as e:
        logger.error(f'筛选栏中未找到最新发布职位:{e}')

def jobs_blocklist(job_name) -> bool:
    jobs_blocklist = ['教师','老师','导师','java','Java','JAVA','数据分析','时间自由','教育','培训','考试','考研','讲师','留学生','视频','咨询','写手','编辑','校对','教练','合伙人','需求经理','顾问','房贷','算法','数据科学家','夜班','高考','规划师','大模型','辅导','SAP','黑灰产','欠款','推广','翻译','助教','债务','合作伙伴','医美','撰写','生信分析','销售','网贷','美业精英','营养师','拉新','流量','视频','数据标注','维修']
    for job_block in jobs_blocklist:
        if job_name.find(job_block) != -1:
            #如果找到，则返回True
            return True
    return False

def retry_on_stale_element(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            sleep(1) 