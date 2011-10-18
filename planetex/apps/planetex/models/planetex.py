from django.core import meta

# Create your models here.
class Feed(meta.Model):
    format = meta.CharField(maxlength=10, null=True)
    link_xml = meta.CharField(maxlength=250)
    link_html = meta.CharField(maxlength=250, null=True)
    title = meta.TextField(null=True)
    tagline = meta.TextField(null=True)
    author_name = meta.CharField(maxlength=150, null=True)
    author_email = meta.EmailField(null=True)
    author_url = meta.CharField(maxlength=250, null=True)
    image = meta.CharField(maxlength=250, null=True)
    subtitle = meta.CharField(maxlength=250, null=True)
    generator = meta.CharField(maxlength=250, null=True)
    language = meta.CharField(maxlength=50, null=True)
    license = meta.CharField(maxlength=250, null=True)
    updated = meta.CharField(maxlength=100, null=True) # meta.DateTimeField()
    # HTTP Request data
    last_visit = meta.DateTimeField(null=True) # meta.CharField(maxlength=100) # 
    modified = meta.DateTimeField(null=True) # meta.CharField(maxlength=100) #
    etag = meta.CharField(maxlength=50, null=True)
    status = meta.IntegerField(null=True)
    feed_type = meta.CharField(maxlength=50, default='planet', null=True)
    created = meta.DateTimeField(auto_now_add=True) # meta.CharField(maxlength=100) # 
    def __repr__(self):
        return self.title or 'Untitled'
    class META:
        admin = meta.Admin()    

class Post(meta.Model):
    feed = meta.ForeignKey(Feed)
    title = meta.TextField(null=True)
    link = meta.CharField(maxlength=250, null=True)
    author = meta.CharField(maxlength=150, null=True)
    summary = meta.TextField(null=True)
    content = meta.TextField(null=True)
    modified = meta.CharField(maxlength=150, null=True) # meta.DateTimeField() # 
    license = meta.CharField(maxlength=150, null=True)
    enclosure_url = meta.CharField(maxlength=250, null=True)
    enclosure_type = meta.CharField(maxlength=100, null=True)
    enclosure_length = meta.IntegerField(null=True)
    guid = meta.CharField(maxlength=250, null=True)
    # Others
    hash = meta.CharField(maxlength=50, null=True)
    created = meta.CharField(maxlength=100) # meta.DateTimeField(auto_now_add=True) # 
    def __repr__(self):
        return self.title or 'Untitled'
    class META:
        admin = meta.Admin()    
        ordering=['modified']

class Category(meta.Model):
    title = meta.CharField(maxlength=100)
    created = meta.DateTimeField(auto_now_add=True)
    posts = meta.ManyToManyField(Post)
    class META:
        admin = meta.Admin()    

"""class Category_Post(meta.Model):
    category = ForeignKey('Category')
    post = ForeignKey('Post')
    created = meta.DateTimeField(auto_now_add=True)"""
    
class Tag(meta.Model):
    title = meta.CharField(maxlength=100)
    created = meta.DateTimeField(auto_now_add=True)
    posts = meta.ManyToManyField(Post)
    class META:
        admin = meta.Admin()    
    
"""class Tag_Post(meta.Model):
    tag = ForeignKey(Tag)
    post = ForeignKey(Post)
    created = meta.DateTimeField(auto_now_add=True)

class Word(meta.Model):
    label = meta.CharField(maxlength=100)
    created = meta.DateTimeField(auto_now_add=True)

class Word_Post(meta.Model):
    word = ForeignKey('Tag')
    post = ForeignKey('Post')
    created = meta.DateTimeField(auto_now_add=True)

class FlickrTag(meta.Model):
    label = meta.CharField(maxlength=100)
    created = meta.DateTimeField(auto_now_add=True)
"""