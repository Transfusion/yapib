import urllib
import urllib2
from bs4 import BeautifulSoup

def shortwiki(articleurl):

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] #wikipedia needs this
    
    
    resource = opener.open(articleurl)
    data = resource.read()
    resource.close()
    soup = BeautifulSoup(data)
    u = soup.find('div',id="bodyContent").p
    return u.get_text().encode('utf8')
    
# Many thanks to http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python?lq=1
