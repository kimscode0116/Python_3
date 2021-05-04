#!/usr/bin/env python
# coding: utf-8

# # 1. 라이브러리 선언

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup 
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# # 2. 웹 드라이브 설정

# In[3]:


options = webdriver.ChromeOptions()
options.add_argument("window-size=1920*1080")
driver_loc = "../midterm/addon/chromedriver/chromedriver.exe" ## 제출전 경로확인
driver = webdriver.Chrome(executable_path=driver_loc,options=options)

targetUrl = "https://store.musinsa.com/app/"
driver.get(targetUrl)


# # 3. 브라우저 내 액션

# In[4]:


##검색창에 마우스 커서클릭
searchXpath = "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/form/input[2]"
searchClick = driver.find_element_by_xpath(searchXpath)
searchClick.click() 

##셔츠 키워드 검색
musinsaSearch = driver.find_element_by_xpath(searchXpath)
searchKeyword = "셔츠"
musinsaSearch.send_keys(searchKeyword)
musinsaSearch.send_keys(Keys.ENTER)

##상품 카테고리 커서 올리기
categoryXpath = "/html/body/div[2]/div[2]/div[1]/div/nav/div[1]/div[2]/ul[2]/li[1]/a"
click = driver.find_element(By.XPATH, categoryXpath)
webdriver.ActionChains(driver).move_to_element(click).perform()

## 셔츠/블라우스 카테고리 선택
categoryTouch = driver.find_element_by_xpath(categoryXpath)
driver.execute_script("arguments[0].click();", categoryTouch)


# # 4. 웹 크롤링(beautifulSoup)

# In[5]:


targetUrl = driver.current_url ## page_source로 html소스 확인가능
resp = requests.get(url=targetUrl)
resp.encoding="utf-8"
html = resp.text
htmlObj = BeautifulSoup(html, "html.parser")

allNameList = htmlObj.findAll(name = "p",attrs={"class":"list_info"})
allPriceList = htmlObj.findAll(name = "p",attrs={"class":"price"})
allbrandList = htmlObj.findAll(name = "p",attrs={"class":"item_title"})

brandList = []
nameList = []
priceList = []

for i in range(0,len(allNameList)):
    product = allNameList[i].find(name="a")
    productName = product.attrs["title"]
    priceName = allPriceList[i].text.split("\n")[1].replace("                                ","").split(" ")[1]
    brandName = allbrandList[i].text
    
    brandList.append(brandName)
    nameList.append(productName)
    priceList.append(priceName)

answer = pd.DataFrame(zip(brandList,nameList,priceList),columns=["브랜드명","제품명","가격"])

## csv 파일 생성
answer.to_csv("./musinsa_shirtsList.csv", index=False, encoding="ms949")


# # 5. smtp를 이용한 메일 발송

# In[11]:


## 비밀번호 보안을 위한 pickle library 사용
import pickle
userpw = "ujscgdstmpaylnjk"

with open('pw.pickle', 'wb') as handle:
    pickle.dump(userpw, handle, pickle.HIGHEST_PROTOCOL)

with open('pw.pickle', 'rb') as handle:
    pwpickle = pickle.load(handle)

## smtp library 사용
import smtplib
from email.message import EmailMessage

smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)
smtp_gmail.ehlo()
smtp_gmail.starttls()

userid = "eunhye3576@gmail.com"
smtp_gmail.login(userid,pwpickle)

## 이메일 리스트
emailData = pd.read_csv("./emailList.csv")
to = emailData.email.tolist()

## 제목 및 메일내용 작성
msg=EmailMessage()
msg['Subject']="무신사 셔츠/블라우스 카테고리 상품정보 리스트"
msg.set_content("무신사 쇼핑몰 셔츠/블라우스 카테고리입니다.")
msg['From']='eunhye3576@gmail.com'
msg['To'] = 'eunhye3_3@naver.com'

## sv 파일첨부
file='musinsa_shirtsList.csv'
fp = open(file,'rb')
file_data=fp.read()
msg.add_attachment(file_data,
                  maintype='text',
                  subtype='plain',
                  filename=file)

## mail 발송
smtp_gmail.send_message(msg)
smtp_gmail.close()


# In[ ]:




