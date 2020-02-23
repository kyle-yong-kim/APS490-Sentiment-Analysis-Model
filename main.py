from encoder import Model
import numpy as np
import nltk
import utils
import matplotlib.pyplot as plt
import seaborn as sns
import string
from itertools import chain
from nltk.corpus import wordnet

def char_to_word(text, values):
    preprocessed_text = utils.preprocess(text)
    chars_to_display = "".join(list(map(lambda x: chr(int(x)), preprocessed_text)))

    sentiment_so_far = 0
    sentiment_overall = 0
    str_so_far = ""
    pos = []
    neg = []
    others = ['\n', ' ']

    for i, char in enumerate(chars_to_display):

        # need to reset the word
        if (char in string.punctuation or char in others) and (len(str_so_far) > 0):
            if sentiment_so_far/len(str_so_far) > 0:
                pos.append((str_so_far,sentiment_so_far/len(str_so_far)),)
            else:
                neg.append((str_so_far,sentiment_so_far/len(str_so_far)),)
            str_so_far = ""
            sentiment_so_far = 0

        elif char.isalpha():
            str_so_far += char
            sentiment_so_far += values[i]
        
        sentiment_overall += values[i]

    return pos, neg, round(sentiment_overall/len(chars_to_display), 2)

def plot_neuron_heatmap(text, values):
    preprocessed_text = utils.preprocess(text)
    n_limit = 57
    num_chars = len(preprocessed_text)

    for i in np.arange(0, len(values), n_limit):
        if i + n_limit > num_chars:
            end_index = num_chars
            #num_values_to_read = num_chars - i
            #values_limited = values[-num_values_to_read:]
            #values_reshaped = values_limited.reshape((1, num_values_to_read))
        else:
            end_index = i+n_limit
        values_limited = values[i:end_index]
        values_reshaped = values_limited.reshape((1, end_index - i))
        # chars_to_display = np.array(map(lambda x : str(x), list(preprocessed_text)[i:end_index])).reshape((1,end_index-i))
        chars_to_display = list(map(lambda x : chr(int(x)), list(preprocessed_text)[i:end_index]))
        chars_to_display = np.array(chars_to_display)
        chars_to_display = chars_to_display.reshape(1,end_index-i)
        #chars_to_display = np.array(list(preprocessed_text)[i:end_index], dtype=str).reshape(1,end_index-i)
        data = values_reshaped
        labels = chars_to_display
        fig, ax = plt.subplots(figsize=(20,0.5))
        
        ax = sns.heatmap(data, annot = labels, fmt = '', annot_kws={"size":15}, vmin=-1, vmax=1, cmap='RdYlGn')
    
    plt.show()

def get_tracked_neuron_values_for_a_review(model, review_text, track_indices):

    feats, tracked_indices_values = model.transform([review_text], track_indices=track_indices)
    return np.array([np.array(vals).flatten() for vals in tracked_indices_values])

def build_synonymDict(labelDict):

    synonymDict = {}
    nltk.download('wordnet')

    for key,val in labelDict.items():
        temp = set()

        for text in val:
            synonyms = wordnet.synsets(text)
            lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
            temp.update(lemmas)

        synonymDict[key] = temp

    return synonymDict

def get_aspects(pos, neg, synonymDict):
    
    res = {}

    # only care about identification
    for key, synonymSet in synonymDict.items():
        for word,_ in pos:
            if word.lower() in synonymSet:
                res[key+"_pos"] = res.get(key+"_pos", 0) + 1

        for word,_ in neg:
            if word.lower() in synonymSet:
                res[key+"_neg"] = res.get(key+"_neg", 0) - 1

    return res

def main(df):
    model = Model()
    sentiment_neuron_index = 2388
    size = df.shape[0]

    # generate synonym set
    labelDict = {
        'service' : ('knowledge','knowledgeable','service', 'help', 'helpful','benefit', 'informative', 'mistake', 'error', 'credible', 'quality', 'stupid', 'competence', 'inexperience', 'experience'),
        'queue' : ('queue','time','wait', 'fast', 'slow','line'),
        'friendliness' : ('friendliness','friendly', 'kind', 'rude', 'ignore', 'attention', 'professional', 'comforting', 'warm', 'cold', 'polite')
        }
    synonymDict = build_synonymDict(labelDict)
    
    res = {}
    for i, row in df.iterrows():
        review = row['Review']
        neuron_values = get_tracked_neuron_values_for_a_review(model, review, [sentiment_neuron_index])[0]
        pos, neg, sentiment_avg = char_to_word(review, neuron_values)

        # plot function only for visualization
        # plot_neuron_heatmap(review_text, neuron_values)

        aspect_performance = get_aspects(pos, neg, synonymDict)

        res[i] = (review, sentiment_avg, pos, neg, aspect_performance)

    return res