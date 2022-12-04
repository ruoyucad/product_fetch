import random
import requests
import cfscrape
from lxml import etree
import csv
import re
import json
import time
import pandas as pd
from google.cloud import bigquery
count = 280

username = 'sp46364524'
password = '!Angelo778899'
proxy = f'http://{username}-sessionduration-1:{password}@us.smartproxy.com:10007'
table_id = "buymamanagement.buyma_ruoyu.guess_data"



all_id = []
all_size = []
all_color = []
all_old_price = []
all_new_price = []
all_name = []
all_description = []
all_image_str = []

#  获取页面源代码
def get_url_source(url = 'https://www.guess.com/ca/en/men/apparel/view-all?start=0&sz=10'):


    scraper = cfscrape.create_scraper()
    # 请求报错，可以加上时延
    #scraper = cfscrape.create_scraper(delay = 10)
    # 获取网页源代码
    web_data = scraper.get(url,
                    proxies={'http': proxy}).text
    return web_data

#  解析页面源代码
def parse_data(resp):
    global count
    tree = etree.HTML(resp)  # xpath解析源代码
    href_list = tree.xpath('//*[@class="product-tile__main-link"]/@href')

    for href in href_list:
        print(f'开始下载第{count}个商品信息！！！')
        id = href.split('/')[-1].split('.')[0]
        resp = get_url_source(href)
        tree = etree.HTML(resp)

        color_div = tree.xpath('//*[@class="flex-wrap d-flex align-items-center"]/button')
        if not color_div:
            colors = tree.xpath('//*[@class="js-selected-color sentence-case--span"]/text()')[0]
        else:
            colors = []
            for button in color_div:
                color = button.xpath('./@aria-label')[0]
                colors.append(color.split('Color')[1].strip())
            colors = '|'.join(colors)

        sizes = []
        size1 = tree.xpath('//select[@id="size-1"]/option')
        for option in size1[1:]:
            size = option.xpath('./text()')[0]
            sizes.append(size.replace('\n', ''))
        sizes = '|'.join(sizes)
        print(colors)
        print(sizes)

        old_price = tree.xpath('//span[@class="value"]/text()')
        old_price = ''.join(old_price).strip()
        print(old_price)

        new_price = tree.xpath('//span[@class="value price__value price__value--sale"]/text()')
        if not new_price:
            new_price = ''
        else:
            new_price = new_price[0].split('\n')[2]
        print(new_price)

        try:
            description = tree.xpath('//*[@id="description-1"]/text()')[0].strip().replace('\n', '')
        except IndexError as e:
            description = ''
            pass

        print(description)

        try:
            name = tree.xpath('//*[@class="product-name product-detail__name text--semibold mt-2 mt-md-0 mb-0"]/text()')[0].strip()
        except IndexError as e:
            name = ''
            pass
        print(name)

        obj = re.findall(r'ld\+json">(.*?)</script>', resp, re.S)[0].strip().replace('\n', '')
        dic = json.loads(obj)['image']

        image_str = '|'.join(dic)
        print(image_str)
        #row = [id, name, old_price, new_price, sizes, colors, description, image_str]
        #write_csv(row)
        all_id.append(id)
        all_size.append(sizes)
        all_color.append(colors)
        all_old_price.append(old_price)
        all_new_price.append(new_price)
        all_name.append(name)
        all_description.append(description)
        all_image_str.append(image_str)

        print(f'成功下载完第{count}个商品信息！！！')
        count += 1
        time.sleep(2)


def write_csv(row):
    file_path = f'new_goods.csv'
    with open(file_path, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)


if __name__ == '__main__':
    resp = get_url_source()
    href_list = parse_data(resp)
    
    print('全部下载完毕！！！')

    guess_data = pd.DataFrame(
    {'id': all_id,
     'size': all_size,
     'color': all_color,
     'old_price': all_old_price,
     'new_price': all_new_price,
     'name': all_name,
     'description': all_description,
     'image_str': all_image_str,

    })
    # set GOOGLE_APPLICATION_CREDENTIALS env var to the json location
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    schema=[
        # Specify the type of columns whose type cannot be auto-detected. For
        # example the "title" column uses pandas dtype "object", so its
        # data type is ambiguous.
        bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("size", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("color", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("old_price", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("new_price", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("description", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("image_str", bigquery.enums.SqlTypeNames.STRING),

    ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
    )

    job = client.load_table_from_dataframe(
    guess_data, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
