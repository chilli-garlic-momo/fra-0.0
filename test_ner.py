import spacy

nlp = spacy.load("fra_ner_model")

text = "Name of the claimant(s): Ramesh Kumar\nVillage: Gudur\nDistrict: Kurnool"
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)
