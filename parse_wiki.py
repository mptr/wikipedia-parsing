from xml.sax import make_parser, handler
from sql_service import SqlService
import page_class, sys

sql = SqlService()

### Page SAX-Handler ###
class PageHandler(handler.ContentHandler):
    tagsToWatch = ["title", "text"]

    currentPage = None
    currentTag = None

    def startElement(self, name, attrs): # set currentTag on enter or create page

        if(name == "page"):
            self.currentPage = page_class.Page() # create blank page object

        if(name in self.tagsToWatch):
            self.currentTag = name # set current Tag

        if(name == "redirect"): # handle disambiguition on auto redirect pages
            sql.insert_ambiguity(attrs.get("title"), self.currentPage.title, 'redirect')
            del self.currentPage

        return super().startElement(name, attrs)
    

    def endElement(self, name): # unset currentTag on leave or save page

        if(self.currentPage == None): # skip all if there is no active page
            return super().endElement(name)

        if(name == "page"): # page is done
            #if(input("process " + self.currentPage.title + "?") == "p"):
            self.currentPage.done()
            del self.currentPage

        if(name in self.tagsToWatch): # unset current Tag
            self.currentTag = None

        return super().endElement(name)


    def characters(self, content): # collect characters based on current active tagname
        if(self.currentPage == None): # skip all if there is no active page
            return super().characters(content)

        if(self.currentTag == "title"): # apend title of current Tag to page instance
            self.currentPage.title  = self.currentPage.title + content
        if(self.currentTag == "text"):
            self.currentPage.acceptText(content)

        return super().characters(content)

### init ###
parser = make_parser()
parser.setContentHandler(PageHandler())
parser.parse(sys.argv[1])