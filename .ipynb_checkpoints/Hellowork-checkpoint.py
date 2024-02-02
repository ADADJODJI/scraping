from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # le button entrer
import pandas as pd
from tqdm import tqdm
import time
import requests
from bs4 import BeautifulSoup


url= "https://www.hellowork.com/fr-fr/"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# naviger sur la page
driver.get(url)

# Sélectionner la barre de recherche
search_input = driver.find_element(by=By.NAME,value="k")

# element de recherche
search_input.send_keys("data science")

time.sleep(2)

# Button entrer
search_input.send_keys(Keys.RETURN)

# temps d'attente
time.sleep(5)






# Définir l'expression XPath pour le bouton "Continuer sans accepter"
continue_button_xpath = '//button[@id="hw-cc-notice-continue-without-accepting-btn"]'

continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, continue_button_xpath))
    )

    

    # Cliquer sur le bouton "Continuer sans accepter"
continue_button.click()

# Définir l'expression XPath pour l'élément <li>

xpath_expression = '//li[@class="next"]'

# Attendre que l'élément soit cliquable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath_expression))
)

# Cliquer sur l'élément
element.click()
time.sleep(5)



def page_link():

#"""avoir les lins sur une page"""

    # pour stoker les lien
    link= []
        # Définir l'expression XPath
    css_expression = '.offer--content .offer--maininfo h3 a'

    # Attendre la présence des éléments avant de les récupérer
    job_links = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_expression))
    )
    # Utiliser les liens d'emploi récupérés
    for job_link in job_links:
        lien_offre = job_link.get_attribute('href')
        link.append(lien_offre)
    
    return link

def change_page():
    # Définir l'expression XPath pour l'élément <li>

    xpath_expression = '//li[@class="next"]'

    # Attendre que l'élément soit cliquable
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_expression))
    )

    # Cliquer sur l'élément
    element.click()
    time.sleep(2)


def get_all_link(nb_page):

    link=[]

    for _ in tqdm(range(1,nb_page), desc='Getting link on page'):

        link.extend(page_link())
        # next page
        change_page()
    
    return link

# Fermez le navigateur après avoir terminé


# Get link data  specify the number of page to get
link_data = get_all_link(4)

driver.quit()

# sauvegarder les lien
#df = pd.DataFrame({
#    "Lien":link_data})

#df.to_csv(r'C:\Users\33753\Desktop\PYLAB\Algorithm\hellowork_data1.csv', index=False, encoding='utf-8')



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_job(url):

    # Fetch the HTML content from the URL with headers
    response = requests.get(url, headers=headers)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Use find method to select the desired span element

    # job tittle
    job_title_span = soup.find('span', {'class': 'tw-block tw-typo-xl sm:tw-typo-3xl tw-mb-2', 'data-cy': 'jobTitle'})
    # company name
    company_name_span = soup.find('span', {'class': 'tw-contents tw-typo-m tw-text-grey'})

    # Location and job type
    spans = soup.find_all('span', {'class': 'tw-inline-flex tw-typo-m tw-text-grey'})
    job_type_span = spans[1].text
    location_span = spans[0].text


    Salary = soup.find('li', {'class': 'tw-tag-attractive-s tw-readonly'})

    # Check if Salary is not None before further processing
    if Salary is not None:
        Salary = Salary.text.strip()
        Salary = Salary.replace('\u202f', '')
    else:
        Salary = None


    Date = soup.find('span', {'class': 'tw-block tw-typo-xs tw-text-grey tw-mt-3 tw-break-words'})
    Date = Date.text.strip()
    Date= Date.split(' ')
    Date= Date[2]


    # Find the <p> element by its class name
    paragraph_element = soup.find('p', class_='tw-typo-long-m')

    # Extract text from the <p> element
    paragraph_text = paragraph_element.get_text(strip=True)

    return job_title_span.text, company_name_span.text,Salary,location_span, paragraph_text,Date
        


def get_infos(data_link):
    # Initialize lists to store individual pieces of information
    job_titles = []
    company_names = []
    job_types = []
    salaries = []
    locations = []
    job_descriptions = []

    # Iterate through each URL in the provided list
    for url in tqdm(data_link, desc='processing link'):
        # Call the get_job function to extract information from the current URL
        infos = get_job(url)

        # Append the extracted information to the respective lists
        job_titles.append(infos[0])
        company_names.append(infos[1])
        job_types.append(infos[5])
        salaries.append(infos[2])
        locations.append(infos[3])
        job_descriptions.append(infos[4])

    # Create a dictionary with the collected information
    data = {
        'Job Title': job_titles,
        'Company Name': company_names,
        'Job Type': job_types,
        'Salary': salaries,
        'Location': locations,
        'Job Description': job_descriptions,
        'lien':link_data
    }

    # Convert the dictionary into a DataFrame using pandas
    df = pd.DataFrame(data)

    # Return the DataFrame
    return df


df= get_infos(link_data)

df.to_csv(r'C:\Users\33753\Desktop\PYLAB\Algorithm\hellowork_data3.csv', index=False, encoding='utf-8')

df.head(10)