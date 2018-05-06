from srvmod.crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler()
    Crawler.Verbose = True
    crawler.run()