# Scrapy settings for duproprio project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'duproprio'

SPIDER_MODULES = ['duproprio.spiders']
NEWSPIDER_MODULE = 'duproprio.spiders'


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'


# ====================================PIPELINE SETTINGS======================================
ITEM_PIPELINES = {
   # 'duproprio.pipelines.DuproprioPipeline': 300,
}



