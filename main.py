from encoder import Model
import numpy as np
import utils
import matplotlib.pyplot as plt
import seaborn as sns
import string

def char_to_word(text, values):
    preprocessed_text = utils.preprocess(text)
    chars_to_display = "".join(list(map(lambda x: chr(int(x)), preprocessed_text)))

    sentiment_so_far = 0
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

    return pos, neg

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

def main(review_text):
    model = Model()
    sentiment_neuron_index = 2388

    # review_text = "This is a good branch. Friendly staff and good service. However, the line up was very very long and slow. I had to wait 30 minutes in line to get my service."
    # review_text = "Branch looks really nice but staff also needs to be kind to TD customers."
    # review_text = "This is good branch. But their service is terrible."

    if len(review_text) == 0: 
        review_text = "I had an issue with my accounts that TD could not resolve for me for years. I went to this branch & Ayush, who was the branch manager came to help me. Not only did he help me with what I came in for, but helped resolve my issue after asking for my banking experience with TD. He was very professionally dressed & was always smiling. He's a keeper. I'll be banking with TD for a very long time. Thank you"

    size = len(review_text)
    neuron_values = get_tracked_neuron_values_for_a_review(model, review_text, [sentiment_neuron_index])[0]

    pos, neg = char_to_word(review_text, neuron_values)

    # plot function only for visualization
    plot_neuron_heatmap(review_text, neuron_values)

    return pos, neg