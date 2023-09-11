import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import csv
import pandas as pd


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(os.environ.get("TARGET_URL"))
    # driver.get('https://play.pakakumi.com/')
    # iteration_count = 0
    # max_iterations = 20
    wait = WebDriverWait(driver, 30)
    column_names = [
        "time_now",
        "num_active_players",
        "num_logged_in_not_playing",
        "highest_bet_in_game",
        "burst",
    ]
    previous_burst = None
    burst_change_count = 0

    with open("data_4.csv", "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
    while True:
        # while iteration_count <= 100:
        try:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            burst_element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='css-xy3rl8']/a[1]")
                )
            )
            burst = burst_element.text
            if burst != previous_burst:
                num_active_players_element = driver.find_element(
                    By.XPATH,
                    "//div[@class='css-cyjiju'][span[text()='Playing']]/strong",
                )
                num_active_players = num_active_players_element.text
                num_logged_in_not_playing_element = driver.find_element(
                    By.XPATH, "//div[@class='css-cyjiju'][span[text()='Online']]/strong"
                )
                num_logged_in_not_playing = num_logged_in_not_playing_element.text
                try:
                    highest_bet_in_game_element = driver.find_element(
                        By.XPATH, "//div[@class='css-u718rw']//tbody/tr[1]//td[3]/div"
                    )
                    highest_bet_in_game = highest_bet_in_game_element.text
                except NoSuchElementException:
                    highest_bet_in_game = "N/A"
                # if iteration_count == 0:
                #   with open('data_3.csv', 'a', newline='') as csvfile:
                #       csvwriter = csv.writer(csvfile)
                #       csvwriter.writerow(column_names)
                with open("data_4.csv", "a", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(
                        [
                            time_now,
                            num_active_players,
                            num_logged_in_not_playing,
                            highest_bet_in_game,
                            burst,
                        ]
                    )
                previous_burst = burst
                burst_change_count += 1

            # if burst_change_count >= 30:
            #    break
            time.sleep(3)

        except Exception as e:
            print(f"an error occured: {str(e)}")
        driver.quit()


if __name__ == "__main__":
    main()
