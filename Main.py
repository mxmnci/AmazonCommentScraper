import AmazonScraper

AmazonScraper.scrape(input("Please input your Amazon Product URL: "), 
input("Please input the EXACT Shopify product name: "), 
int(input("Please input the minimum rating you would like to gather 1-5: ")), 
int(input("Please input the amount of comments you would like to search (input 0 to search all): ")), 
input("Please input the words you would like to exclude separated by commas (If there are none then leave this blank): \n").split(','))

