from itertools import chain
import re


# removes {{...}} and {|...|}
def remove_blocks(t):
    bracepipe_depth = 0
    doublebrace_depth = 0
    result = ''
    t = t.replace("{{", u"\u9999") # just random unicode to merge {{ and }}
    t = t.replace("}}", u"\u9998")
    t = t.replace("{|", u"\u9997") # just random unicode to merge {| and |}
    t = t.replace("|}", u"\u9996")
    for c in t: # remove nested {{ ... }} from text
        if(c == u"\u9999"): doublebrace_depth = doublebrace_depth+1
        if(c == u"\u9997"): bracepipe_depth = bracepipe_depth+1
        if(doublebrace_depth == 0 and bracepipe_depth == 0): result = result + c
        if(c == u"\u9998"): doublebrace_depth = doublebrace_depth-1
        if(c == u"\u9996"): bracepipe_depth = bracepipe_depth-1

    return result


# get wikidata ids from t
wikidata_id_regex1 = re.compile(r'{{.*?=(Q\d+).*?}}', re.M)
wikidata_id_regex2 = re.compile(r'wikidata.org[\w/\\]*?(Q\d+)', re.M)
def get_wikidata_ids(t):
    ms = chain(
        list(wikidata_id_regex1.finditer(t)),
        list(wikidata_id_regex2.finditer(t))
    )
    return set(map(lambda m: m.groups()[0], ms))


files = re.compile(r'\[\[File:.*?\]\]\n', re.M) # [[File:...]]\n
standalone_links = re.compile(r'\n\[\[.*?\]\]', re.M)
refs = re.compile(r'<\s*ref[\s\S]*?>[\s\S]*?<\s*\/\s*ref>', re.M) # matches <ref>...</ref>
headline = re.compile(r'^={2,}.*?={2,}\n', re.M)
stars_and_whitespace = re.compile(r'[\s*]{3,}', re.M)
html_comments = re.compile(r'<!--[\s\S]*-->', re.M)
newlines = re.compile(r'[\n ]+', re.M)
def cleanup_text(t):
    t = t.replace("'''", "")
    t = files.sub("", t) 
    t = standalone_links.sub("", t)
    t = refs.sub("", t)
    t = headline.sub("", t)
    t = stars_and_whitespace.sub("", t)
    t = html_comments.sub("", t)
    t = newlines.sub(" ", t)
    t = t.replace("''", '"')
    return t


links = re.compile(r'\[\[([^|\[\]]*?)\|?([^|\[\]]*?)\]\]', re.M) # https://regex101.com/r/R5HUKi/2
def find_links(t):
    ambigs = list()
    for i in links.finditer(t): # get links on page and save their texts and linked article in db
        [article, text] = i.groups()
        if(article != ""):
            ambigs.append(dict(
                base= article,
                alt= text
            ))
    return (links.sub(r"\2", t), ambigs) # remove link target for nlp