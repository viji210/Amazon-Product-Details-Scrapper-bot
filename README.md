# Scraping product details from amazon websites
## Overview
  Created a bot using Selenium webdriver that can Scrape from the Amazon website the Product's Title, Product's Price, Product's img url, Product's details, for 1000 different URLS of different products of the AMAZON website, the URL is created from the products Asin and country code, that I got as CSV file.

## Method of Approach
  First I tried scraping using the Beautifulsoup,Since it is faster than Selenium, but since forget to add time sleeps in between the request to the server, My IP address and Brower details got Blacklisted as Bot by the Amazon server, So whenever I try to get the HTML of the product website using the requests module, I got the Amazon captcha page Telling me to confirm that Iam not a bot.
  
  Then to prevent from getting Amazon Captcha I added some more details into my headers parameter of the requests, And for couple of time it Worked I got the Product HTML, But after that again I began to get the Amazon Captcha pages as the response.
  
  Since I don't have any paid proxies and Don't want to use the Free proxies, I decided to Scrape using the Selenium webdriver
  
  The Best thing about the Selenium is I can see my Code running Before my eyes, As it opened the URLS one by one, seeing it made me feel assured that my code running good.
  
  In order to respect the server and not to overload requests to the server and getting blacklisted as a bot, I add time sleep of 2secs in between each requests
  
## Scrapping URLS
  I didn't Scrape All 1000 Urls, I only Scrapped the first 200 urls, and the time taken for it 32 minutes, the CSV file containing the Asins and country codes that I got, I think it's pretty old, cause for the first 200 urls I only 30 product sites, for the rest of the URL's I got to see cute dog images of Amazon telling that the product information can't be found and some 404 responses.
