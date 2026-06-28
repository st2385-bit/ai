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
    # "bedrooms" : [],
    # "bathrooms" : [],
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
    else_info = text.find_elements(By.CLASS_NAME,"card-prop-item")
    has_bedroom_filled = False 
    
    for info in else_info:
        info_value = info.text.strip()
        if "ตร.ม." in info_value:
            continue  
        
        if "ชั้น" in info_value:
            # ใช้ re.findall ดึงเฉพาะตัวเลข เช่น "2 ชั้น" -> 2
            floors_num = re.findall(r'\d+', info_value)
            if floors_num:
                data["floors"].append(int(floors_num[0]))
        # elif "ห้อง" in info_value:
        #     rooms_num = re.findall(r'\d+', info_value)
        #     if rooms_num:
        #         num = int(rooms_num[0]) # ได้ตัวเลขจำนวนห้อง เช่น 4
            
        #     # เช็กว่า ข้อมูล "ห้องนอน" ของบ้านหลังนี้ถูกใส่ไปหรือยัง?
        #     if not has_bedroom_filled:
        #         data["bedrooms"].append(num)      # ใส่ในช่องห้องนอน
        #         has_bedroom_filled = True         # เปิดสวิตช์บอกว่าใส่ห้องนอนแล้วนะ
        #     else:
        #         data["bathrooms"].append(num)     # ตัวถัดมาใส่ในช่องห้องน้ำ
        #         has_bedroom_filled = False

# for i in data :
#     print(i,len(data[i]))

df = pd.DataFrame(data)
print(df)



# ปิดเบราว์เซอร์
driver.quit()