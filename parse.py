from xml.sax import make_parser, handler
from sql_service import insert_ambiguity
from textprocess import textprocess

class Page:
    def __init__(self):
        self.title = ""
        self.text = ""
        self.doublebrace_depth = 0
        self.bracepipe_depth = 0

    def acceptText(self, t):
        t = t.replace("{{", u"\u9999") # just random unicode to merge {{ and }}
        t = t.replace("}}", u"\u9998")
        t = t.replace("{{", u"\u9997") # just random unicode to merge {| and |}
        t = t.replace("}}", u"\u9996")
        for c in t: # remove nested {{ ... }} from text
            if(c == u"\u9999"): self.doublebrace_depth = self.doublebrace_depth+1
            if(c == u"\u9997"): self.bracepipe_depth = self.bracepipe_depth+1
            if(self.doublebrace_depth == 0 and self.bracepipe_depth == 0): self.text = self.text + c
            if(c == u"\u9998"): self.doublebrace_depth = self.doublebrace_depth-1
            if(c == u"\u9996"): self.bracepipe_depth = self.bracepipe_depth-1

    def done(self):
        textprocess(self.text)
        self.save()

    def save(self):
        print(self.title)
        print(len(self.text)) # SQL

class PageHandler(handler.ContentHandler):
    tagsToWatch = ["title", "text"]

    currentPage = None
    currentTag = None

    def startElement(self, name, attrs): # set currentTag on enter or create page

        if(name == "page"):
            self.currentPage = Page() # create blank page object

        if(name in self.tagsToWatch):
            self.currentTag = name # set current Tag

        if(name == "redirect"): # handle disambiguition on auto redirect pages
            insert_ambiguity(attrs.get("title"), self.currentPage.title, 'redirect')
            del self.currentPage

        return super().startElement(name, attrs)
    

    def endElement(self, name): # unset currentTag on leave or save page

        if(self.currentPage == None): # skip all if there is no active page
            return super().endElement(name)

        if(name == "page"): # page is done
            if(input("process " + self.currentPage.title + "?") == "p"):
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


parser = make_parser()
parser.setContentHandler(PageHandler())
parser.parse("enwiki-latest-pages-articles-multistream000.xml")