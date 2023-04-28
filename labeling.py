import spacy


nlp = spacy.load("ja_ginza")
text = "アップルがカリフォルニア州クパチーノに本社を構える。"
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)
