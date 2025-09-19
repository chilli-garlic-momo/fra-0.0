import spacy

nlp = spacy.load("fra_ner_model")

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        entities[label] = entities.get(label, [])
        entities[label].append(ent.text)
    return entities
