import http
import pickle
import string
from urllib.parse import quote
from urllib.request import urlretrieve

import pandas
import os

import requests
from selenium.common.exceptions import NoSuchElementException
import tqdm
from time import sleep
from selenium import webdriver

PREFIX = "photo"

dd = dict()


def load_data():
    data = pandas.read_excel("45861706_0_华南理工大学第三十届研究生会招新报名表_659_659.xls")
    for item in data.itertuples(index=False):
        yield {
            "index": getattr(item, "序号"),
            "name": getattr(item, "_6"),
            "area": getattr(item, "_10"),
            "school": getattr(item, "_11"),
            "first": getattr(item, "_13"),
            "second": getattr(item, "_14"),
            "photo": getattr(item, "_18"),
            "desc_pdf": getattr(item, "_20"),
        }


def down_load_photo(data, driver):
    if not os.path.exists(PREFIX):
        os.mkdir(PREFIX)
    for dd in tqdm.tqdm(data):
        if dd['photo'] == "(空)":
            continue
        file_name = f"{dd['name']}_{dd['area']}_{dd['school']}_{dd['first']}_{dd['second']}"
        url = dd['photo']
        if "," in url:
            urls = url.split(",")
            for i in urls:
                _down_load_photo(file_name, i)
        else:
            _down_load_photo(file_name, url)

        sleep(0.1)


def rename_photo(data):
    for dd in tqdm.tqdm(os.listdir("D:\Project\Independent_project\downLoadwjx\photo")):# type:str
        index = dd.split(".")[0].split("_")[0]
        ext = dd.split(".")[-1]
        this_name = os.path.join("D:\Project\Independent_project\downLoadwjx\photo", dd)
        name_file = data[int(index) - 1]
        print(f"file index is {index} and data_file index is {name_file['index']}")
        file_name = f"{name_file['index']}_{name_file['name']}_{name_file['area']}_{name_file['school']}_{name_file['first']}_{name_file['second']}"
        rename_name = os.path.join("D:\Project\Independent_project\downLoadwjx\photo", f"{file_name}.{ext}")
        print(f"rename {this_name} to {rename_name}")
        os.rename(this_name,rename_name)


# def _down_load_photo(file_name, url):
#     try:
#         driver.get(url)
#     except Exception as e:
#         print("filed url is %s" % url)
#         print(e)
#     sleep(0.4)


def login(driver):
    driver.get(
        "https://www.wjx.cn/Login.aspx?returnUrl=%2fnewwjx%2fmanage%2fmyquestionnaires.aspx%3frandomt%3d1570015757")
    driver.find_element_by_xpath('//*[@id="UserName"]').send_keys("18663278150")
    driver.find_element_by_xpath('//*[@id="Password"]').send_keys("715903657412")
    driver.find_element_by_xpath('//*[@id="LoginButton"]').click()
    try:
        driver.find_element_by_xpath('//*[@id="AntiSpam1_txtValInputCode"]')
        input("输入验证码继续")
    except NoSuchElementException as e:
        pass


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(file_path, x)))
        # print(dir_list)
        # for i in dir_list:
        #     print(os.path.getctime(os.path.join(file_path,i)))
        return dir_list


if __name__ == '__main__':
    # options = webdriver.ChromeOptions()
    # prefs = {'profile.default_content_settings.popups': 0,
    #          'download.default_directory': 'D:\\Project\\Independent_project\\downLoadwjx\\photo'}
    # options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(chrome_options=options)
    # login(driver)
    # down_load_photo(load_data(), driver)
    # with open("fff.data", "wb") as f:
    #     pickle.dump(dd, f)
    rename_photo(list(load_data()))
