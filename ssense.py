import httpx
import re
from bs4 import BeautifulSoup
import time
import csv
import os



csv_name_new = "./csv/数据.csv"
if os.path.exists(csv_name_new):
    print("文件存在，不创建！！！")
else:
    with open(csv_name_new, 'w', encoding='utf-8-sig', newline="") as f:
        pass
    print("文件创建！！！")


def get_ip():
    return ip



def get_page_one(page_one_url,ip_ip):
    # "https://www.ssense.com/ja-ca/men/clothing?page=2"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "gdprCountry=false; visitorId=bf286774f740d0e4577e23c74d04fefce309b53c391167108111672b12caf281; exp_mobile_nav_filter3=false; exp_pdp_last_image_cta=variant_b; exp_nav_recent_designer=variant_b; isp=cnservers llc; pxcts=447bec3a-7066-11ed-8cd8-466772786272; _pxvid=42f784ef-7066-11ed-bd73-4d4848616e4a; preferredLanguage=ja; _gcl_au=1.1.1551362442.1669782021; SSP_AB_876878223=control; sid=9d0e9438317b05f111580fcda27658d3; lang=ja_JP; country=CA; _fbp=fb.1.1669782021570.1084193823; shopping_bag=6386da066b0389f3bdf6ca39; _gid=GA1.2.1958474695.1669782023; ab.storage.deviceId.e352e6f5-ea92-41e0-be85-df1e6a76e0b7=%7B%22g%22%3A%225987d00f-367a-836d-95bc-9ff4ea062693%22%2C%22c%22%3A1669782023974%2C%22l%22%3A1669782023974%7D; rskxRunCookie=0; rCookie=w0iosa5z9carvnf4f5jzaqlb353rni; _pin_unauth=dWlkPU9UQmtOelE1TW1RdFlUaGtZaTAwWkdRNUxUbGhNVE10Tm1OaE4yTmhZbUV5TVdRNA; wcs_bt=s_15f8bbc72b9c:1669784628; _ga_3L9QF4WT0T=GS1.1.1669782020.1.1.1669784628.59.0.0; _sp_id.c6c8=5dee447b-5692-4cbc-90ec-19b692c408e7.1669782021.1.1669784630.1669782021.690a5e81-ed11-4bc6-9b80-1785b7ea425d; _ga=GA1.2.235854816.1669782021; ab.storage.sessionId.e352e6f5-ea92-41e0-be85-df1e6a76e0b7=%7B%22g%22%3A%22b73021f3-8830-617b-8728-6370d95687ac%22%2C%22e%22%3A1669786429784%2C%22c%22%3A1669782023971%2C%22l%22%3A1669784629784%7D; _pxhd=ge1eN5KX2OTPQzxSJzQGtdgNkpzi/mLh89BR65O1zJVVVED1Bxbh1wvP6zO-sf91JP6TOsaOkbA-NoyyYqdSfQ==:uXQNyoOg1NAAdabmcx-ymjGdTKL/Sd1VawYnWscYQQKmETeefXYo4LjjcR8QtdAZgb/mFRN3i7qvhqo6iTC6ft0A6xRTElM3r00nZBZuOi4=; lastRskxRun=1669784630874; __cf_bm=zc7ZfatPYxthyAOgVn14lIpkqbdoOFcG.He28h1epTM-1669789373-0-Ac9KZpCcZXDQ9asPk3d/ysOaapcNUKEOiIkxLuxzjjh2KsZjgEBnShry1oGcd7xvIa8Yj3EdHfaUmN+YSdjdS2k=; _px2=eyJ1IjoiNTM5MTI2NzAtNzA2Ni0xMWVkLThhN2UtYzU1Njk0ZGU2NzFlIiwidiI6IjQyZjc4NGVmLTcwNjYtMTFlZC1iZDczLTRkNDg0ODYxNmU0YSIsInQiOjE2Njk3OTAyMTQxMTIsImgiOiI0ZjdiOWIwZGRhYjA1YjY5Y2ExZDViZDlhYWIxNjRlNDRkZjhkMjJiMmJmYjlkNTExMzZkNzk5MDcxNDY5MjZkIn0=; _dd_s=rum=0&expire=1669790874086&logs=1&id=a441b98a-257a-46f6-b247-083c52ff1afe&created=1669789924011",
        "referer": "https://www.ssense.com/ja-ca/men/clothing",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4564.0 Safari/537.36"
    }
    proxies = {'http://': 'http://'+ip_ip, 'https://': 'http://'+ip_ip}

    page_one_html = httpx.get(page_one_url, headers=headers, proxies=proxies)
    print(page_one_html)
    page_one_txt = BeautifulSoup(page_one_html.text, "html.parser")
    div_products__row = page_one_txt.select_one("div.plp-products__row")
    div_products__column_s = div_products__row.select("div.plp-products__column")
    detail_list = []
    for div_a_s in div_products__column_s:
        a = "https://www.ssense.com" + div_a_s.select_one("a").get("href")
        print(a)
        detail_list.append(a)
    return detail_list


def get_detail(z_url,url,detail_ip):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "gdprCountry=false; visitorId=bf286774f740d0e4577e23c74d04fefce309b53c391167108111672b12caf281; exp_mobile_nav_filter3=false; exp_pdp_last_image_cta=variant_b; exp_nav_recent_designer=variant_b; isp=cnservers llc; pxcts=447bec3a-7066-11ed-8cd8-466772786272; _pxvid=42f784ef-7066-11ed-bd73-4d4848616e4a; preferredLanguage=ja; _gcl_au=1.1.1551362442.1669782021; SSP_AB_876878223=control; _sp_ses.c6c8=*; sid=9d0e9438317b05f111580fcda27658d3; lang=ja_JP; country=CA; _fbp=fb.1.1669782021570.1084193823; shopping_bag=6386da066b0389f3bdf6ca39; _gid=GA1.2.1958474695.1669782023; ab.storage.deviceId.e352e6f5-ea92-41e0-be85-df1e6a76e0b7=%7B%22g%22%3A%225987d00f-367a-836d-95bc-9ff4ea062693%22%2C%22c%22%3A1669782023974%2C%22l%22%3A1669782023974%7D; rskxRunCookie=0; rCookie=w0iosa5z9carvnf4f5jzaqlb353rni; _pin_unauth=dWlkPU9UQmtOelE1TW1RdFlUaGtZaTAwWkdRNUxUbGhNVE10Tm1OaE4yTmhZbUV5TVdRNA; __cf_bm=RG3CHweRi.gECXTo3rxVb_FYKQqsO.me4hTD4ZrK4tw-1669783973-0-AYMh/8bATn/t70AUe203Iy2jegARWOmXsaKepX1FFZgveWgntc2qvQmVrLxIDwtxDXW16l6C96vq/Z22JYcrjvI=; wcs_bt=s_15f8bbc72b9c:1669784119; _ga_3L9QF4WT0T=GS1.1.1669782020.1.1.1669784119.59.0.0; _sp_id.c6c8=5dee447b-5692-4cbc-90ec-19b692c408e7.1669782021.1.1669784120.1669782021.690a5e81-ed11-4bc6-9b80-1785b7ea425d; _pxhd=ge1eN5KX2OTPQzxSJzQGtdgNkpzi/mLh89BR65O1zJVVVED1Bxbh1wvP6zO-sf91JP6TOsaOkbA-NoyyYqdSfQ==:uXQNyoOg1NAAdabmcx-ymjGdTKL/Sd1VawYnWscYQQKmETeefXYo4LjjcR8QtdAZgb/mFRN3i7qvhqo6iTC6ft0A6xRTElM3r00nZBZuOi4=; _ga=GA1.2.235854816.1669782021; lastRskxRun=1669784120536; ab.storage.sessionId.e352e6f5-ea92-41e0-be85-df1e6a76e0b7=%7B%22g%22%3A%22b73021f3-8830-617b-8728-6370d95687ac%22%2C%22e%22%3A1669785920616%2C%22c%22%3A1669782023971%2C%22l%22%3A1669784120616%7D; _px2=eyJ1IjoiMzAxMzM0OTAtNzA2Yi0xMWVkLWE1ODItNGRmOTMxYzdlZTlkIiwidiI6IjQyZjc4NGVmLTcwNjYtMTFlZC1iZDczLTRkNDg0ODYxNmU0YSIsInQiOjE2Njk3ODQ5MDIxNDYsImgiOiJlNzAxMWI2OTk3OTkwYzhiNDBmNmM4ZGM3MjdjZTRiN2NkYWRmODUwMzUzY2EzMjJjMWY1Y2UyOTFiYzJiZDc4In0=; _dd_s=rum=0&expire=1669785521395&logs=1&id=b88b17af-5a94-427b-acc9-43849e79d9c7&created=1669782020694&lock=d0c81607-837f-4930-9295-64fd855350b8",

        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4564.0 Safari/537.36"
    }
    proxies = {'http://': 'http://'+detail_ip, 'https://': 'http://'+detail_ip}
    a = httpx.get(url, headers=headers, proxies=proxies)
    print(a)
    a_html = BeautifulSoup(a.text, "html.parser")
    scripct = str(a_html.select_one("div.pdp__redesign.view"))
    productID = re.findall('"productID":(.*?),', scripct)[-1]
    name = re.findall('"name": "(.*?)",', scripct)[-1]
    sku = re.findall('"sku": "(.*?)"', scripct)[-1]
    name_two = re.findall('"name": "(.*?)"', scripct)[-1]
    price = re.findall('"price":(.*?),', scripct)[-1]
    priceCurrency = re.findall('"priceCurrency": "(.*?)",', scripct)[-1]
    availability = re.findall('"availability": "(.*?)",', scripct)[-1]
    url_shop = re.findall('"url": "(.*?)"', scripct)[-1]
    description = re.findall('"description": "(.*?)",', scripct)[-1]
    image = re.findall('"image": "(.*?)"', scripct)[-1]

    data = [productID, name, sku, name_two, price,
            priceCurrency, availability,
            url_shop, description, image]
    print(z_url)
    print(len(data), "======", data)
    with open(csv_name_new, 'a', encoding='utf-8-sig', newline="") as f_c:
        writer = csv.writer(f_c)
        writer.writerow(data)
    print("===========")
    time.sleep(1)


def bgen():
    k = int(input("输入开始页面："))
    for i in range(k,416+1):
        global page_url
        if i == 1:
            page_url = "https://www.ssense.com/ja-ca/men/clothing"
        else:
            page_url = "https://www.ssense.com/ja-ca/men/clothing?page="+str(i)
        while True:
            try:
                g_ip = get_ip()
                u_list = get_page_one(page_url, g_ip)
                print(u_list)
                break
            except:
                # duration = 1000  # millisecond
                # freq = 1600  # Hz
                # winsound.Beep(freq, duration)
                for i in range(11):
                    time.sleep(2)
                    print('\r当前进度：{0}{1}%'.format('▉' * i, (i * 10)), end='')
                print()
        f_w = open("爬过.txt", "r", encoding="utf-8")
        f_w_list = f_w.readlines()
        f_w.close()
        for u in u_list:
            if (u + "\n") not in f_w_list:
                while True:
                    try:
                        get_detail(page_url, u, g_ip)
                        time.sleep(1)
                        break
                    except:
                        # duration = 1000  # millisecond
                        # freq = 1600  # Hz
                        # winsound.Beep(freq, duration)
                        print("有问题！！！")
                        for i in range(11):
                            time.sleep(2)
                            print('\r当前进度：{0}{1}%'.format('▉' * i, (i * 10)), end='')
                        print()
                with open("爬过.txt", "a", encoding="utf-8") as ff:
                    ff.write(u + "\n")
            else:
                print(u, "====爬虫过了，跳过！！！")

bgen()


# get_page_one("https://www.ssense.com/ja-ca/men/clothing?page=2","127.0.0.1:1080")