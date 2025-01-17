import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def get_info_dict(driver):
    # info table part
    info_table = driver.find_element(By.CSS_SELECTOR, ".infolist")
    info_element = info_table.find_elements(By.TAG_NAME, "li")
    info_lst = info_table.text.split("\n")

    info_lst = [info.text for info in info_element]
    final_info_lst = []
    for i in info_lst:
        if len(i.split("\n")) == 1:
            single_el = i.split("\n")
            single_el.append("EMPTY")
            final_info_lst.append(single_el)
        else:
            final_info_lst.append(i.split("\n"))

    final_info_lst = np.array(final_info_lst).flatten()
    return dict(zip(final_info_lst[0::2], final_info_lst[1::2]))


def get_tables(driver, moblist):
    table = driver.find_element(By.CSS_SELECTOR, moblist)

    rank_lst = table.find_elements(By.TAG_NAME, "tr")
    time_table = table.find_elements(By.CSS_SELECTOR, ".time.ar")
    info_table = driver.find_element(By.CSS_SELECTOR, ".infolist")
    info_element = info_table.find_elements(By.TAG_NAME, "li")
    name_lst = []
    time_lst = []

    for rank in rank_lst:
        if len(rank.text.split("\n")) > 2:
            name_lst.append(rank.text.split("\n")[1])

    for k, t in enumerate(time_table):
        if k > 0:
            time_lst.append(t.text)

    info_lst = [info.text for info in info_element]

    return [name_lst, time_lst, info_lst]


def get_tables_ttt(driver, moblist_ttt):
    try:
        table = driver.find_element(By.CLASS_NAME, moblist_ttt)
        main_list = [
            [time.text for time in table.find_elements(By.CSS_SELECTOR, "tr.team")],
            [],
            [],
        ]

    except NoSuchElementException:
        print("Nothing in TTT list.")
        main_list = [[], [], []]

    return main_list
    # find_elements(By.CSS_SELECTOR, "team").text


# time_table = table.find_elements(By.CSS_SELECTOR, ".time.ar")
# info_table = driver.find_element(By.CSS_SELECTOR, ".infolist")
# info_element = info_table.find_elements(By.TAG_NAME, "li")
# name_lst = []
# time_lst = []

# for rank in rank_lst:
#     if len(rank.text.split("\n")) > 2:
#         name_lst.append(rank.text.split("\n")[1])

# for k, t in enumerate(time_table):
#     if k > 0:
#         time_lst.append(t.text)

# return [name_lst, time_lst, info_element]
