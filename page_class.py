import textprocess, re
from sql_service import SqlService

sql = SqlService()

wikidata_id_regex = re.compile(r'{{.*?=(Q\d+).*?}}', re.M)

### Page Class ###
class Page:
    def __init__(self):
        self.title = ""
        self.text = ""
        self.sents = None
        self.wikidata_id = ""
        self.doublebrace_depth = 0
        self.bracepipe_depth = 0

    def acceptText(self, t):
        self.text = self.text + t

    def filterText(self):
        t = self.text
        self.text = ''
        t = t.replace("{{", u"\u9999") # just random unicode to merge {{ and }}
        t = t.replace("}}", u"\u9998")
        t = t.replace("{|", u"\u9997") # just random unicode to merge {| and |}
        t = t.replace("|}", u"\u9996")
        for c in t: # remove nested {{ ... }} from text
            if(c == u"\u9999"): self.doublebrace_depth = self.doublebrace_depth+1
            if(c == u"\u9997"): self.bracepipe_depth = self.bracepipe_depth+1
            if(self.doublebrace_depth == 0 and self.bracepipe_depth == 0): self.text = self.text + c
            if(c == u"\u9998"): self.doublebrace_depth = self.doublebrace_depth-1
            if(c == u"\u9996"): self.bracepipe_depth = self.bracepipe_depth-1

    def done(self):
        # get wikidata id from captured text
        matches = list(wikidata_id_regex.finditer(self.text))
        if(len(matches) == 1): self.wikidata_id = matches[0].groups()[0]
        if(len(matches) > 1): raise Exception("Multiple wikidata-id matches")
        # filter text from non-regular stuff
        self.filterText()
        # process text in page
        self.sents = textprocess.to_sents(self.text)
        # save the page
        self.save()

    def save(self):
        sql.insert_page(self)