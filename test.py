import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Warren Buffett is the CEO of Berkshire Hathaway.")
print([ent.text for ent in doc.ents])
