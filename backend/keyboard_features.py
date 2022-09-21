import time
import pandas as pd
import numpy as np
import enchant
from nltk.tokenize import word_tokenize, sent_tokenize
import warnings
import nltk
# nltk.download('punkt')
warnings.filterwarnings('ignore')

class keyboard():
    
    def __init__(self):
        self.start_time = time.time()
        self.min_time = 0
        self.time_last_change = time.time()
        self.termination_time = time.time()

        self.previous_charcount = 0
        self.PAGE_LENGTH = 4002

        self.counter = 0
        self.completion = False
        self.roadblock = False
        self.new = False
        self.previous_roadblock = False
        self.roadblock_number = 0
        self.previous_saved_charcount = 0
        self.saved_charcount = 0
        self.previous_saved_wordcount = 0
        self.saved_wordcount = 0
        self.previous_saved_sentencecount = 0
        self.saved_sentencecount = 0

        self.standby = False
        self.nb_standby = 0
        self.features_list = ["wordcount", "sentencecount", "standby", "number of standby", "roadblock number", "words produced", "sentences produced", "words deleted", "sentences deleted", "change in wordcount", "change in sentencecount"]
        self.history_time_seconds = []
        self.history_min_time_seconds = []
        self.history_charcount = []
        self.history_wordcount = []
        self.history_sentencecount = []
        self.history_standby = []
        self.history_nb_standby = []
        self.history_features = []
        self.history_dffeatures = []
        self.history_roadblock = []
        self.history_roadblock_number = []
        self.wordcount_list = []
        self.history_new = []
        
        self.row_index = 0
        self.keyboard_training_features = pd.DataFrame()
        self.training_label = []

        self.text = ''

    def realtime(self, text):
        charcount, wordcount, sentencecount = 0, 0, 0
        wordcount_threshold, pagecount_threshold = 0, 0
        dictionary = enchant.Dict("en_US")
        
        completeSentences = sent_tokenize(text)  # arg needs to be a string, produces array of sentences

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
                    # self.time_last_change = time.time()

        charcount = len(text.replace('\n', ''))
        if self.previous_charcount != charcount:
            self.time_last_change = time.time()
        self.previous_charcount = charcount

        pagecount = len(text) // self.PAGE_LENGTH
        
        # case: user wrote or deleted nothing for 10s
        if (time.time() - self.time_last_change) > 10:
            self.standby = True
            self.nb_standby += 1
        else:
            self.standby = False

        """
            # way back when we had tkiner gui...
            # WHEN ML MODEL IS FINISHED INCORPORATE PREDICTIONS INTO ROADBLOCK NOTIFICATION POPPING UP
            ml_label_predicted = machine_learning.training_predictions < wordcountThresholdInt
            if ml_label_predicted:
                if self.roadblock:
                    self.popup_display()
                else:
                    self.popup_close()
        """

        # print(((self.keyboard_training_features['wordcount']) == wordcount).any())
        if self.counter != 0:
            similar_rows = self.keyboard_training_features[self.keyboard_training_features['wordcount'] == wordcount]
            if wordcount in self.history_wordcount and not similar_rows.empty:
            # if wordcount in self.keyboard_training_features.values:
            # if ((self.keyboard_training_features['wordcount']) == wordcount).all():
                self.new = True
                # print(similar_rows)
                # similar_row = similar_rows[0]
                # print(self.history_wordcount)
                self.min_time = similar_rows['min time (s)'].iloc[0]
                print(self.min_time)
            else:
                self.min_time = time.time() - self.start_time
                self.new = False
            print(self.min_time)
        if self.counter == 0:
            self.counter += 1

        # for data collection
        self.history_time_seconds.append(time.time() - self.start_time)
        self.history_new.append(self.new)
        self.history_charcount.append(charcount)
        self.history_wordcount.append(wordcount)
        self.history_sentencecount.append(sentencecount)
        self.history_standby.append(self.standby)
        self.history_nb_standby.append(self.nb_standby)
        self.history_roadblock.append(self.roadblock)
        self.history_roadblock_number.append(self.roadblock_number)
        if (self.min_time == 0):
            self.history_min_time_seconds.append(time.time() - self.start_time)
        else:
            self.history_min_time_seconds.append(self.min_time)
        
        self.history_dffeatures = pd.DataFrame(self.history_features)
        
        self.history_dffeatures["new"] = self.history_new
        self.history_dffeatures["charcount"] = self.history_charcount
        self.history_dffeatures["wordcount"] = self.history_wordcount
        self.history_dffeatures["sentencecount"] = self.history_sentencecount
        self.history_dffeatures["number of standby"] = self.history_nb_standby
        self.history_dffeatures["standby"] = self.history_standby
        self.history_dffeatures["roadblock"] = self.history_roadblock
        self.history_dffeatures["roadblock number"] = self.history_roadblock_number
        self.history_dffeatures["change in charcount"] = self.history_dffeatures["charcount"].diff() if not self.history_dffeatures["charcount"].diff().empty else [0]
        self.history_dffeatures["change in wordcount"] = self.history_dffeatures["wordcount"].diff() if not self.history_dffeatures["wordcount"].diff().empty else [0]
        self.history_dffeatures["change in sentencecount"] = self.history_dffeatures["sentencecount"].diff() if not self.history_dffeatures["sentencecount"].diff().empty else [0]
        self.history_dffeatures["chars produced"] = self.history_dffeatures["change in charcount"].copy() if not self.history_dffeatures["change in charcount"].copy().empty else [0]
        self.history_dffeatures["chars produced"][self.history_dffeatures["chars produced"] < 0] = 0 
        self.history_dffeatures["words produced"] = self.history_dffeatures["change in wordcount"].copy() if not self.history_dffeatures["change in wordcount"].copy().empty else [0]
        self.history_dffeatures["words produced"][self.history_dffeatures["words produced"] < 0] = 0
        self.history_dffeatures["sentences produced"] = self.history_dffeatures["change in sentencecount"].copy() if not self.history_dffeatures["change in sentencecount"].copy().empty else [0]
        self.history_dffeatures["sentences produced"][self.history_dffeatures["sentences produced"] < 0] = 0
        self.history_dffeatures["chars deleted"] = -1*self.history_dffeatures["change in charcount"].copy() if not self.history_dffeatures["change in charcount"].copy().empty else [0]
        self.history_dffeatures["chars deleted"][self.history_dffeatures["chars deleted"] < 0] = 0
        self.history_dffeatures["chars deleted"] = self.history_dffeatures["chars deleted"].abs() if not self.history_dffeatures["chars deleted"].abs().empty else [0]
        self.history_dffeatures["words deleted"] = -1*self.history_dffeatures["change in wordcount"].copy() if not self.history_dffeatures["change in wordcount"].copy().empty else [0]
        self.history_dffeatures["words deleted"][self.history_dffeatures["words deleted"] < 0] = 0
        self.history_dffeatures["words deleted"] = self.history_dffeatures["words deleted"].abs() if not self.history_dffeatures["words deleted"].abs().empty else [0]
        self.history_dffeatures["sentences deleted"] = -1*self.history_dffeatures["change in sentencecount"].copy() if not self.history_dffeatures["change in sentencecount"].copy().empty else [0]
        self.history_dffeatures["sentences deleted"][self.history_dffeatures["sentences deleted"] < 0] = 0
        self.history_dffeatures["sentences deleted"] = self.history_dffeatures["sentences deleted"].abs() if not self.history_dffeatures["sentences deleted"].abs().empty else [0]
        self.history_dffeatures["time (s)"] = self.history_time_seconds
        self.history_dffeatures['min time (s)'] = self.history_min_time_seconds

        # take a rolling computation where 1st row would be computations of that row, 2nd row would be 1st and 
        # 2nd, 3rd so on until the last row, for example, is  mean of the last 60 rows
        for col in self.features_list:
            if col == "charcount" or col == "wordcount" or col == "sentencecount" or col == "standby" or col == "number of standby" or col == "roadblock" or col == "roadblock number":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(60, min_periods=1).mean() 
            # elif col == "standby":
            #     self.history_dffeatures["5rSUMMARY " + col] = self.history_dffeatures[col].rolling(60, min_periods=1).max()
            elif col == "chars produced" or col == "words produced" or col == "sentences produced" or col == "chars deleted" or col == "words deleted" or col == "sentences deleted" or col == "change in charcount" or col == "change in wordcount" or col == "change in sentencecount":
                self.history_dffeatures['5rSUMMARY ' + col] = self.history_dffeatures[col].rolling(60, min_periods=1).sum() 
        
        # because of current rolling mean, all previous rows are NaN, need to take most current row
        self.history_dffeatures = self.history_dffeatures.tail(1)

        # concatenate rows so dataframe is continuous
        self.keyboard_training_features = pd.concat([self.keyboard_training_features, self.history_dffeatures], axis=0)  
        self.row_index += 1

        """
        if self.columns == 0:
            # every 5s append one row to existing csv file to update records
            self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard1.csv', mode='a', header=True)
        else:
            self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard1.csv', mode='a', header=False)
        self.columns += 1
        """
        self.keyboard_training_features = self.keyboard_training_features.reset_index(drop=True)
        keyboard2 = None
        try:
            keyboard2 = pd.read_csv('keyboard3.csv')
        except:
            keyboard2 = pd.DataFrame()
            # every 5s append one row to existing csv file to update records
            self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard3.csv', mode='a', header=True, index=False)
        if not keyboard2.empty:
            self.keyboard_training_features.loc[self.row_index - 1:self.row_index].to_csv('keyboard3.csv', mode='a', index=False, header=False)

        # ROADBLOCK LOGIC
        # existence of roadblock is checked every 5 min
        # notification of roadblock is prompted if rate of charcount/wordcount/sentencecount written is less than previous 5 min
        # at time 0: previous_saved_charcount
        # at time 5: saved_charcount
        # at time 10: charcount
        # at time 15 and beyond: new charcount

        # changes too little
        # ((sentencecount - self.saved_sentencecount)/10 <= (self.saved_sentencecount - self.previous_saved_sentencecount)/10)
        if abs((float((charcount - self.saved_charcount)/10)) <= abs(float((self.saved_charcount - self.previous_saved_charcount)/10)) and 
        abs(float((wordcount - self.saved_wordcount)/10)) <= abs(float((self.saved_wordcount - self.previous_saved_wordcount)/10)) and
        (self.standby is True)):
            self.roadblock = True
            if self.previous_roadblock is False:
                self.roadblock_number += 1
            self.previous_roadblock = self.roadblock
        else:
            self.roadblock = False

        # if (time.time - self.start_time >= 60):
        self.previous_saved_charcount = self.saved_charcount
        self.saved_charcount = charcount
        self.previous_saved_wordcount = self.saved_wordcount
        self.saved_wordcount = wordcount
        self.previous_saved_sentencecount = self.saved_sentencecount
        self.saved_sentencecount = sentencecount

        # COMPLETION LOGIC
        # check this every 5 min
        trade_buffer = open("thr.buf", 'r')
        with trade_buffer as f:
            lines = f.read() 
            wordcount_threshold = lines.split('\n', 1)[0]
            pagecount_threshold = lines.split('\n', 1)[1]
        
        if (wordcount == wordcount_threshold) or (pagecount == pagecount_threshold):
            self.completion = True
            self.termination_time = time.time()

        # write roadblock boolean to buf to check later
        # roadblock_buffer = open("roadblock.buf", 'w')
        # roadblock_buffer.write(str(self.roadblock))

        completion_buffer = open("completion.buf", "w")
        completion_buffer.write(str(self.completion))

        print(self.keyboard_training_features)
        # print(self.keyboard_training_features.columns)
        return self.keyboard_training_features
        
        # test both types of keyboard features in ml model and determine which has less error
        # return self.history_dffeatures # second training set - raw numbers
        # self.keyboard_training_features # first training set - means, maxes, sums

if __name__ == '__main__':
    keyboard1 = keyboard()
