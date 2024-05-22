import os
import pandas as pd
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure Loguru: setting up logging configuration to log to a file with rotation, retention, and logging level
logger.add("poem_app.log", rotation="500 MB", retention="10 days", level="INFO")


class Scraper:
    def __init__(self):
        # Initialize Selenium WebDriver and other variables
        self.chrome_options = (
            Options()
        )  # Create an instance of 'Options' class for Chrome browser
        self.chrome_options.add_argument(
            "-incognito-"
        )  # Add argument to run Chrome in incognito mode
        self.poem = []  # Initialize an empty list to store poem data

    def scrape(self, urls, dest):
        for url in urls:  # Loop through the list of URLs
            try:
                driver = webdriver.Chrome(
                    options=self.chrome_options
                )  # Create an instance of Chrome WebDriver with specified options
                driver.implicitly_wait(5)  # Set implicit wait time to 5 seconds
                wait = WebDriverWait(
                    driver, WAIT_TIMEOUT
                )  # Create WebDriverWait object with specified timeout

                driver.get(url)  # Open the URL in the browser

                # Get writer's name and other static elements
                writer_element = driver.find_element(
                    By.XPATH, "/html/body/div[5]/div[2]/div/header/h1"
                )  # Find writer's name element using XPath
                writer_name = (
                    writer_element.text.strip()
                )  # Get the text of the writer's name and remove leading/trailing whitespaces

                poetry_collection_xpath_tags = '//*[@class="poem-group-title"]'  # XPath for identifying poetry collection titles
                poetry_collection_tags = driver.find_elements(
                    By.XPATH, poetry_collection_xpath_tags
                )  # Find all poetry collection elements
                num_poetry_collection_tags = len(
                    poetry_collection_tags
                )  # Count the number of poetry collection elements
                logger.info(
                    "Number of poetry collection tags: {}", num_poetry_collection_tags
                )  # Log the number of poetry collection elements

                if (
                    num_poetry_collection_tags == 0
                ):  # Check if no poetry collection titles found
                    logger.info(
                        "No poetry collection titles found. Moving to the next URL."
                    )  # Log that no poetry collection titles found and move to next URL
                    continue  # Continue to the next URL

                for idx in range(
                    len(poetry_collection_tags)
                ):  # Loop through each poetry collection
                    poetry_collection_title_xpath = f"/html/body/div[5]/div[2]/div/h4[{idx+1}]/a"  # XPath for each poetry collection title
                    poetry_collection_title = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, poetry_collection_title_xpath)
                        )
                    ).text  # Wait for the presence of the poetry collection title and get its text
                    logger.info(
                        "Poetry collection title: {}", poetry_collection_title
                    )  # Log the poetry collection title

                    content_xpath = f"/html/body/div[5]/div[2]/div/div[{6+idx}]/ol/li"  # XPath for the content of each poetry collection
                    content_tags = driver.find_elements(
                        By.XPATH, content_xpath
                    )  # Find all content elements within the current poetry collection

                    # Add variable to track if poem_title exists or not
                    has_poem_title = False  # Initialize a flag to track if a poem title is found or not

                    for index, content_tag in enumerate(
                        content_tags, start=1
                    ):  # Loop through each content tag
                        poem_title_xpath = f"/html/body/div[5]/div[2]/div/div[{6+idx}]/ol/li[{index}]/a"  # XPath for each poem title within the current content

                        try:
                            poem_title_element = wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, poem_title_xpath)
                                )
                            )  # Wait for the presence of poem title element
                            poem_title = (
                                poem_title_element.text
                            )  # Get the text of the poem title
                            poem_url = poem_title_element.get_attribute(
                                "href"
                            )  # Get the URL of the poem
                            has_poem_title = (
                                True  # Set flag to True if poem title found
                            )
                        except Exception as e:
                            logger.warning(
                                "An error occurred while getting poem title: {}", e
                            )  # Log warning if error occurs while getting poem title
                            continue  # Continue to next iteration

                        logger.info(
                            "Title: {}, URL: {}", poem_title, poem_url
                        )  # Log the poem title and its URL

                        try:
                            driver.get(poem_url)  # Open the URL of the poem

                            poem_src_xpath = '//div[@class="small"]'  # XPath for the source of the poem

                            poem_content_tag = wait.until(
                                EC.presence_of_element_located(
                                    (By.CLASS_NAME, "poem-content")
                                )
                            )  # Wait for the presence of poem content element

                            try:
                                poem_content_i_tag = poem_content_tag.find_element(
                                    By.TAG_NAME, "i"
                                )  # Find <i> tags in poem content
                                driver.execute_script(
                                    self.deletion_script, poem_content_i_tag
                                )  # Execute script to delete <i> tags
                            except:
                                pass  # If <i> tags not found, continue without raising an exception

                            try:
                                poem_content_b_tag = poem_content_tag.find_element(
                                    By.TAG_NAME, "b"
                                )  # Find <b> tags in poem content
                                driver.execute_script(
                                    self.deletion_script, poem_content_b_tag
                                )  # Execute script to delete <b> tags
                            except:
                                pass  # If <b> tags not found, continue without raising an exception

                            poem_content = (
                                poem_content_tag.text
                            )  # Get the text content of the poem

                            try:
                                poem_src_tag = wait.until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, poem_src_xpath)
                                    )
                                )  # Wait for the presence of poem source element
                                poem_src = (
                                    poem_src_tag.text
                                )  # Get the text of the poem source
                            except:
                                poem_src = ""  # If poem source not found, assign an empty string

                            poem_info = (
                                {  # Create a dictionary containing poem information
                                    "Title": poem_title,
                                    "Content": poem_content,
                                    "Poetry Collection": poetry_collection_title,
                                    "URL": poem_url,
                                    "Writer": writer_name,
                                }
                            )
                            self.poem.append(
                                poem_info
                            )  # Append poem information to the poem list
                            logger.info(
                                "Poem Info: {}", poem_info
                            )  # Log the poem information
                            driver.back()  # Navigate back to the previous page

                        except Exception as e:
                            logger.error(
                                "An error occurred: {}", e
                            )  # Log error if any exception occurs while scraping poem

                    # Check if poem_title exists after iterating through all content_tags
                    if not has_poem_title:  # If no poem title found
                        logger.info(
                            "No poem title found in this poetry collection. Moving to the next one."
                        )  # Log that no poem title found in current poetry collection
                        continue  # Continue to next poetry collection

                logger.info(
                    "Finished scraping poems from URL: {}", url
                )  # Log that scraping poems from current URL finished

            except TimeoutException:
                logger.error(
                    "Timeout occurred while scraping URL {}. Closing the window.".format(
                        url
                    )
                )  # Log timeout error while scraping URL
            except WebDriverException:
                logger.error(
                    "WebDriverException occurred while scraping URL {}. Closing the window.".format(
                        url
                    )
                )  # Log WebDriverException error while scraping URL
            finally:
                try:
                    driver.quit()  # Quit the WebDriver instance
                except UnboundLocalError:
                    pass  # If WebDriver instance not found, continue without raising an exception

            self.save_to_csv(dest)  # Save poem information to CSV file

    def save_to_csv(self, dest):
        df = pd.DataFrame.from_dict(self.poem)  # Create a DataFrame from the poem list
        if os.path.exists(dest):  # Check if the destination CSV file already exists
            df.to_csv(
                dest, mode="a", index=False, header=True
            )  # Append DataFrame to existing CSV file without writing headers again
        else:
            df.to_csv(
                dest, mode="w", index=False, header=True
            )  # Write DataFrame to new CSV file with headers


if __name__ == "__main__":
    WAIT_TIMEOUT = 60  # Define a constant for wait timeout
    scraper = Scraper()  # Create an instance of Scraper class
    POEM_URLS = [  # List of URLs to scrape poems from
        "https://www.thivien.net/Nguy%E1%BB%85n-Phong-Vi%E1%BB%87t/author-Hu_jFQUEWR8VnFyLZ7zdEw",
        "https://www.thivien.net/Nguy%E1%BB%85n-Thi%C3%AAn-Ng%C3%A2n/author-5eeALBFvrxrBL3c-Vsvn4w",
        "https://www.thivien.net/L%C6%B0u-Quang-V%C5%A9/author-WpRofb64NUUZVCwLGK-ucg",
        "https://www.thivien.net/Xu%C3%A2n-Qu%E1%BB%B3nh/author-uAY7gIaARbh2b4DCVporPQ",
        "https://www.thivien.net/Xu%C3%A2n-Di%E1%BB%87u/author-RFLL7QmxIAtjETgw2z9Z4w",
        "https://www.thivien.net/Nguy%E1%BB%85n-Nh%E1%BA%ADt-%C3%81nh/author-mYEcs2AZA6uARv-MA69oaA",
        "https://www.thivien.net/H%C3%A0n-M%E1%BA%B7c-T%E1%BB%AD/author-mz8hO4-xm_bQYO5dbc_rLg",
        "https://www.thivien.net/Nguy%E1%BB%85n-L%C3%A3m-Th%E1%BA%AFng/author-BMkQRdDALat1QVkZh01GPg",
        # Add more URLs here if needed
    ]
    dest = "./dataset/vietnamese_poem_dataset.csv"  # Destination path for CSV file
    scraper.scrape(
        POEM_URLS, dest
    )  # Call scrape method to start scraping poems from specified URLs and save to CSV file
