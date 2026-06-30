from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd


# open browser 
driver = webdriver.Chrome()
# options = Options()



driver.get("https://www.livinginsider.com/searchword/Home/all/1/%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B9%80%E0%B8%9E%E0%B8%A5%E0%B8%B4%E0%B8%99%E0%B8%88%E0%B8%B4%E0%B8%95.html")

time.sleep(3) 

#pull data
house_info = driver.find_elements(By.CLASS_NAME,"item-desc")

data = {
    "ads" : [],
    "rent_price" : [],
    "sell_price" : [],
    "area" : [],
    "floors" : [],
    "bedrooms" : [],
    "bathrooms" : [],
}
# 4.store each data
for text in house_info:
    #kosana
    ads_info = text.find_element(By.CLASS_NAME,"text-title-card")
    data["ads"].append(ads_info.text)
    
    #price
    price = text.find_elements(By.CLASS_NAME,"text_price")
    rent_value = "-"
    sell_value = "-"
    for pri in price:
        if "/ด" in pri.text:
            rent_value = pri.text[1:]
        else:
            sell_value = pri.text[1:]
    data["sell_price"].append(sell_value)
    data["rent_price"].append(rent_value)
    
    #area
    area = text.find_element(By.CLASS_NAME,"card-prop-area-row")
    area_value = area.find_element(By.CLASS_NAME,"card-prop-value")
    data["area"].append(area_value.text)
    
    #floors bedrooms bathrooms
    floors_val = "-"
    bedrooms_val = "-"
    bathrooms_val = "-"
    
    else_info = text.find_elements(By.CLASS_NAME,"card-prop-item")
    has_bedroom_filled = False 
    
    for info in else_info:
        info_value = info.text.strip()
        if "ตร.ม." in info_value:
            continue  
        
        elif "ชั้น" in info_value:
            nums = re.findall(r'\d+', info_value)
            if nums:
                floors_val = int(nums[0])

        elif "ห้อง" in info_value:
            nums = re.findall(r'\d+', info_value)
            if nums:
                num = int(nums[0])
               
                if not has_bedroom_filled:
                    bedrooms_val = num
                    has_bedroom_filled = True
                else:
                    bathrooms_val = num
    data["floors"].append(floors_val)
    data["bedrooms"].append(bedrooms_val)
    data["bathrooms"].append(bathrooms_val)

# for i in data :
#     print(i,len(data[i]))

df = pd.DataFrame(data)
print(df)



# ปิดเบราว์เซอร์
driver.quit()