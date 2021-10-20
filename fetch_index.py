import requests, re, wget

baseUrl = 'https://dumps.wikimedia.org/enwiki/latest/'
index = requests.get(baseUrl) # fetch index of wikidump

href_regex = re.compile(r'href=".*?"') # extract all hrefs
hrefs = href_regex.findall(index.text, re.M)
hrefs = map(lambda ln: ln.replace('href="', "").replace('"', ""), hrefs)

hrefs = filter(lambda x: "multistream" in x, hrefs) # only with multistream
hrefs = filter(lambda x: ".xml" in x, hrefs) # only xmls
hrefs = filter(lambda x: "multistream.xml" not in x, hrefs) # not xml containing all
hrefs = filter(lambda x: not x.endswith("-rss.xml"), hrefs) # no xmls with -rss

number_regex = re.compile(r'(\d*).xml') # get number of file
def replace_with_padded_number(f): # en...istream1.xml-..z2 -> en...istream001.xml-..z2
    number = int("0" + number_regex.search(f).groups()[0])
    return re.sub(number_regex, ("%03d" % number) + ".xml", f)

for h in hrefs:
    filename = replace_with_padded_number(h)
    print("donloading " + h)
    wget.download(baseUrl + h, out=filename)
