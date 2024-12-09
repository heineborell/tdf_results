import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CyclingDataScraper:
    BASE_URL = "https://www.procyclingstats.com/race/tour-de-france"
    PROBLEMATIC_STAGES = [
        "Stage 14 | Metz - Dunkerque",
        "Stage 4 | Grenoble - Toulon",
        "Stage 4 | Toulouse - Bordeaux",
    ]

    def __init__(self):
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 5)
        self.results_df = pd.DataFrame(columns=["year", "stage", "name", "time"])
        self.info_df = pd.DataFrame()

    def _setup_driver(self) -> webdriver.Chrome:
        """Configure and return Chrome webdriver."""
        options = Options()
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = "eager"
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)

    def _get_year_list(self) -> List[str]:
        """Get list of available years."""
        self.driver.get(f"{self.BASE_URL}/2024/stage-11")
        drop_list = self.driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
        year_element = drop_list[0].find_elements(By.TAG_NAME, "option")
        return [year.text for year in year_element][1:]  # Skip first element

    def _get_stage_list(self, year: str) -> List[str]:
        """Get list of stages for a given year."""
        self.driver.get(f"{self.BASE_URL}/{year}/")
        time.sleep(2)
        drop_list = self.driver.find_elements(By.CLASS_NAME, "pageSelectNav ")

        # Handle different page layouts
        stage_element = (
            drop_list[1] if len(drop_list) == 2 else drop_list[2]
        ).find_elements(By.TAG_NAME, "option")
        stages = [stage.text for stage in stage_element if "Stage" in stage.text]

        # Remove problematic stages
        return [stage for stage in stages if stage not in self.PROBLEMATIC_STAGES]

    def _parse_race_table(self, table) -> Tuple[List[str], List[str]]:
        """Extract names and times from race results table."""
        rank_lst = table.find_elements(By.TAG_NAME, "tr")
        time_table = table.find_elements(By.CSS_SELECTOR, ".time.ar")

        names = [
            rank.text.split("\n")[1]
            for rank in rank_lst
            if len(rank.text.split("\n")) > 2
        ]
        times = [t.text for k, t in enumerate(time_table) if k > 0]

        return names, times

    def _convert_time_to_seconds(self, time_str: str) -> Optional[int]:
        """Convert time string to seconds."""
        if time_str == ",," or "-" in time_str:
            return None

        try:
            if "," not in time_str:
                format_str = "%H:%M:%S" if ":" in time_str else "%M:%S"
                t = datetime.strptime(time_str, format_str)
            else:
                stripped_time = time_str[: time_str.index(",")]
                t = datetime.strptime(stripped_time, "%M.%S")

            return int(
                timedelta(
                    hours=t.hour, minutes=t.minute, seconds=t.second
                ).total_seconds()
            )
        except ValueError:
            return None

    def _process_times(self, time_lst: List[str]) -> List[int]:
        """Process list of time strings into normalized seconds."""
        # Convert times to seconds
        processed_times = []
        base_time = None

        for time_str in time_lst:
            if time_str == ",,":
                processed_times.append(processed_times[-1] if processed_times else None)
                continue

            seconds = self._convert_time_to_seconds(time_str)
            if seconds is not None:
                if base_time is None:
                    base_time = seconds
                processed_times.append(
                    seconds + (0 if base_time is None else base_time)
                )
            else:
                processed_times.append(None)

        return processed_times

    def _process_info_table(self, info_element) -> Dict:
        """Process race information table."""
        info_lst = [info.text for info in info_element]
        processed_info = []

        for info in info_lst:
            if len(info.split("\n")) == 1:
                processed_info.append([info, "Na"])
            else:
                processed_info.append(info.split("\n"))

        flat_info = np.array(processed_info).flatten()
        return dict(zip(flat_info[0::2], flat_info[1::2]))

    def _save_data(self, final_dict: Dict, info_dict: Dict):
        """Save race data to CSV files."""
        self.results_df = pd.concat([self.results_df, pd.DataFrame(final_dict)])

        self.info_df = pd.concat(
            [self.info_df, pd.DataFrame({k: [v] for k, v in info_dict.items()})],
            ignore_index=True,
        )

        self.results_df.to_csv("protdf.csv")
        self.info_df.to_csv("infodf.csv")

    def _scrape_stage(self, year: str, stage: str):
        """Scrape data for a specific stage."""
        stage_num = stage.split(" ")[1]
        self.driver.get(f"{self.BASE_URL}/{year}/stage-{stage_num}")
        time.sleep(2)

        # Try different table formats
        for table_class in [
            ".results.basic.moblist12",
            ".results.basic.moblist11",
            ".results.basic.moblist10",
        ]:
            try:
                table = self.driver.find_element(By.CSS_SELECTOR, table_class)
                break
            except NoSuchElementException:
                continue
        else:
            # Check if it's a team time trial
            try:
                self.driver.find_element(By.CLASS_NAME, "results-ttt")
                print("It is a TTT stage")
                return
            except NoSuchElementException:
                print("No results table found")
                return

        # Parse race data
        name_lst, time_lst = self._parse_race_table(table)
        if not time_lst:
            print("No times found")
            return

        # Process times
        processed_times = self._process_times(time_lst)

        # Process info table
        info_table = self.driver.find_element(By.CSS_SELECTOR, ".infolist")
        info_element = info_table.find_elements(By.TAG_NAME, "li")
        info_dict = self._process_info_table(info_element)

        # Prepare final data
        final_dict = {
            "year": [int(year)] * len(name_lst),
            "stage": [stage] * len(name_lst),
            "name": name_lst,
            "time": processed_times,
            **{k: [v] * len(name_lst) for k, v in info_dict.items()},
        }

        self._save_data(final_dict, info_dict)

    def scrape_tour(self, years: Optional[List[str]] = None):
        """Main method to scrape Tour de France data."""
        try:
            year_list = years if years else self._get_year_list()

            for year in year_list:
                print(f"Processing year: {year}")
                stage_list = self._get_stage_list(year)

                for stage in stage_list:
                    print(f"Processing stage: {stage}")
                    self._scrape_stage(year, stage)
        finally:
            self.driver.quit()


def main():
    scraper = CyclingDataScraper()
    # Optional: Specify years to scrape
    # years_to_scrape = ["2023", "2022", "2021"]
    scraper.scrape_tour()


if __name__ == "__main__":
    main()
