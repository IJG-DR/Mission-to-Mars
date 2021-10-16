

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
# Set URL and browser
browser = Browser('chrome', **executable_path, headless=False)

##############################################################
# ### Visit the NASA Mars News Site
##############################################################

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Search for elements with a specific combination of tag (div) and 
# attribute (list_text). Add an optional delay of 1 second in case
# the page is slow to load.
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser:
html = browser.html

# Convert the browser html to a soup object and then quit the browser
news_soup = soup(html, 'html.parser')

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



# Now get the teaser body. After using Inspector on that element of
# the web page, we identied it is associated with class "article_teaser_body."
# Repurpose the above code to get it.
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

##############################################################
# ### JPL Space Images Featured Image
##############################################################

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
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url



##############################################################
# ### Mars Facts
##############################################################


# Create a new DataFrame from the HTML table using
# the Pandas read_html method. By specifying an index 
# of [0], we're telling Pandas to pull only the first table 
# it encounters (or the first item in the list). Then, it 
# turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# Assign columns to the new DataFrame for additional clarity.
df.columns=['Description', 'Mars', 'Earth']

# Set the 'Description' column into the DataFrame's index. 
# inplace=True means that the updated index will remain in 
# place, without having to reassign the DataFrame to a new 
# variable.
df.set_index('Description', inplace=True)

# Inspect the dataframe.
df


# Pandas also has a way of converting a dataframe back to 
# an HTML table by using the to_html() method.
df.to_html()


##############################################################
# ### Hemisphere
##############################################################


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.

html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# Find the relevant content section in the html block
relevant_section = img_soup.find('div', class_='collapsible results')


# Use a for loop to: 
# CHANGE CODE TO CLICK LINKS !!!!!
# a) click on each hemisphere link, 
# b) navigate to the full-resolution image page, 
# c) retrieve the full-resolution image URL string and title for the hemisphere image,
# d) use browser.back() to navigate back to the beginning to get the next hemisphere image.

for titles in relevant_section:
    
    try:
        # Get the hemisphere image titles
        image_title = titles.find('h3').text
        print(image_title)
        
        # Get the thumbnail url
        thumbnail_url = titles.find('img', class_='thumb').get('src')
        print(thumbnail_url)
        
        img_link = titles.a['href']
        print(img_link)
        
        #complete the url address
        img_link_url = url + img_link
        print(img_link_url)
        
        #visit the image url
        browser.visit(img_link_url)
        html_2 = browser.html
        img_soup_2 = soup(html_2, 'html.parser')
        
        # exctarct the jpg image url
        image_url= url + img_soup_2.find('img', class_='wide-image').get('src')
        print(image_url)
        
        #Add image title and url to the list
        hemisphere_image_urls.append({'img_url':image_url,'title':image_title})
        
    except AttributeError:
        None


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# End the browsing session.
browser.quit()


##############################################################
# END
##############################################################