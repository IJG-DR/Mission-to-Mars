#####################################################################
# The following code scrapes the most recent article, the teaser text, 
# the image associated with it, and facts about mars from two NASA url's. 
#####################################################################

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


#####################################################################
# Define the scrape_all function that our app.py will call when
# the web page button is clicked.
#####################################################################

def scrape_all():
    # Initiate headless driver for deployment
    # Set executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # Set URL and browser
    browser = Browser('chrome', **executable_path, headless=True)
    # Call the function that gets the title and teaser body
    news_title, news_paragraph = mars_news(browser)
    # Call the function that gets the urls and titles for the hemispheres
    hemispheres = mars_hemispheres(browser)
    # Run all scraping functions and store results in dictionary.
    # Include a timestamp to know when the data was obtained.
    # We will also call on the two other functions to get the
    # featured image and the mars facts.
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemispheres,
      "last_modified": dt.datetime.now()
    }
    
    # End the browsing session and return the data.
    browser.quit()
    return data


#####################################################################
# SCRAPE THE TITLE AND TEASER BODY OF THE MOST RECENT ARTICLE
#####################################################################

# Repurpose the code in the original scraping.py file to convert the 
# title and teaser scraping into a function, and pass as imput the 
# variable 'browser' created in are app.py code file. Also add a 
# try-except code to handle potential errors.
def mars_news(browser):
    
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

    # Add try/except for error handling
    try:
    
        # Use select_one to only select the first item, as we only want
        # the most recent Nasa article on the page.
        # Use div.list_text to search for all 'div' tag with a class 'list_text'
        slide_elem = news_soup.select_one('div.list_text')

        # look inside the slide_elem object for the specific title
        slide_elem.find('div', class_='content_title')

        # Clean the title of other html code. 
        # Use the parent element to find the first `a` tag and 
        # save it as `news_title`.
        # This line is similar to the code above, but adds the 
        # method "get_text()" to extract only the text from the html.
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # After using Inspector on that element of
        # the web page, we identied it is associated with class "article_teaser_body."
        # Repurpose the above code to get it.
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Add except so that if it runs into an AttributeError type, python 
    # returns nothing for each variable.
    except AttributeError:
        return None, None

    # Return the article title and teaser body
    return news_title, news_p




#####################################################################
# SCRAPE THE FEATURED IMAGES
#####################################################################

# Repurpose the code in the original scraping.py file to convert the 
# scraping of the image into a function, and pass as imput the 
# variable 'browser' created in are app.py code file. Also add a 
# try-except code to handle potential errors.

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try-except for error handling
    try:

        # Repurpose the code above using the 'get.src()' 
        # method to pull the link to the image.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    return img_url




#####################################################################
# SCRAPE THE MARS FACTS
#####################################################################

def mars_facts():

    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    # Use the BaseException "catch-all" or general exception 
    # for error handling.
    except BaseException:
            return None

    # Assign columns to the new DataFrame for additional clarity
    # and set the index to 'description'.
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()



#####################################################################
# SCRAPE FOR THE HEMISPHERES
#####################################################################

def mars_hemispheres(browser):

     #1. Use browser to visit the URL 
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
    return hemisphere_image_urls


#####################################################################
# If running as script
#####################################################################


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


#####################################################################
# END
#####################################################################




