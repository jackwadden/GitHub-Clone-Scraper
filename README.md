# GitHub-Clone-Scraper

For various reasons, GitHub repo owners need to track the number of times their code is downloaded or cloned. GitHub allows repository owners to track clone counts in a sliding window via the <repo>/graphs/traffic pane. However, GitHub does not track total counts. This code uses GitHub's API to scrape <repo>/graphs/traffic for any number of an owner's repositories, saving this information in a file. The scraper is idempotent, meaning that it will never delete old unique entries, or write over existing information previously scraped from the database. Thus, this script can be set to run every few days to keep an accurate tally of total clones.

## Who would use this?

The NSF requires that grant recipients report how many times there code has been downloaded. Since I convinced my advisor that GitHub would help me get a job one day, he forced me to figure out how to do this.

## How can I use this?

Download the code and then set up a "cron" job to run the script every day, few days, week. GitHub seems to keep clone information for two weeks.




