import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import re
import queue

#didn't know what to call it
class Racer(scrapy.Spider):
    name = 'Racer'
    #a set of pages that have been visited
    visited = set()
    link_list = []
    follow_links = []
    #the current page and paths to the current page
    paths = {}
    shortest_path = []
    def start_requests(self):
        self.paths[start_link] = []
        self.visited.add(start_link[start_link.find('/wiki'):])
        self.follow_links.append(start_link[start_link.find('/wiki'):])
        yield scrapy.Request(url=start_link, callback=self.parse)

    def parse(self, response):
        page_content = response.xpath('//main[@id="content"]')
        page_title = page_content.xpath('./header[1]/h1[1]//text()').get()
        if response.url == target_link:
            if self.shortest_path:
                if len(self.paths[response.url])+1 < len(self.shortest_path):
                    self.shortest_path = self.paths[response.url]
                    self.shortest_path.append(response.url)
            else:
                self.shortest_path = self.paths[response.url]
                self.shortest_path.append(response.url)
            print(f'Found {target_link} in {len(self.paths[response.url])+1} steps')
            print(f'path found: {" -> ".join(reversed(self.paths[response.url]))} -> {target_link}')
            return
        elif self.shortest_path:
            if len(self.shortest_path) <= len(self.paths[response.url])+1:
                return
        else:
            links = page_content.xpath('.//@href').getall()
            articles_re = r'^/wiki/(?!(File:|Category:|Talk:|Special:|Help:|Template:|Template_talk:|User:))'
            for link in links:
                link = link.split('#')[0]
                if link in self.visited:
                    continue
                if re.search(articles_re, link):
                        self.visited.add(link)
                        self.link_list.append(link)
                        # regex guarantees that the article
                        self.paths['https://en.wikipedia.org' + link] = [response.url] + self.paths[response.url]
            del self.paths[response.url]
            self.follow_links.remove(response.url.removeprefix('https://en.wikipedia.org'))
            if not len(self.follow_links):
                self.follow_links = self.link_list[:]
                self.link_list.clear()
                return response.follow_all(urls=self.follow_links, callback=self.parse)
            else:
                return


def main():
    print(sys.argv)
    global start_link
    global target_link
    start_link = sys.argv[1]
    target_link = sys.argv[2]
    wiki_racer = CrawlerProcess()
    wiki_racer.crawl(Racer)
    wiki_racer.start()
    print(Racer.shortest_path)

main()

