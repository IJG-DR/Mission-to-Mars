#####################################################################
# The following code scrapes the most recent article, the teaser text, 
# the image associated with it, and facts about mars from two NASA url's. 
#####################################################################

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}

# Set URL and browser
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Search for elements with a specific combination of tag (div) and 
# attribute (list_text). Add an optional delay of 1 second in case
# the page is slow to load.
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')

#####################################################################
# SCRAPE THE TITLE OF THE MOST RECENT ARTICLE (FIRST ARTICLE)
#####################################################################

# Use select_one to only select the first item, as we only want
# the most recent Nasa article on the page.
# Use div.list_text to search for all 'div' tag with a class 'list_text'
slide_elem = news_soup.select_one('div.list_text')


# After opening the web page and using Inspector to explore 
# the most recent article, we identified that the title is in 
# class 'content_title'.

# look inside the slide_elem object for the specific title
slide_elem.find('div', class_='content_title')


# Clean the title of other html code. 
# Use the parent element to find the first `a` tag and 
# save it as `news_title`.
# This line is similar to the code above, but adds the 
# method "get_text()" to extract only the text from the html.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#####################################################################
# SCRAPE THE TEASER BODY 
#####################################################################

# After using Inspector on that element of
# the web page, we identied it is associated with class "article_teaser_body."
# Repurpose the above code to get it.
teaser = slide_elem.find('div', class_='article_teaser_body').get_text()
teaser

#####################################################################
# SCRAPE THE FEATURED IMAGES
#####################################################################

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


### WHY USE A [1] IF THERE ARE PREVIOUS 'button' INSTANCES IN THE INSPECTOR??
### THE PREVIOUS BUTTON IS FOR THE SEARCH BAR, IF YOUR USE [0], THAT ONE
### WILL BE SELECTED!!!

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


## After using Inspector on the full size image, we found its class.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image')
img_url_rel


# Repurpose the code above using the 'get.src()' 
# method to pull the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#####################################################################
# ## MODULE 10.3.5 - Scrape Mars Data: Mars Facts
#####################################################################


#####################################################################
# For scraping the data, we will use Pandas .read_html()
# method to read whole tables instead of item by item
#####################################################################

# Import pandas dependencies

import pandas as pd

# Create a new DataFrame from the HTML table using
# the Pandas read_html method. By specifying an index 
# of [0], we're telling Pandas to pull only the first table 
# it encounters (or the first item in the list). Then, it 
# turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Assign columns to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']

# Set the 'Description' column into the DataFrame's index. 
# inplace=True means that the updated index will remain in 
# place, without having to reassign the DataFrame to a new 
# variable.
df.set_index('description', inplace=True)

# Inspect the dataframe.
df

# Pandas also has a way of converting a dataframe back to 
# an HTML table by using the to_html() method.
df.to_html()

# End the browsing session.
browser.quit()

#####################################################################
# MODULE 10.3.6 - Export to Python
#####################################################################


# Export to Python using the jupyter notebook <File> menu, 
# <Download as> and <Python (.py)> selections. Then open the file in
# Visual Studio Code and clean unnecesary comments (such as how
# many times each cell was run).

