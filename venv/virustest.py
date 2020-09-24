from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

fp = webdriver.FirefoxProfile()

#fp.set_preference('browser.download.lastDir', r"C:\test")
# 设置下载时不提示是否要开始下载
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", r"D:\test")
fp.set_preference('browser.download.manager.showWhenStarting', False)
# 指定要下载的文件类型，可以去 HTTP Content-type对照表查询，这里指定的是.exe文件
fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

with webdriver.Firefox(firefox_profile=fp) as driver:
    driver.get('https://www.icourse163.org/learn/HENANNU-1003544138?tid=1003773132#/learn/content')
    driver.maximize_window()
    driver.implicitly_wait(10)
    # 滚动条到底，加载网页内容
    driver.execute_script('window.scrollTo(100, document.body.scrollHeight);')
    sleep(3)
    # 这里driver 点击元素操作有点问题



    #ele = driver.find_element_by_link_text('文档下载')
    #ele = driver.find_elements_by_class_name('u-icon-doc')
    #titles = driver.find_elements_by_class_name("j-titleName name f-fl f-thide")
    h3eles = driver.find_elements_by_tag_name("h3")
    for i in range(len(h3eles)):
        if (i != 0 and i <= 10):
            h3eles[i].click()
    #driver.execute_script('arguments[0].click();', ele)
    eles = driver.find_elements_by_class_name('u-icon-doc')
    for i in range(len(eles)):
        eles[i].click()
        sleep(1)
        download = driver.find_element_by_link_text('文档下载')
        driver.execute_script('window.scrollTo(100, document.body.scrollHeight);')
        sleep(3)
        print(download.get_attribute("href"))
        driver.get(download.get_attribute("href"))
        download.send_keys(Keys.ENTER)
        sleep(100)
        #driver.back()
        driver.get('https://www.icourse163.org/learn/HENANNU-1003544138?tid=1003773132#/learn/content')
        sleep(3)
        h3eles = driver.find_elements_by_tag_name("h3")
        for i in range(len(h3eles)):
            if (i != 0 and i <= 10):
                h3eles[i].click()
        # driver.execute_script('arguments[0].click();', ele)
        #file = driver.find_element_by_class_name('u-icon-doc')

        eles = driver.find_elements_by_class_name('u-icon-doc')

        #file.click()

    #print(len(ele))

    sleep(10000)




#print(company)
'''url = 'https://www.tianyancha.com/search?key='
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
company = urllib.parse.quote("上海日钢物流有限公司")
fullurl = url + company
cookie = 'TYCID=dafe39b036a111eaba0ff19a8d077fcd; undefined=dafe39b036a111eaba0ff19a8d077fcd; ssuid=3895022467; _ga=GA1.2.601338959.1578987940; aliyungf_tc=AQAAAOvKZ3ULsQ0AWsRr2rPTpyWH3NDA; csrfToken=-uK08qzCyyXwwxf4QTzvw_MC; jsid=SEM-BAIDU-PZ0703-VIP-000001; bannerFlag=false; RTYCID=a19f53c7eeff436f9202a20974ff9247; CT_TYCID=0f0d5101192c4ffba60c02aa399b647a; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1597128431,1597131347; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522personalClaimType%2522%253A%2522none%2522%252C%2522integrity%2522%253A%252210%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522score%2522%253A%252215%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%2522129%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522showPost%2522%253Anull%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzExMDUwODM1MiIsImlhdCI6MTU5NzEzMTU3NSwiZXhwIjoxNjI4NjY3NTc1fQ.LYAJn2H2s-8WrPU2sy2CsvqOFPFy1v2bG-2pOBeYJ7jAJfNq9tCnjWDL4B9np_-BkkpQker90SKpEFEwMRTyQA%2522%252C%2522schoolAuthStatus%2522%253A%25222%2522%252C%2522scoreUnit%2522%253A%2522%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myTidings%2522%253A%25220%2522%252C%2522companyAuthStatus%2522%253A%25222%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E4%25B8%2581%25E4%25B8%258D%25E4%25B8%2589%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522bossStatus%2522%253A%25222%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522yellowDiamondEndTime%2522%253A%25220%2522%252C%2522yellowDiamondStatus%2522%253A%2522-1%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213110508352%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzExMDUwODM1MiIsImlhdCI6MTU5NzEzMTU3NSwiZXhwIjoxNjI4NjY3NTc1fQ.LYAJn2H2s-8WrPU2sy2CsvqOFPFy1v2bG-2pOBeYJ7jAJfNq9tCnjWDL4B9np_-BkkpQker90SKpEFEwMRTyQA; tyc-user-phone=%255B%252213110508352%2522%255D; cloud_token=4773b7f634dc4a61b709153b41368d08; token=6f42e95d95844bd0967071505051fb3e; _utm=403873a6393e4a67a8fd7ed933936e38; relatedHumanSearchGraphId=2944431047; relatedHumanSearchGraphId.sig=yHbcvSKSjiYbL9FDFzMR-iUbX6MKwRE1AD1JeXoqcSM; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1597132698'
headers = { 'User-Agent' : user_agent,'Cookie' : cookie }

req = urllib.request.Request(fullurl, headers = headers)
response = urllib.request.urlopen(req)
html = response.read()
html =html.decode("utf-8")

reg = r'<a.*?tyc-event-ch="CompanySearch.Company".*?href="(.*?)" target=\'_blank'  # 根据网站样式匹配的正则：(.*?)可以匹配所有东西，加括号为我们需要的
reg = re.compile(reg,re.DOTALL)
urls = re.findall(reg, html)#最匹配
print(urls[0])
req = urllib.request.Request(str(urls[0]), headers = headers)
detalil = urllib.request.urlopen(req)
html = detalil.read()
html =html.decode("utf-8")
reg = r'有帮助</a></div></div></div></td><td width="308px">(.*?)</td><td width="150px">工商注册号</td><td>(.*?)</td>'
reg1 = r'src="https://cdn.tianyancha.com/resources/images/icon_useful.png">有帮助</a></div></div></div></td><td colspan="2">(.*?)</td></tr><tr><td width="148px">公司类型</td><td width="308px">(.*?)</td>'
reg2 = r'电话：</span><span>(.*?)</span>'
reg3 = r'注册地址</td><td colspan="4">(.*?)<!--'
reg4 = r'<div class="humancompany"><div class="name"><a class="link-click".*?title="(.*?)".*?href'
reg = re.compile(reg,re.DOTALL)
reg1 = re.compile(reg1,re.DOTALL)
reg2 = re.compile(reg2,re.DOTALL)
reg3 = re.compile(reg3,re.DOTALL)
reg4 = re.compile(reg4,re.DOTALL)
gszc = re.findall(reg, html)#最匹配
test = re.findall(reg1,html)
phone = re.findall(reg2,html)
addr = re.findall(reg3,html)
person = re.findall(reg4,html)
print(test)
print(phone)
print(addr)
print(person)'''