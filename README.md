# major_req_scraper
Finished up this quick little project! Fairly happy with it, it did what I needed it to but I could add some more functionality to the CSV analyzer part and make it more interactive.


- A simple web scraper to take UC Davis major requirement info into a csv file for later work. 

- A combiner to combine the scraped csv files into a single merged csv file for analysis. Formatted to distinguish classes that you can choose between. 

- A very basic analyzer, shows amount of units needed for both majors. Plan on coming back and adding more functionality. 

CS, Cog Sci, and Ling are the folder for the slightly modified webscrapers for each major. Stripped is where the scraped CSVs are put. Analysis is where the combined CSVs went. Merged 1 is CS and Cog Sci, Merged 2 is CS and Linguistics.

The class combiner will take any correctly formatted CSV for the stripped classes and put them into one combined one. The analyzer will take a combined CSV and tell you how many units the double major would be. I could definitely expand the functionality of the analyzer in the future, but at the moment that was the bulk of my curiosity.
