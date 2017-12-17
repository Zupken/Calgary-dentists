import lxml.html
import requests
import database


class Scraping:

    def __init__(self):
        self.default_url = "https://www.canpages.ca/business/AB/calgary/dentists/91-239800-p"
        self.data = []
        self.site = lambda number: self.default_url + number + '.html'
        self.number = 1

    def get_data(self):
        while self.number < 39:
            try:
                print(self.site(str(self.number)))
                self.source = requests.get(self.site(str(self.number)))
                self.tree = lxml.html.fromstring(self.source.content)
                self.etree = self.tree.xpath('//div[@id="results-panel"]//div[@data-list="business"]')
                for element in self.etree:
                    try:
                        self.company = element.xpath('./div[@class="result__head"]/h2//text()')[0]
                    except IndexError:
                        self.company = 'N/A'
                    try:
                        self.distance = element.xpath('./div[@class="result__head"]/span[@class="result__distance"]/text()')[0]
                    except IndexError:
                        self.distance = 'N/A'
                    try:
                        self.address = element.xpath('./div[@class="result__address"]/text()')[0]
                    except IndexError:
                        self.address = 'N/A'
                    try:
                        self.phone = element.xpath('./div[@class="result__phone__wrap"]//span[@class="phone__number"]/text()')[0]
                    except IndexError:
                        self.phone = 'N/A'
                    self.data.append([self.company, self.distance, self.address, self.phone])
                self.number += 1
            except requests.exceptions.MissingSchema as e:
                print(e)
                break

    def save(self):
        Database = database.Database(('company', 'distance', 'address', 'phone number'))
        Database.create_database()
        for info in self.data:
            Database.insert_data(info)
        Database.commit_changes()


Scraping = Scraping()
Scraping.get_data()
Scraping.save()
