import spacy
from spacy.training.example import Example
from train_data import TRAIN_DATA  # Import your generated training data

def train_ner_model(train_data, iterations=20):
    # Create a blank English model
    nlp = spacy.blank("en")
    # Add NER pipe to the model
    ner = nlp.add_pipe("ner")

    # Add labels from the training data
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Initialize optimizer
    optimizer = nlp.begin_training()

    for itn in range(iterations):
        losses = {}
        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses, sgd=optimizer)
        print(f"Iteration {itn+1} - Losses: {losses}")

    # Save the trained model to disk
    nlp.to_disk("fra_ner_model")
    print("Training completed. Model saved to 'fra_ner_model'.")

if __name__ == "__main__":
    train_ner_model(TRAIN_DATA)
