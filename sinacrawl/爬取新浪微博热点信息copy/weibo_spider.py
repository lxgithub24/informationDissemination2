# coding=utf-8

import time            
import re            
import os  
import time 
import string
import datetime 
import sys  
import codecs  
import shutil
import urllib 
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains



# 先调用无界面浏览器PhantomJS或Firefox    
# driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")    
driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver, 10)


# 全局变量 文件操作读写信息
infofile = codecs.open("hottopic.txt", 'w', 'utf-8')
# topiclist = codecs.open("hotlist.txt",'w','utf-8')

def LoginWeibo(username, password):
    try:
        # 输入用户名/密码登录
        print u'准备登陆Weibo.cn网站...'
        driver.get("http://login.sina.com.cn/")
#        driver.get("http://weibo.com/login.php")
        elem_user = driver.find_element_by_name("username")
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.send_keys(password)  # 密码
        # elem_rem = driver.find_element_by_name("safe_login")
        # elem_rem.click()             #安全登录

        # 重点: 暂停时间输入验证码(http://login.weibo.cn/login/ 手机端需要)
        time.sleep(2)
        
        # elem_sub = driver.find_element_by_xpath("//input[@class='smb_btn']")
        # elem_sub.click()              #点击登陆 因无name属性
        elem_pwd.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # 获取Coockie 推荐资料：http://www.cnblogs.com/fnng/p/3269450.html
        print driver.current_url
        print driver.get_cookies()  # 获得cookie信息 dict存储
        print u'输出Cookie键值对信息:'
        for cookie in driver.get_cookies(): 
            # print cookie
            for key in cookie:
                print key, cookie[key]
                    
        # driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print u'登陆成功...'
        
        
    except Exception, e:      
        print "Error: ", e
    finally:    
        print u'End LoginWeibo!\n\n'

def GetTopic():
    try:
        topiclist = codecs.open("hotlist.txt", 'w', 'utf-8')
        driver.get("http://d.weibo.com/100803")
        item_topics = driver.find_elements_by_xpath("//div[@class='title W_autocut']/a[@class='S_txt1']")
        k = 0
        while k < len(item_topics):
            topiclist.write(item_topics[k].text.replace("#", "").replace(".", "") + '\r\n')
            k = k + 1
        topiclist.close()
    except Exception, e:      
        print "Error: ", e
    finally:    
        print '读取热点话题列表'
        print '**********************************************\n'

# ##热点信息
def GetComment(key):
    try:
        global infofile  # 全局文件变量
        driver.get("http://s.weibo.com/")
        print u'搜索热点主题：', key

        # 输入主题并点击搜索
        item_inp = driver.find_element_by_xpath("//input[@class='searchInp_form']")
        item_inp.send_keys(key)
        item_inp.send_keys(Keys.RETURN)  # 采用点击回车直接搜索


        # 翻页
        j = 1
        while j <= 2:
            url = 'http://s.weibo.com/weibo/' + key + '&Refer=index' + '?page=' + str(j)
            driver.get(url)

        # 内容
            content = driver.find_elements_by_xpath("//div[@class='content clearfix']/div/p")
#             content = driver.find_elements_by_xpath("//p[@class='comment_txt']")
            username = driver.find_elements_by_xpath("//div[@class='content clearfix']/div/a[@class='W_texta W_fb']")
            repost = driver.find_elements_by_xpath("//div[@class='feed_action clearfix']/ul/li")
            posttime = driver.find_elements_by_xpath("//div[@class='content clearfix']/div[@class='feed_from W_textb']/a[@class='W_textb']")
#             currentdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            
            print content
            i = 0
            print u'长度', len(content)
            while i < len(content):
                print '微博信息:'
                print content[i].text
        # 用户名，博文，转发数，评论数
                
                print posttime[i].text
                currenttime = (posttime[i].text.replace(" ", "").replace(":", "-")).encode("utf-8")
                print currenttime
                if "今天" in currenttime:
                    print '今天'
                    a = time.strftime('%Y-%m-%d', time.localtime(time.time())) + "-"
                    currenttime = currenttime.replace("今天", a) + "-00"
                    timeArray = time.strptime(currenttime, "%Y-%m-%d-%H-%M-%S")
                    timeStamp = int(time.mktime(timeArray))
                elif "月" in currenttime:
                    print '月'
                    currenttime = "2016-" + currenttime.replace("月", "-").replace("日", "-")
                    currenttime = currenttime + "-00"
                    tmp = currenttime.split('-')
                    if len(tmp[1]) == 1:
                        tmp[1] = "0" + tmp[1]
                    if len(tmp[2]) == 1:
                        tmp[2] = "0" + tmp[2]
                    currenttime = "-".join(tmp)
                    timeArray = time.strptime(currenttime, "%Y-%m-%d-%H-%M-%S")
                    timeStamp = int(time.mktime(timeArray))
                elif "分钟前" in currenttime:
                    print '分钟前'
                    currenttime = currenttime.replace("分钟前", "")
#                     timeStamp = int(time.mktime(datetime.datetime.now() - datetime.timedelta(minutes=string.atoi(currenttime))))
                    timeStamp = int(time.mktime(time.strptime((datetime.datetime.now() - datetime.timedelta(minutes=string.atoi(currenttime))).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")))
#                 timeArray = time.strptime(currenttime, "%Y-%m-%d-%H-%M-%S")
#                 timeStamp = int(time.mktime(timeArray))
                else:
                    print "else"
                    timeStamp = 1453513417
                dqsj = int(time.mktime(datetime.datetime.now().timetuple()))#<= current time
                if(timeStamp<=dqsj):
                    infofile.write(username[i].text.replace('\'', '') + ' ')
                    infofile.write(content[i].text.replace(' ', '').replace('|', '').replace('\\', '').replace('\'', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\b', '') + ' ')
                    infofile.write(repost[4 * i + 1].text + ' ')
                    infofile.write(repost[4 * i + 2].text + ' ')
                    infofile.write(str(timeStamp) + '\r\n')
                i = i + 1
            j = j + 1
            time.sleep(20)

    except Exception, e:      
        print "Error: ", e
    finally:    
        print '获取博文信息'
        print '**********************************************\n'

        
    
if __name__ == '__main__':

    # 定义变量
    username = '1207467967@qq.com'  # 输入你的用户名
    password = '1207467967qq'  # 输入你的密码

    # 操作函数
    LoginWeibo(username, password)  # 登陆微博
    
    
    
    GetTopic()
    
    time.sleep(20)
#     infofile = codecs.open("hottopic.txt", 'w', 'utf-8')
    hotlist = codecs.open("hotlist.txt", 'r', 'utf-8')
    # 搜索热点微博
    key = hotlist.readline().rstrip('\r\n')
    while key != "":
        GetComment(key)
        key = hotlist.readline().rstrip('\r\n') 
    
    
    hotlist.close()
    infofile.close()
    driver.close()
    

