

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # le button entrer
from selenium.webdriver.chrome.options import Options
import pandas as pd
from tqdm import tqdm
import time
# Initialize WebDriver for Chrome in headless mode
chrome_options = Options()
chrome_options.headless = True



url = 'https://fr.indeed.com/'


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# naviger sur la page
driver.get(url)

time.sleep(2)

# Find the input element by ID
search_input = driver.find_element_by_id("text-input-what")

# Enter a search term
search_input.send_keys("Data Scientist")

time.sleep(2)

# Press Enter to submit the search
search_input.send_keys(Keys.RETURN)

# Optional: Wait for a few seconds to see the result
time.sleep(2)


def get_url_date_page(): 

    # Find all elements with the class name "jcs-JobTitle"
    elements = driver.find_elements_by_class_name("jcs-JobTitle")

    date_span = driver.find_elements_by_class_name("date")

    return elements , date_span

def get_pages(nb_page):

    urls= []
    dates= []

    for _ in tqdm(range(1, nb_page), desc="Processing pages"):
        
        first= get_url_date_page()
        
        for url in first[0] :
            urls.append(url.get_attribute("href"))

        for date in first[1]: 
            
            dates.append( date)

        # Find the element by CSS selector
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page_button = driver.find_element_by_css_selector("li.css-227srf.eu4oa1w0 a[data-testid='pagination-page-next']")

        # Click on the element
        next_page_button.click()

        time.sleep(5)
        driver.quit()
    return urls, dates

def get_infos(url):

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get(url)

    # Find the job title element by class name
    job_title_element = driver.find_element_by_class_name("jobsearch-JobInfoHeader-title")

    # Extract the text content from the element
    job_title = job_title_element.text.strip()

    # Find the company name element by CSS selector
    company_element = driver.find_element_by_css_selector('div[data-company-name="true"] span a')

    # Extract the text content from the element
    company_name = company_element.text.strip()

    # Find the job type element by CSS selector
    #job_type_element = driver.find_element_by_css_selector('ul.js-match-insights-provider-1czx045 li.js-match-insights-provider-10zb82q')

    # Extract the text content from the element
    #job_type = job_type_element.text.strip()

    # Find the salary element by CSS selector
    salary_element = driver.find_element_by_css_selector('div.js-match-insights-provider-tvvxwd')

    # Extract the text content from the element
    salary_text = salary_element.text.strip()

    # Find the location element by CSS selector
    location_element = driver.find_element_by_css_selector('div[data-testid="jobsearch-JobInfoHeader-companyLocation"] span')

    # Extract the text content from the element
    location_text = location_element.text.strip()

    # Find the job description element by XPath
    description_element = driver.find_element_by_css_selector('div#jobDescriptionText div')

    # Extract the text content from the element
    job_description = description_element.text.strip()
    driver.quit()
    return {
        "Job Title": job_title,
        "Company Name": company_name,
        #"Job Type": job_type,
        "Salary": salary_text,
        "Location": location_text,
        "Job Description": job_description
    }

# Optional: Wait for a few seconds to see the result
time.sleep(5)

data = get_pages(nb_page= 2)

job_titles = []
company_names = []
#job_types = []
salaries = []
locations = []
job_descriptions = []

for url in tqdm(data[0], desc='looping'):

    job_info = get_infos(url)
    
    # Append the results to the respective lists
    job_titles.append(job_info["Job Title"])
    company_names.append(job_info["Company Name"])
    #job_types.append(job_info["Job Type"])
    salaries.append(job_info["Salary"])
    locations.append(job_info["Location"])
    job_descriptions.append(job_info["Job Description"])

# Create a DataFrame from the lists
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company Name": company_names,
    #"Job Type": job_types,
    "Salary": salaries,
    "Location": locations,
    "Job Description": job_descriptions
})

# Write the DataFrame to a CSV file
df.to_csv('job_data.csv', index=False)


#element = driver.find_element_by_class_name("jcs-JobTitle")

# Get the id attribute value
# element_url = element.get_attribute("href")

# # Print the id value
# print("href:", element_url)


# Fermez le navigateur après avoir terminé
#driver.quit()
