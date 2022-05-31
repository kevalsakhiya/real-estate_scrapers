# Scrapy settings for centris project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'centris'

SPIDER_MODULES = ['centris.spiders']
NEWSPIDER_MODULE = 'centris.spiders'


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'


# ====================================PIPELINE SETTINGS======================================
ITEM_PIPELINES = {
   # 'centris.pipelines.CentrisPipeline': 300,
   # 'centris.pipelines.ImagesDownloadPipeline': 301,
}


# ===================================AWS CREDS================================================
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

MEDIA_ALLOW_REDIRECTS = True
FILES_STORE = 's3://img-listing/'
