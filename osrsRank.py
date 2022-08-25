import scrapy
from scrapy.crawler import CrawlerProcess

class OSRSSpider(scrapy.Spider):
    name = "OSRS"

    def start_requests(self):
        team = self.team
        team = ('+').join(team.split(' '))
        url = "https://secure.runescape.com/m=hiscore_oldschool_ironman/group-ironman/?groupName=" + team
        yield scrapy.Request(url, callback = self.parse)

    def parse(self, response):
        for g in response.css('.uc-scroll__table-row').getall():
            outResponse.insert(0, [g.css('.uc-scroll__link::text').get(), g.css('.uc-scroll__table-cell::text').get()])

def lookforResult(items, teamName):
    for i in items:
        if i[0] == teamName:
            return i[1]

    return "iunno"

def OSRSCrawler(teamName):
    outputResponse = []
    process = CrawlerProcess({"LOG_ENABLED": False})
    process.crawl(OSRSSpider, outputResponse = outputResponse, team = teamName)
    process.start()
    return lookforResult(outputResponse, teamName)