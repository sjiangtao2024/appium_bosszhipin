# 使用Appnium Python自动化安卓/IOS应用测试
## 目标
使用Appium Python自动化Boss直聘沟通与简历投递，实现以下功能：
  - 启动Boss直聘App(简历已经准备好)
  - 检索推荐的职位，筛选出符合条件的职位
    - 年龄不超过限制的职位
    - 薪资在指定范围内的职位
    - 大体符合要求的职位（技能点符合2个以上）
    - 离家距离在指定范围内的职位 
  - 点击符合条件的职位，进入职位详情页
    - 点击立即沟通
  - 进入消息页
  "appium:appWaitActivity": "com.hpbr.bosszhipin.module.main.activity.MainActivity, com.hpbr.bosszhipin.module.splash.activity.SplashActivity",
  "appium:automationName": "UiAutomator2",
  "appium:ensureWebviewsHavePages": true,
  "appium:nativeWebScreenshot": true,
  "appium:newCommandTimeout": 3600,
  "appium:connectHardwareKeyboard": true,
  "appium:noReset": true
}
```
##### 由于Boss直聘APP的appActivity使用默认的com.hpbr.bosszhipin.module.main.activity.MainActivity 会报错，所以只能启动到主界面，然后手机上点击Boss直聘APP图标进入，然后进行元素定位

### Python启动代码
#### Python可以使用
```
adb shell monkey -p com.hpbr.bosszhipin -c android.intent.category.LAUNCHER 1
```

### 运行代码

```
python boss_android.py
```

#### 运行结果如下：
```
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 兼职系统工程师投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 兼职运维工程师投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 兼职测试开发投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 兼职Golang投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 兼职Python投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - 测试开发投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - Golang投递数为4
2024-09-24 09:06:56,722 - jobs_data_output - INFO - Python投递数为4
2024-09-24 09:06:56,725 - jobs_data_output - INFO - 总投递数为32
2024-09-24 09:06:56,725 - timer - INFO - retrive_expected_jobs 函数运行时间: 13.96 分钟
```

##图片参考

boss直聘APP界面
<img src="path/to/image.jpg" alt="描述" width="300" height="200">
