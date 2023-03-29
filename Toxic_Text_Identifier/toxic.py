import torch
import transformers
import re

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
model = transformers.BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
tokenizer = transformers.BertTokenizer.from_pretrained(model_name)

# Set device to run the model on
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# List of abusive words
abusive_words = ["hate", "stupid", "idiot", "fool", "moron"]

# Define function to predict toxicity and check for abusive words in text
def predict_and_check(texts, batch_size=16):
    num_texts = len(texts)
    results = []
    for i in range(0, num_texts, batch_size):
        # Tokenize texts
        batch = texts[i:i+batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt").to(device)

        # Predict toxicity
        outputs = model(**inputs)
        logits = outputs.logits
        scores = torch.softmax(logits, dim=1).tolist()

        # Check for abusive words in text
        for j in range(len(batch)):
            text = batch[j]
            toxic_prob = scores[j][1]
            abusive_words_present = check_abusive_words(text)
            result = {'text': text, 'toxicity': toxic_prob, 'abusive_words': abusive_words_present}
            results.append(result)

    # Return results
    return results

# Define function to check for abusive words in text
def check_abusive_words(text):
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Check if any abusive words are present in the text
    abusive_words_present = [word for word in abusive_words if word in text]
    return abusive_words_present

# Example usage
texts = ["I hate you, you're so stupid!", "I love you, you're the best!", "moron"]
results = predict_and_check(texts)
print(results)
