#!/usr/bin/python2.4
"""Planet Express

Handles RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom feeds

Uses Universal Feed Parser <http://feedparser.org/docs/>

Required: Python 2.1 or later
Recommended: Python 2.3 or later
Recommended: CJKCodecs and iconv_codec <http://cjkpython.i18n.org/>
"""

__version__ = "0.3"
__license__ = "BSD"
__copyright__ = "(C) 2004, 2005 Victor R. Ruiz <rvr@blogalia.com>"
__author__ = "Victor R. Ruiz <http://rvr.typepad.com/>"

_debug = 1

import sys, codecs, md5, pprint
import time, datetime, optparse
from mx.DateTime import ISO

import feedparser
from django.models.planetex import feeds, posts

class PlanetReader:
    """ Class Planet Reader """

    def __init__(self, database=None):
        """ Constructor """
        self.page_fields = {
            'url': 'link_xml',
            'status' : 'status',
            'etag' : 'etag'
        }
        self.feed_fields = {
            'link' : 'link_html',
            'title' : 'title',
            'tagline' : 'tagline',
            'generator' : 'generator',
            'tagline' : 'tagline',
            #'image' : 'image', ## Dict
            'generator' : 'generator',
            'language' : 'language',
        }
        self.post_fields = {
            'title' : 'title',
            'link' : 'link',
            'author' : 'author',
            'content' : 'content',
            'license' : 'license',
            'guid' : 'guid',
        }
        
    def add(self, url, planet='planet'):
        """ Add a feed to the list.
        
            Returns True if successful. False is no feed found.
        """
        if (_debug): print "Parsing %s..." % (url)
        ## try:
        page = feedparser.parse(url)
        ## except:
        ##    if (_debug): print "Some error ocurred."
        ##    return False
        if (not page.has_key('url') or (page.has_key('url') and page.url == '')):
            if (_debug): print "Error downloading page."
            return False
        if (page.version == '' and page.bozo == 1
            and page.has_key('feed') and page.feed.has_key('links')):
            if (_debug): print "Not a feed. Autodiscovering..."
            # Not a Feed. Do autodiscover
            if (len(page.feed.links) > 0):
                if (_debug): print "Parsing links..."
                link = None
                for f in page.feed.links:
                    if (f.has_key('type') and f.has_key('rel') and f.has_key('href')
                        and f['type'] in ['application/rss+xml', 'application/atom+xml', 'text/xml']
                        and f['rel'] == 'alternate' and f['href'] <> ''):
                        if (_debug): print "href: %(href)s,  type: %(type)s" % (f)
                        if (link == None):
                            link = f
                        elif (f['type'] == 'application/atom+xml'):
                            # Atom feed priority
                            link = f
                if (link == None):
                    # Autodiscovery failed
                    if (_debug): print "Autodiscovery failed."
                    return False                
                if (_debug): print "Parsing %s..." % (link.href)
                feed = feedparser.parse(link.href)
                if (feed.version == ''):
                    if (_debug): print "Autodiscovery failed."
                    return False
                page = feed
                url = link.href
            else:
                return False
        if (_debug): print "Checking database to avoid duplications..."
        exists = feeds.get_count(link_xml__exact = page.url)
        if (exists > 0):
            if (_debug): print "Feed %s already in database." % (page.url)
            return False
        if (_debug): print "Saving data..."
        f = dict()
        for field in self.page_fields.keys():
            if (page.has_key(field)):
                print field
                print page[field]
                f[self.page_fields[field]] = page[field]
        if (page.has_key('modified')): f['modified'] = time.strftime('%Y-%m-%d %T', page.modified)
        for field in self.feed_fields.keys():
            if (page.feed.has_key(field)):
                f[self.feed_fields[field]] = page.feed[field]
        if (f.has_key('author_detail')):
            f['authorName'] = page.feed.author_detail.name
            f['authorEmail'] = page.feed.author_detail.email
            f['authorUri'] = page.feed.author_detail.url
        f['feed_type'] = planet
        try:
            feed = feeds.Feed(**f)
            feed.save()
    	    if (_debug): print "Data saved."
    	    return True
        except:
             if (_debug): print "Error saving data on feed %s" % (page.url)

    def update(self, feed=None, planet='planet'):
        """ Read new feed posts and publish them """
        if (_debug): print "Retrieving feed list..."
        if (feed <> None):
            feed_list = [feed]
        else:
            feed_list = feeds.get_list(feed_type__exact=planet)
        for feed in feed_list:
            if (_debug): print "Downloading %s..." % (feed.link_xml)
            # Download and parse the feeds
            try:
                params = dict()
                if (_debug): print "Etag: %s" % (feed.etag)
                ## if (feed.has_key('modified_parsed'): params['modified'] = feed.modified
                if (feed.etag <> ''):
                    p = feedparser.parse(feed.link_xml, etag=feed.etag)
                else:
                    p = feedparser.parse(feed.link_xml)
            except:
                if (_debug): print "Error downloading feed %s" % (feed.link_xml) 
                continue
            # Parse feed entries
            num = 0
            if (_debug): print "Saving new posts..."
            for post in p.entries:
                hash = self.__post_hash(post)
                # Check if post is already in database
                if (_debug): print "Checking if post exists... %s" % (hash)
                if (post.has_key('guid')):
                    if (_debug): print "guid... %s" % (post.guid)
                    old_post = posts.get_list(guid__exact = post.guid)
                else:
                    old_post = posts.get_list(hash__exact = hash)
                if (len(old_post) > 0):
                    # Post exists in database
                    if (_debug): print "Checking if post was updated... %s" % (old_post[0].hash)
                    if (old_post[0].hash <> hash):
                        # Publish post
                        if (_debug): print "Updating post..."
                        self.post_save(post, old_post[0])
                        if (_debug): print "Post updated."
                    else:
                        if (_debug): print "Post already published."
                else:
                    # Publish post
                    if (_debug): print "Publishing new post..."
                    self.post_save(post, feed = feed)
                    if (_debug): print "New post published."
            # Update feed data
            if (_debug): print "Updating feed data..."
            param = dict()
            if (p.has_key('etag')):
                param['etag'] = p.etag
            if (p.has_key('status')):
                param['status'] = p.status
            if (p.has_key('modified_parsed')):
                param['modified'] = datetime.datetime(*p.modified_parsed[:7])
            param['lastVisit'] = datetime.datetime.now()
            try:
                for field in param:
                    feed.__setattr__(field, param[field])
                if (_debug): print "Feed data updated."
            except:
                if (_debug): print "Error updating data."

    def post_save(self, post, old_post = None, feed = None):
        """ Saves a post """
        entry = dict()
        for field in self.post_fields.keys():
            if (post.has_key(field)):
                entry[self.post_fields[field]] = post[field]
        # Assign a date for the post
        print post.keys()
        if (post.has_key('updated_parsed') and (type(post.updated_parsed) == time.struct_time)):
            entry['modified'] = datetime.datetime(*post.updated_parsed[:7])
        elif (post.has_key('created_parsed') and (type(post.updated_parsed) == time.struct_time)):
            entry['modified'] = datetime.datetime(*post.created_parsed[:7])
        else:
            entry['modified'] = datetime.datetime.now()
        if (_debug): print "Date: %s" % (entry['modified'])
        if (post.has_key('content') and (len(post.content) > 0)):
            # Atom stores the content in post.content, which is a list
            entry['content'] = post.content[0].value
        elif (post.has_key('summary')):
            # RSS stores the content in post.summary
            entry['content'] = post.summary
        if (post.has_key('enclosure')):
            # Save enclosure data, if available
            entry['enclosureUrl'] = post.enclosure.url
            entry['enclosureType'] = post.enclosure.type
            entry['enclosureLength'] = post.enclosure.length
        entry['hash'] = self.__post_hash(entry)
        if (_debug): print "Saving post..."
        if (old_post <> None):
            for field in entry.keys():
                old_post.__setattr__(field, entry[field])
            old_post.save()
            if (_debug): print "Post saved."
        elif (feed <> None):
            entry['feed'] = feed
	    try:
                post = posts.Post(**entry)
	        post.save()
                if (_debug): print "Post saved."
	    except:
        	if (_debug): print "Error updating data."

        else:
            if (_debug): print "Need feed."

    def __post_hash(self, post):
        """ Generate a hash for the post """
        m = md5.new()
        text = u''
        if (post.has_key('title')):
            text = post['title']
        if (post.has_key('content')):
            if (type(post['content']) == list):
                text = text + post['content'][0].value
            else:
                text = text + post['content']
        elif (post.has_key('summary')):
            text = text + post['summary']
        if (text == u''):
            u''.join(post)
        m.update(text.encode('utf8'))
        return m.hexdigest()

def add_feed(url, planet='planet'):
    """ Add a single feed to the Planet """
    reader = PlanetReader()
    reader.add(url, planet=planet)

def add_file(file, planet='planet'):
    """ Add a feed list to the Planet """
    reader = PlanetReader()
    f = open(file, 'r')
    l = f.readlines()
    for site in l:
        reader.add(site, planet)
    
def update(planet='planet'):
    """ Update the Planet """
    reader = PlanetReader()
    reader.update(planet=planet)
    
def main():
    """ To be called from command line """
    from optparse import OptionParser
    print "Planet Express %s - %s\n"  % (__version__, __copyright__)
    usage = "python %prog [options] arg1 arg2\n\n"
    parser = OptionParser(usage=usage)
    parser.add_option('-i', '--init', action='store_true', help="Initialize the database.")
    parser.add_option('-u', '--update', action='store_true', help="Update the planet's feeds")
    parser.add_option('-a', '--add', action='store', dest='url', help='Add feed to planet. Autodiscovering supported.')
    parser.add_option('-f', '--file', action='store', dest='filename', help='Add file to planet. One URL per line.')
    parser.add_option('-d', '--database', action='store', dest='database', help='Database')
    (options, args) = parser.parse_args()
    
    if (options.init):
        initdb()
    elif (options.update):
        update()
    elif (options.url):
        add_feed(options.url)
    elif (options.filename):
        add_file(options.filename)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    
"""
TODO:
    - Standarize 'modified' date to feed assigns
"""