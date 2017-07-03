from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse
import time
import pymysql as m
c = None

url = "http://www.chongoodhome.com/home_cheaper_million.php?page=1&home_id=&zone_id=2&type_id=12&price=#"
urls = "http://www.chongoodhome.com/"
url_testcut = "http://www.chongoodhome.com/home_frame_image.php?id=2176&images=2176-P2162337"
html  = requests.get(url).content
count =0
soup = BeautifulSoup(html, "html.parser")




navs = soup.find_all('a', {'class': 'mynavi'})
for nav in navs:
    new_url = 'http://www.chongoodhome.com/home_cheaper_million.php' + nav['href']
    #print('หน้า')
    #print(new_url)
    #print(new_url)
   ## print('-----------------')
    new_html = requests.get(new_url).content
    new_soup = BeautifulSoup(new_html, "html.parser")



    brhtml = new_soup.select('a[href^="home_detail"]')
    brhtml1 = new_soup.select('a[href$="=new"]')


    for b in brhtml1:


        try:
            new_in = urls + b['href']
            news = requests.get(new_in).content
            new_s = BeautifulSoup(news, "html.parser")
            #print(new_in)
            iframe = new_s.find_all('iframe', {'height': '2000'})
            for f in iframe:
                url_iframe = urls + f['src']
                newlast = requests.get(url_iframe).content
                new_last = BeautifulSoup(newlast, "html.parser")

                pikud = new_last.iframe['src']
                parsed = urlparse.urlparse(pikud)
                lat = (urlparse.parse_qs(parsed.query)['lat'][0])
                lng = (urlparse.parse_qs(parsed.query)['lng'][0])
                x = new_last.get_text()
                y = x.split()
                home = y[269]
                type = y[266]
                numsell = 270
                numadree = 266
                mudjom = 266
                bank = 266
                ponehome = 266
                sleeproom = 300
                toiroom = 300
                contact = 'คุณนิด : 086-345-8811'
                map = 'บ้านเลขที่ '  # map = y[275] + " " + y[276] + " " + y[277] + " " + y[278]

                while y[numadree] != 'บ้านเลขที่':  # หาจุดเริ่มบ้านเลขที่
                    numadree = numadree + 1

                numadree = numadree + 2  # หาจุดเริ่มบ้านเลขที่

                while y[numadree] != 'ราคาขาย':  # นำบ้านเลขที่มาต่อกับที่อยู่ทั้งหมด
                    map = map + y[numadree] + " "
                    numadree = numadree + 1

                while y[numsell] != 'ราคาขาย':  # หาราคาขาย
                    numsell = numsell + 1

                while y[mudjom] != 'วางมัดจำ':  # หาคำว่าวางมัดจำ
                    mudjom = mudjom + 1

                while y[bank] != 'กู้ธนาคารได้':  # หาคำว่าู้ธนาคารได้
                    bank = bank + 1

                while y[ponehome] != 'ผ่อนประมาณ' and y[ponehome] != 'รายละเอียด':  # หาคำว่าูบาท/เดือน
                    ponehome = ponehome + 1

                while y[sleeproom] != 'ห้องนอน' and y[sleeproom] != 'การเดินทางและสถานที่ใกล้เคียง':  # หาคำว่าูห้องนอน
                    sleeproom = sleeproom + 1

                while y[toiroom] != 'ห้องน้ำ' and y[toiroom] != 'การเดินทางและสถานที่ใกล้เคียง':  # หาคำว่าูห้องนอน

                    toiroom = toiroom + 1

                if y[sleeproom] == 'ห้องนอน':
                    sleeproom = sleeproom - 1
                else:
                    y[sleeproom] = '0'
                if y[toiroom] == 'ห้องน้ำ':
                    toiroom = toiroom - 1
                else:
                    y[toiroom] = '0'

                if y[ponehome] == 'ผ่อนประมาณ':
                    ponehome = ponehome + 2
                else:
                    y[ponehome] = '0'

                if type == 'บ้านเดี่ยว':
                   type = 1
                if type == 'ทาวน์เฮาส์':
                    type = 2
                if type == 'อาคารพาณิชย์':
                    type = 3
                if type == 'คอนโด' or type == 'สถานที่ตั้ง':
                    type = 4
                if type == 'บ้านแฝด':
                    type = 5
                if type == 'ที่ดินเปล่า' or type == 'เนื้อที่':
                    type = 6

                sumtoiroom = y[toiroom]
                sumsleeproom = y[sleeproom]
                sumponehome = y[ponehome]
                sumbank = y[bank + 2]
                summudjom = y[mudjom + 2]
                sell = y[numsell + 2]
                ctime = time.ctime()


                print("ชื่อสถานที่ = " + home)
                print(type)
                print("พิกัดละติจูด = " + lat)
                print("พิกัดลองจิจูด = " + lng)
                print("สถานที่ตั้ง = " + map)
                print("ราคามัดจำ = " + summudjom)
                print("กู้ธนาคารได้ = " + sumbank)
                print("ผ่อนประมาณเดือนละ = " + sumponehome)
                print("ห้องนอน = " + sumsleeproom)
                print("ห้องน้ำ = " + sumtoiroom)
                print("ราคารวม = " + sell)
                print("ติดต่อสอบถาม = " + contact)
                print("ลิ้งอ้างอิง = " + new_in)
                print(ctime)
                print("-------------------------------------------------------------------")
                #print("รูปภาพ")

                c = m.connect(host='localhost', user='root', passwd='1234', db='db_gmap', charset='utf8mb4')
                cur = c.cursor()
                cur.execute('SET NAMES utf8;')
                sql = "SELECT * FROM tbl_location"
                sql = sql.encode('utf-8')
                cur.execute(sql)
                results = cur.fetchall()
                i = 0
                name_home = []
                for row in results:
                    name_home.append(row[10])
                for row in results:
                    if name_home[i] != home:
                        sumsimi = '0'
                    else:
                        sumsimi = '1'
                        break
                    i = i + 1
                if sumsimi == '0':
                    c = m.connect(host='localhost', user='root', passwd='1234', db='db_gmap', charset='utf8mb4')
                    cur = c.cursor()
                    cur.execute('SET NAMES utf8;')
                    sql = "INSERT INTO `tbl_location` (`id`,`lat`,`lng`,`location`,`deposit`,`borrower`,`installment`,`bedroom`,`toilet`,`total_price`,`location_name`,`type_local`,`contact`,`new_url`,`time_map`) \
                          VALUE (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (lat,lng,map,summudjom,sumbank,sumponehome,sumsleeproom,sumtoiroom,sell,home,type,contact,new_in,ctime)
                    sql = sql.encode('utf-8')
                    cur.execute(sql)
                    try:
                        c.commit()
                        print('เพื่มข้อมูล เรียบร้อยแล้ว')
                    except:
                        c.rollback()
                        print("เพ่ิ่มข้อมูล ผิดพลาด")
        except m.Error:
            print("ติดต่อฐานข้อมูลผิดพลาด")

                #for link in new_last.select(('a[href$="(Custom).JPG"]')):
                 #   print("www.chongoodhome.com/" + link.get('href').replace(' ', ''))


                #print("-------------------------------------------------------------------")


        except KeyError as e:
            print('I got a KeyError - reason '+ str(e))

        except (RuntimeError, TypeError, NameError):
            ...
            pass







