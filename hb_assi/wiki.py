#wiki.py
# !pip install wikipedia
import wikipedia

class Wikipedia:
    def __init__(self, language="en"):
        wikipedia.set_lang(language)

    def get_summary_of_first_result(self, query, sentences=3):
        results = wikipedia.search(query)
        if results:
            return results[0], wikipedia.summary(results[0], sentences=sentences)
        return None, "No results found."
