# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_normal project
# 
#   在这里，此文件只包括重要的和常用的设置，具体你可以参考以下文档：
# 
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_normal'

SPIDER_MODULES = ['scrapy_normal.spiders']
NEWSPIDER_MODULE = 'scrapy_normal.spiders'


# 通过user-agent认证你的身份(或者你网站的身份)对爬行负法律责任(常见于搜索引擎识别)
#USER_AGENT = 'scrapy_normal (+http://www.yourdomain.com)'

# 遵从 robots.txt 协议
ROBOTSTXT_OBEY = False

# Scrapy downloader 并发请求(concurrent requests)的最大值。
CONCURRENT_REQUESTS = 32


# 
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# 下载延迟
#DOWNLOAD_DELAY = 3
# 下载延迟设置将只遵守一个：
# 对单个网站进行并发请求的最大值。(default: 0)
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站。
#CONCURRENT_REQUESTS_PER_IP = 16

# 是否开启cookie下载(enabled by default)
#COOKIES_ENABLED = False
#COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# 默认的请求头:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# 爬虫中间键
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_normal.middlewares.ScrapyNormalSpiderMiddleware': 543,
#}

# 下载中间键
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'scrapy_normal.middlewares.ScrapyNormalDownloaderMiddleware': 543,
   'scrapy_normal.middlewares.UAmiddleware': 800,
}

# scrapy 扩展
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 项目管道 
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 300
}

# 自动限速扩展 (disabled by default)
# spider永远以1并发请求数及 AUTOTHROTTLE_START_DELAY 中指定的下载延迟启动。
# 当接收到回复时，下载延迟会调整到该回复的延迟与之前下载延迟之间的平均值。
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# 初始下载延迟(单位秒)
#AUTOTHROTTLE_START_DELAY = 5
# 在高延迟情况下最大的下载延迟(单位秒)
#AUTOTHROTTLE_MAX_DELAY = 60
# 默认情况下，AutoThrottle调整延迟发送一个同步请求每个远程网站。
# 将此选项设置为更高的值（例如2），以增加远程服务器上的吞吐量和负载。
# 下调（如0.5）使爬虫更保守和礼貌
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 起用AutoThrottle调试(debug)模式，展示每个接收到的response。
#AUTOTHROTTLE_DEBUG = False

# 启用和配置HTTP缓存 (disabled by default)
# 理论上应该在调试的时候开启，这样可以避免以为频繁请求而被网站封杀
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
 
#确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
 
#默认请求序列化使用的是pickle 但是我们可以更改为其他类似的。PS：这玩意儿2.X的可以用。3.X的不能用
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"
 
#不清除Redis队列、这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True
 
#使用优先级调度请求队列 （默认使用）
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
 
#最大空闲时间防止分布式爬虫因为等待而关闭
#这只有当上面设置的队列类是SpiderQueue或SpiderStack时才有效
#并且当您的蜘蛛首次启动时，也可能会阻止同一时间启动（由于队列为空）
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

 
#序列化项目管道作为redis Key存储
#REDIS_ITEMS_KEY = '%(spider)s:items'
 
#默认使用ScrapyJSONEncoder进行项目序列化
#You can use any importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'
 
#指定连接到redis时使用的端口和地址（可选）
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
 
#指定用于连接redis的URL（可选）
#如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
#REDIS_URL = 'redis://user:pass@hostname:9001'
 
#自定义的redis参数（连接超时之类的）
#REDIS_PARAMS  = {}
 
#自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'
 
#如果为True，则使用redis的'spop'进行操作。
#如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
#REDIS_START_URLS_AS_SET = False
 
#RedisSpider和RedisCrawlSpider默认 start_usls 键
#REDIS_START_URLS_KEY = '%(name)s:start_urls'
 
#设置redis使用utf-8之外的编码
#REDIS_ENCODING = 'latin1'