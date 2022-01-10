import time
import pandas as pd
import numpy as np
import tkinter as tk
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
from sys import exit
import machine_learning 
import itertools as it

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
    Last 5 minutes - 10s spacing take readings

    # Length of history list readings needed (queue) (one every 10s): 120 (past and future)
    10s for past - sliding window queue for 5s intervals with overlap (0-10, 5-15, 10-20, etc.)
    60 features - words typed in 10s intervals for past 5 mins
    1 label - 60 summed indexes for future - words typed in future 5 mins
    Can change intervals if want length of queue to be different, based on # of bins
    """

    def __init__(self):
        # 5 mins in future, 5 mins in past (length = 120, 60 and 60)
        self.np_wordcount_queue = []
        self.wordcount = 0
        # self.ml_object = machine_learning.ml()
        self.time_last_change = 0
        self.PAGE_LENGTH = 4002
        self.roadblock = False
        self.nb_standby = 0
        self.intervals_array = []
        self.split_intervals_array = []
        self.wordcount_list = [0, ]
        self.total_wordcount_list = []

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
        
        charcount, self.wordcount, sentencecount, pagecount = 0, 0, 0, 0
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
                    self.wordcount += 1
        self.wordcount_list.append(self.wordcount)
        # print("wordcount list:", self.wordcount_list)
        
        charcount = len(prompt.replace('\n', ''))
        pagecount = len(prompt) // self.PAGE_LENGTH

        # case: user wrote or deleted nothing for 60s
        # if nothing has changed from last loop and the last change was over 60s ago --> standby
        standbyNotification = ""
        if charcount == 0:
            self.time_last_change = time.time()
            self.last_charcount = charcount
            self.last_wordcount = self.wordcount
            self.last_sentencecount = sentencecount

        if (time.time() - self.time_last_change) > 60:
            standbyNotification = "You've entered a standby"
            self.nb_standby += 1

        # set Thresholds to -1 unless a number exists
        wordcountThresholdInt, pagecountThresholdInt = -1, -1
        try:
            wordcountThresholdInt = int(self.input_wordcount_threshold.get(0.0, "end"))
        except:
            pass

        # put values in interface
        self.output_charcount.insert(tk.INSERT, charcount)
        self.output_wordcount.insert(tk.INSERT, self.wordcount)
        self.output_sentencecount.insert(tk.INSERT, sentencecount)
        self.output_pagecount.insert(tk.INSERT, pagecount)
        self.output_standby.insert(tk.INSERT, standbyNotification)

        # call realtime() every 5s
        self.main_window.after(5000, self.realtime)
        
        return self.wordcount_list
    
    def lists_of_lists(self):
        overlap = 2 
        window_length = 10 # 10s
        split = window_length / overlap # 5s
        batch_length = 60 # 60 batches every 5 min
        retrain_delay = 300 # 5 min
        num_batches = retrain_delay / batch_length # 300/10 * 2 (overlap)= 60
        
        """
            Alternative for getting # words typed in each sliding window:

            Make data collection window 5 seconds. For each sliding window, add 
            the # words in those 5 seconds to the next # words in the next 5
            seconds. 
            Example: # words in sliding window 0-10 = #window1 + #window2
                    # words in sliding window 5-15 = #window2 + #window3
                    # words in sliding window 10-20 = #window3 + #window4
                    etc....
        """

        self.total_wordcount_list.append(self.wordcount_list)
        self.wordcount_list = []
        self.main_window.after(5000, self.lists_of_lists) 
        print(self.total_wordcount_list)
        return self.total_wordcount_list

        """
                np_wordcount_queue = np.zeros(1000)
                np_wordcount_queue = np.insert(np_wordcount_queue, 0, int(self.wordcount))
                if len(np_wordcount_queue) > retrain_delay:
                np_wordcount_queue = np.delete(np_wordcount_queue, 0) # remove oldest reading
                
                index = 0
                wordcount_queue = []
                realtime = self.realtime()
                for index in np.arange(0, 29, realtime): # compute two batches each time, 60 in all
                    wordcount_queue.append(self.wordcount)
                    self.realtime()
                    # print(wordcount_queue)
                    first_half_sum = wordcount_queue[index] # first 5s (0-5)
                    second_half_sum = wordcount_queue[index] # second 5s (5-10)
                    third_half_sum = wordcount_queue[index] # second 5s (10-15)
                    first_batch = first_half_sum + second_half_sum
                    second_batch = second_half_sum + third_half_sum

                index = 0
                beginning_intervals = 0
                for beginning_intervals in range (0, retrain_delay + 1, 5): 
                    beginning_intervals = beginning_intervals # beginning interval of each batch
                    end_intervals = beginning_intervals + 10 # end interval of each batch
                    for index in range (0, 1, 5):
                        self.intervals_array.insert(0, beginning_intervals)
                        self.intervals_array.insert(0, end_intervals)
                self.intervals_array.pop(0) # extra 310
                self.intervals_array.pop(1) # extra 305
                self.intervals_array.reverse() # was in reverse order beforehand

                # move across array in window fashion, printing each beginning and end interval pair
                def moving_window(x, length, step=1):
                    streams = it.tee(x, length)
                    return zip(*[it.islice(stream, i, None, step*length) for stream, i in zip(streams, it.count(step=step))])
                self.split_intervals_array = list(moving_window(self.intervals_array, 2))
                # print(self.split_intervals_array)
                self.np_split_intervals_array = np.array(self.split_intervals_array)
                dataframe = pd.DataFrame(self.np_split_intervals_array)
                dataframe["wordcount"] = ""
                print(dataframe)

                realtime_time = time.time()
                realtime_index = 0
                time_frame_condition = round((time.time() - realtime_time), 2)
                while time_frame_condition <= 300:
                    time_frame_condition = round((time.time() - realtime_time), 2)
                    if time_frame_condition % 5 == 0 and time_frame_condition >= 0:
                        dataframe.insert(realtime_index, "wordcount", self.wordcount_list)
                        realtime_index += 1
                
                # online training
                for index in np.arange(0, batch_length - 1, 1):
                    keyboard_training_features = self.np_wordcount_queue[self.split_intervals_array].sum()
                    keyboard_training_label = sum(self.np_wordcount_queue[:-300])
                    print(keyboard_training_features)
                
                training_features = [sum(self.wordcount_queue[i:5*i+5]) for i in range(5*60/5)]
                training_label = sum(self.wordcount_queue[:-300])
                
                curr_features = [sum(self.diff_wordcount_queue[301+i:300+5*i+5]) for i in range(5*60/5)]
                ml_prediction = []
                ml_label_predicted = ml_prediction.predict(curr_features) < wordcountThresholdInt
                if ml_label_predicted:
                    if self.roadblock:
                        self.popup_display()
                    else:
                        self.popup_close()
        """
    def every_5_min(self):
        # second list is 0-5, third is 5-10, fourth is 10-15, etc.
        # second value in list is most updated, use this - wordcount every 5s
        wordcount_index = 2 # first two inner lists are unused, first interval wanted is 0-10
        final_wordcount_list = []
        # print(self.wordcount_list)
        # for  in range (0, len(self.total_wordcount_list), wordcount_index):
        for i in range (0, len(self.total_wordcount_list), wordcount_index):
            # ACCESS SECOND ELEMENT OF EACH INNER LIST FOR 5 MIN
            wordcount_in_interval = self.wordcount_list[i]
            print(wordcount_in_interval)
            # final_wordcount_list.append(wordcount_in_interval)
            wordcount_index += 1
        # print(wordcount_index)
        
        self.main_window.after(5000, self.every_5_min) # run every 5 min

if __name__ == '__main__':
    gui1 = gui()
    # main processing function
    gui1.realtime()
    gui1.lists_of_lists()
    gui1.every_5_min()

    # main loop blocks code from continuing past this line
    # ie code in class runs and doesn't finish until exit using interface or command line
    gui1.main_window.mainloop()