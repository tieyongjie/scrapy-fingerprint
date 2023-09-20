from scrapy.cmdline import execute
import os

dirpath = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirpath)
execute(['scrapy', 'crawl', 'democrawl'])