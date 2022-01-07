import time
import pandas as pd
import tkinter as tk
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit
from ml import *

class gui():
    """
    STANDBY:
    Discrete gui notification that you haven't typed for 60s

    ROADBLOCK:
    min_goal = 200 words / 5 minutes --> if ml predicts from brain data + recent historic
    data that not going to hit min_goal in next 5 mins tells you to stop --> we call this
    a roadblock - ml predicts 200 words / 5 minute and is trained by you typing e.g. retrain
    every 10 mins?

    CHANGES:
    Last 5 minutes - 5s spacing take readings

    # length of history list readings needed (one every 5s): 120
    5s for past - sum up every 5 entries ie indexes 0-4, 4-8, ... for the first 300 entries
    (features are words typed in 5s intervals for past 5 mins)
    (length of queue is 120) - can change to 15s intervals if want length of queue to be 20 based on # of bins
    60 indexes to sum for future (label = words typed in future 5 mins)

    Takes 10 minutes to create datapoint 1
    after that making a new datapoint every 5s --> 60 datapoints in next 5 mins
    Therefore after 15mins have 60 datapoints
    """

    def __init__(self):
        # 5 mins in future, 5 mins in past (length=120, 60 and 60)
        self.wordcount_queue = []
        self.time_last_change = 0
        self.ml_object = ml()
        self.PAGE_LENGTH = 4002
        self.roadblock = False
        self.nb_standby = 0

        # Root of tk popup window when opened
        self.popup_root = None

        # Main tk window
        self.main_window = tk.Tk()
        self.main_window.title("Roadblocks Project")
        self.main_window.geometry("500x600")

        # Textbox for prompt
        promptLabel = tk.Label(self.main_window, text="Write prompt here")
        self.input_user_prompt = tk.Text(self.main_window, width=450, height=8, font=("Times New Roman", 12),
                                         wrap="word")

        # Textbox for wordcount threshold
        wordcountThresholdLabel = tk.Label(self.main_window, text="Wordcount threshold")
        self.input_wordcount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12),
                                                 wrap="word")

        pagecountThresholdLabel = tk.Label(self.main_window, text="Page count threshold")
        self.input_pagecount_threshold = tk.Text(self.main_window, width=10, height=1, font=("Helvetica", 12),
                                                 wrap="word")

        begin = tk.Button(self.main_window, text="Begin", command=self.realtime)

        charcountLabel = tk.Label(self.main_window, text="Charcount")
        self.output_charcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        wordcountLabel = tk.Label(self.main_window, text="Wordcount")
        self.output_wordcount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        sentencecountLabel = tk.Label(self.main_window, text="Sentence count")
        self.output_sentencecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        pagecountLabel = tk.Label(self.main_window, text="Page count")
        self.output_pagecount = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        standbyLabel = tk.Label(self.main_window, text="Standby")
        self.output_standby = tk.Text(self.main_window, width=20, height=1, font=("Helvetica", 12), wrap="word")

        promptLabel.pack()
        self.input_user_prompt.pack()

        charcountLabel.pack()
        self.output_charcount.pack()

        wordcountLabel.pack()
        self.output_wordcount.pack()

        sentencecountLabel.pack()
        self.output_sentencecount.pack()

        pagecountLabel.pack()
        self.output_pagecount.pack()

        standbyLabel.pack()
        self.output_standby.pack()

        wordcountThresholdLabel.pack()
        self.input_wordcount_threshold.pack()

        pagecountThresholdLabel.pack()
        self.input_pagecount_threshold.pack()

        begin.pack()

    def popup_display(self):
        # if no popup and should have popup, display it
        if not self.popup_root:
            self.popup_root = tk.Tk()  # create popup window
            popup_button = tk.Button(self.popup_root, text="You've hit a roadblock", font=("Verdana", 12), bg="yellow", command=exit)
            popup_button.pack()

    def popup_close(self):
        if self.popup_root:
            self.popup_root.destroy()  # destroys pop up window
            self.popup_root = None

    def realtime(self):
        self.output_charcount.delete(0.0, "end")
        self.output_wordcount.delete(0.0, "end")
        self.output_sentencecount.delete(0.0, "end")
        self.output_pagecount.delete(0.0, "end")
        self.output_standby.delete(0.0, "end")
        
        charcount, wordcount, sentencecount, pagecount = 0, 0, 0, 0

        dictionary = enchant.Dict("en_US")

        prompt = self.input_user_prompt.get(0.0, "end")
        completeSentences = sent_tokenize(prompt)  # produces array of sentences
        for sentence in completeSentences:
            sentencecount += 1
            words = word_tokenize(sentence)
            for i, word in enumerate (words):
                if i == len(words) - 1:
                    if word[-1] != "." and word[-1] != "?" and word[-1] != "!":
                        sentencecount -=1 
                # this dictionary counts . as words, but not ! or ?
                if dictionary.check(word) and word != ".":
                    wordcount += 1
        
        charcount = len(prompt.replace('\n', ''))
        pagecount = len(prompt) // self.PAGE_LENGTH

        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if charcount == 0:
            self.time_last_change = time.time()
            self.last_charcount = charcount
            self.last_wordcount = wordcount
            self.last_sentencecount = sentencecount

        if time.time() - self.time_last_change > 60:
            standbyNotification = "You've entered a standby"
            self.nb_standby += 1

        # moving window queue
        i = 0
        overlap = 2 
        window_length = 5 # 5s
        split = window_length / overlap # 2.5s
        batch = (i * split) + window_length 
        batch_length = 120 # 120 batches every 5 min
        retrain_delay = 300 # 5 min
        num_batches = retrain_delay / batch_length
        self.wordcount_queue.append(wordcount)
        print(self.wordcount_queue)
        if len(self.wordcount_queue) > retrain_delay:
            self.wordcount_queue.pop(0) # remove oldest reading
        
        # online training
        training_features = [sum(self.wordcount_queue[i:5*i+5]) for i in range(5*60/5)]
        training_label = sum(self.wordcount_queue[:-300])
        
        # update ml object
        self.ml_object = self.ml_object

        # set Thresholds to -1 unless a number exists
        wordcountThresholdInt, pagecountThresholdInt = -1, -1
        try:
            wordcountThresholdInt = int(self.input_wordcount_threshold.get(0.0, "end"))
        except:
            pass

        # if nothing has changed from last loop and the last change was over 180s ago --> roadblock
        # this is wrong --> roadblocks are set by ml model only
        curr_features = [sum(self.diff_wordcount_queue[301+i:300+5*i+5]) for i in range(5*60/5)]
        ml_prediction = []
        ml_label_predicted = ml_prediction.predict(curr_features) < wordcountThresholdInt
        if ml_label_predicted:
            if self.roadblock:
                self.popup_display()
            else:
                self.popup_close()

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 10s
        self.main_window.after(10000, self.realtime)

if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()