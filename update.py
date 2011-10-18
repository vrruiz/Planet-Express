#!/usr/bin/python
from planetex.apps.planetex.contrib import express

#express.add_feed('http://www.flickr.com/services/feeds/photos_public.gne?tags=lesblogs&format=rss_200', planet='flickr')
#express.add_feed('http://feeds.technorati.com/feed/posts/tag/lesblogs', planet='technorati')
#express.add_feed('http://www.alianzo.com/blogs/redessociales', planet='planet')
express.update(planet='planet')
express.update(planet='delicious')
