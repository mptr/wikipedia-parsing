from xml.sax import handler
from .Article import Article
from models.ambiguity import Ambiguity

class PageHandler(handler.ContentHandler):
    tagsToWatch = ["title", "text"]

    currentPage = None
    currentTag = None

    def startElement(self, name, attrs): # set currentTag on enter or create page

        if name == "page":
            self.currentPage = Article() # create blank page object

        if name in self.tagsToWatch:
            self.currentTag = name # set current Tag

        if name == "redirect": # handle disambiguition on auto redirect pages
            Ambiguity.create(base=attrs.get("title"), alt=self.currentPage.title, kind='redirect')
            del self.currentPage

        return super().startElement(name, attrs)
    

    def endElement(self, name): # unset currentTag on leave or save page

        if self.currentPage == None: # skip all if there is no active page
            return super().endElement(name)

        if name == "page": # page is done
            if(input("process " + self.currentPage.title + "? [y/N]") == "y"):
                self.currentPage.done()
            del self.currentPage

        if name in self.tagsToWatch: # unset current Tag
            self.currentTag = None

        return super().endElement(name)


    def characters(self, content): # collect characters based on current active tagname
        if self.currentPage == None: # skip all if there is no active page
            return super().characters(content)

        if self.currentTag == "title": # apend title of current Tag to page instance
            self.currentPage.acceptTitle(content)

        if self.currentTag == "text":
            self.currentPage.acceptText(content)

        return super().characters(content)