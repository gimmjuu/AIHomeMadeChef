"""
Detail : 만개의 레시피에서 레시피 썸네일 이미지 경로를 크롤링합니다.
"""
import time

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class Recipe:
    def __init__(self):
        super().__init__()

        self.df = pd.read_excel("./recipe_list.xlsx")
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.10000recipe.com/")

        self.recipe_id = self.df['RECIPE_ID'].tolist()
        self.recipe_name_list = self.df['RECIPE_NM'].tolist()
        self.link_list = list()

        search_box = self.driver.find_element(By.XPATH, '//*[@id="srhRecipeText"]')
        for name in self.recipe_name_list:
            search_box.send_keys(name)
            search_box.send_keys(Keys.ENTER)
            btn = self.driver.find_element(By.XPATH, '//*[@id="contents_area_full"]/ul/div/ul/li[1]/a').click()
            wait = WebDriverWait(self.driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="srhRecipeText"]')))
            search_box.clear()

            img_element = self.driver.find_element(By.XPATH, '//*[@id="contents_area_full"]/ul/ul/li[1]/div[1]/a/img')
            img_src = img_element.get_attribute('src')

            self.link_list.append(img_src)

        for id, nm, thumb in zip(self.recipe_id, self.recipe_name_list, self.link_list):
            print(id, nm, thumb)

        data = {
            'RECIPE_ID': self.recipe_id,
            'RECIPE_NM': self.recipe_name_list,
            'RECIPE_THUMB': self.link_list
        }

        df = pd.DataFrame(data)
        df.to_csv('recipe.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    Recipe()
    