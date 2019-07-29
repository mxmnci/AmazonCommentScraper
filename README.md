# AmazonCommentScraper - Mac OS & Windows!
A python based app that uses the selenium automation framework to convert comments from any Amazon product page into a CSV file (compatible with Shopify!).

## Instructions:
1. Open up your Command Prompt or Terminal inside the "AmazonCommentScraper" folder and run this command:</br>
```python3 Main.py```<br><br>
2. Go to Amazon and locate your desired product and copy the product link. Example:</br>
```https://www.amazon.com/Scotch-Brand-Applications-Engineered-810K6/dp/B00006IF67/ref=cm_cr_arp_d_product_top?ie=UTF8```<br><br>
3. (Optional) If you are using Shopify make sure this name matches EXACTLY what your product name is at the end of the product link! Example:```https://modernbeyond.com/products/magic-scrubber-electric-brush```<br>
Use only the <b>```magic-scrubber-electric-brush```</b> part of your product link!<br><br>
4. Choose the minimum rating that you would like to gather. Example: choosing 3 stars collects reviews that are 3 stars and above.<br><br>
5. Choose the amount of comments that you would like the program to search for before terminating. Input 0 to search through all of them. <br><br>
6. Input any words that you would like to exclude from the comments. All reviews containing these words will be ignored.

### That's it, Enjoy :)
