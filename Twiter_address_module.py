#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd

import time
import config
import pandas as pd
import helper_functions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(executable_path=r"E:\\chrome driver\\chromedriver.exe",options=options)
url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
driver.get(url)
time.sleep(1)

driver.find_element_by_id('username').send_keys(config.USERNAME)


time.sleep(1)

driver.find_element_by_id('password').send_keys(config.PASSWORD)


time.sleep(1)

driver.find_element_by_class_name('login__form_action_container ').click()

if __name__=="__main__":
    # Read csv
    linkedin_people=pd.read_csv('unique_instances_data.csv', index_col=False)
# taking final data csv and gettings urls from that
# try part says that if there are urls that are already done ignore them and continue onwards
# except start from the first url
    try:
        final_data = pd.read_csv('Final_Data.csv', index_col=False)
        done_urls = list(final_data['LinkedIn URL'])
        done_already_exists = True

    except:
        done_urls = []
        done_already_exists = False

    all_names=[]
    all_positions = []
    all_employers=[]
    all_locations=[]
    all_linkedin_profiles=[]
    all_twitters=[]
    all_addresses=[]
    all_exp1=[]
    all_exp2=[]
    all_exp3=[]
    all_exp4=[]
    all_exp1_dur=[]
    all_exp2_dur=[]
    all_exp1_loc=[]
    all_exp2_loc=[]

    # Go over every url and get twitter and address data
    for index, row in linkedin_people.iterrows():
        Name=row['Name']
        Position=row['Position']
        Employer=row['Employer at']
        Location=row['Location']
        LinkedIn_Profile_URL=row['LinkedIn Profile URL']
        if LinkedIn_Profile_URL in done_urls:
            continue
#         visiting urls one by one
        driver.get(LinkedIn_Profile_URL)
        time.sleep(5)
#         clicks on more info tab 
        info = driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']")
        info.click()
        time.sleep(2)
#         driver.execute_script("window.scrollTo(0, 2500)") 
#         time.sleep(2)
#       scraping exerience 
#         try:
#             experience_element = driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")
#             if experience_element:
#                 ex1 = experience_element[0].find_element_by_tag_name('h3')
#                 exp1 = ex1.text.strip()
#                 print('exp1: ' ,exp1)

#                 try:
#                     ex2 = experience_element[1].find_element_by_tag_name('h3')
#                     if ex2:
#                         exp2 = ex2.text.strip()
#                         print('exp2: ' ,exp2)
#                 except:
#                     exp2 = 'N/A'
#                     print('exp2: ' ,exp2)

#                 try:
#                     ex3 = experience_element[2].find_element_by_tag_name('h3')
#                     if ex3:
#                         exp3 = ex3.text.strip()
#                         print('exp3: ' ,exp3)
#                 except:
#                     exp3 = 'N/A'
#                     print('exp3: ' ,exp3)

#                 try:
#                     ex4 = experience_element[3].find_element_by_tag_name('h3')
#                     if ex4:
#                         exp4 = ex4.text.strip()
#                         print('exp4: ' ,exp4)
#                 except:
#                     exp4 = 'N/A'
#                     print('exp4: ' ,exp4)
#         except:
#             print('no experience')
#             exp1 = 'N/A'
#             exp2 = 'N/A'
#             exp3 = 'N/A'
#             exp4 = 'N/A'
#         driver.refresh()
#         info = driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']")
#         info.click()
#         time.sleep(2)
# scraping twitter handle
        
#     extract address of the user if available
        try:
            address = driver.find_element_by_xpath("//section[@class='pv-contact-info__contact-type ci-address']//a")

            if address:
                adr = address.get_attribute('text')
                print(adr)
        except:
            adr = 'N/A'
            print(adr)

        time.sleep(1)
#         print("=============================")
        exp1 = 'N/A'
        exp2 = 'N/A'
        exp3 = 'N/A'
        exp4 = 'N/A'
        exp1_dur='N/A'
        exp2_dur='N/A'
        exp1_loc='N/A'
        exp2_loc='N/A'

#         extracts twitter handle if available
        
        try:
            twitter = driver.find_element_by_xpath("//section[@class='pv-contact-info__contact-type ci-twitter']//a")

            if twitter:
                twit = twitter.get_attribute('href')
                print(twit)
                time.sleep(2)
                driver.get(LinkedIn_Profile_URL)
#                 driver.refresh()
#                 print('here')
                time.sleep(4)
                helper_functions.scroll_down_page(driver, speed=30)
#                 driver.execute_script("window.scrollTo(0, 2500)")
                time.sleep(3)
#             if twitter handle is found then extracting experience
                try:
                    experience_element = driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")
                    
                    if experience_element:
                        ex1 = experience_element[0].find_element_by_tag_name('h3')
                        exp1 = ex1.text.strip()
                        if exp1=="Company Name":
                            ex1 = experience_element[0].find_elements_by_xpath("//div[@class='pv-entity__company-summary-info']//span")[1]
                            exp1=ex1.text.strip()
                            
                        ex1_dur=experience_element[0].find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")[0]
                        exp1_dur=ex1_dur.text.strip()
                        ex1_loc=experience_element[0].find_elements_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']//span")[1]
                        exp1_loc=ex1_loc.text.strip()

                        print('exp1: ' ,exp1)
                        print('exp1_dur: ',exp1_dur)
                        print('exp1_loc: ',exp1_loc)
                        

                        try:
                            ex2 = experience_element[1].find_element_by_tag_name('h3')
                            if ex2:
                                exp2  = ex2.text.strip()
                                if exp2=="Company Name":
                                    ex2 = experience_element[1].find_elements_by_xpath("//div[@class='pv-entity__company-summary-info']//span")[1]
                                    exp2=ex2.text.strip()
                                ex2_dur=experience_element[1].find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")[1]
                                exp2_dur=ex2_dur.text.strip()
                                ex2_loc=experience_element[1].find_elements_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']//span")[3]
                                exp2_loc=ex2_loc.text.strip()
                                print('exp2: ' ,exp2)
                                print('exp2_dur: ',exp2_dur)
                                print('exp2_loc: ',exp2_loc)
                               
                        except:
                            exp2 = 'N/A'
                            print('exp2: ' ,exp2)

                        try:
                            ex3 = experience_element[2].find_element_by_tag_name('h3')
                            if ex3:
                                exp3 = ex3.text.strip()
                                print('exp3: ' ,exp3)
                        except:
                            exp3 = 'N/A'
                            print('exp3: ' ,exp3)

                        try:
                            ex4 = experience_element[3].find_element_by_tag_name('h3')
                            if ex4:
                                exp4 = ex4.text.strip()
                                print('exp4: ' ,exp4)
                        except:
                            exp4 = 'N/A'
                            print('exp4: ' ,exp4)
                except:
                    print('no experience')
#                     exp1 = 'N/A'
#                     exp2 = 'N/A'
#                     exp3 = 'N/A'
#                     exp4 = 'N/A'
#             driver.refresh()
#             info = driver.find_element_by_xpath("//a[@data-control-name='contact_see_more']")
#             info.click()
#             time.sleep(2)
        except:
            twit = 'N/A'

# scrapping address

#         try:
#             address = driver.find_element_by_xpath("//section[@class='pv-contact-info__contact-type ci-address']//a")

#             if address:
#                 adr = address.get_attribute('text')
#                 print(adr)
#         except:
#             adr = 'N/A'
        
#         time.sleep(1)
#         print("=============================")
        
# appending details into their respective lists
        all_names.append(Name)
        all_employers.append(Employer)
        all_addresses.append(adr)
        all_positions.append(Position)
        all_linkedin_profiles.append(LinkedIn_Profile_URL)
        all_locations.append(Location)
        all_twitters.append(twit)
        all_exp1.append(exp1)
        all_exp2.append(exp2)
        all_exp3.append(exp3)
        all_exp4.append(exp4)
        all_exp1_dur.append(exp1_dur)
        all_exp2_dur.append(exp2_dur)
        all_exp1_loc.append(exp1_loc)
        all_exp2_loc.append(exp2_loc)
        all_data = pd.DataFrame({
            "Name":all_names,
            "Employer":all_employers,
            "Position":all_positions,
            "LinkedIn URL":all_linkedin_profiles,
            "Twitter":all_twitters,
            "Address":all_addresses,
            "Experience_1":all_exp1,
            "Experience1_loc":all_exp1_loc,
            "Experience1_dur":all_exp1_dur,
            "Experience_2":all_exp2,
            "Experience2_loc":all_exp2_loc,
            "Experience2_dur":all_exp2_dur,
            "Experience_3":all_exp3,
            "Experience_4":all_exp4
            

        })
        if done_already_exists:
            all_data.to_csv('Final_Data.csv', mode='a', header=False, index=False)
        else:
            all_data.to_csv('Final_Data.csv', index=False)
    # Save new csv


# In[166]:


try:
    experience_element = driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")
    
    if experience_element:
        print('here')
        ex1 = experience_element[0].find_element_by_tag_name('h3')
        exp1 = ex1.text.strip()
        ex1_dur=experience_element[0].find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")[0]
        exp1_dur=ex1_dur.text.strip()
        ex1_loc=experience_element[0].find_elements_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']//span")[1]
        exp1_loc=ex1_loc.text.strip()

        print('exp1: ' ,exp1)
        print('exp1_dur: ',exp1_dur)
        print('exp1_loc: ',exp1_loc)
        try:
            ex2 = experience_element[1].find_element_by_tag_name('h3')
            if ex2:
                exp2  = ex2.text.strip()
                ex2_dur=experience_element[1].find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")[1]
                exp2_dur=ex2_dur.text.strip()
                ex2_loc=experience_element[1].find_elements_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']//span")[3]
                exp2_loc=ex2_loc.text.strip()
                print('exp2: ' ,exp2)
                print('exp2_dur: ',exp2_dur)
                print('exp2_loc: ',exp2_loc)
        except:
            exp2 = 'N/A'
            print('exp2: ' ,exp2)

        try:
            ex3 = experience_element[2].find_element_by_tag_name('h3')
            if ex3:
                exp3 = ex3.text.strip()
                print('exp3: ' ,exp3)
        except:
            exp3 = 'N/A'
            print('exp3: ' ,exp3)

        try:
            ex4 = experience_element[3].find_element_by_tag_name('h3')
            if ex4:
                exp4 = ex4.text.strip()
                print('exp4: ' ,exp4)
        except:
            exp4 = 'N/A'
            print('exp4: ' ,exp4)
except:
    print('no experience')


# In[162]:


driver.find_elements_by_xpath("//h4[@class='pv-entity__location t-14 t-black--light t-normal block']//span")[1].text.strip()


# In[139]:


exp1_loc


# In[174]:


driver.find_elements_by_xpath("//div[@class='pv-entity__company-summary-info']//span")[1].text.strip()


# In[9]:


import helper_functions
helper_functions.scroll_down_page(driver, speed=30)


# In[ ]:




