import markov
import random
import pandas
import csv
from datetime import datetime
import matplotlib.pyplot as plt
my_name = "Han" ### CHANGE HERE IF YOU'RE SOMEONE ELSE USING THIS

class TextThread:
    def __init__(self, person_name: str, person_num: str):
        """
        person num whatever format the row[1] format is in
        """
        self.person_with = person_name
        self.person_num = person_num
        self.make_csv()
        self.pandas_setup()
        self.me_texts = self.data.loc[self.data["IsFromMe"] == 1]
        self.them_texts = self.data.loc[self.data["IsFromMe"] == 0]
        self.make_num_cons_text_lists()
        self.make_text_lists()
        self.me = Person(my_name, self.me_texts, self.me_in_a_row)
        self.them = Person(self.person_with, self.them_texts, self.them_in_a_row)
        self.make_dates_messages_dict()
    
    def pandas_setup(self):
        self.data = pandas.read_csv(self.person_messages_filename)
        self.data["date"] = self.data.apply(lambda row: datetime.strptime(row[6][2:10], "%y-%m-%d"), axis=1)
        self.data["time"] = self.data.apply(lambda row: datetime.strptime(row[6][11:],"%H:%M:%S").time(), axis=1)

    def make_csv(self):
        self.person_messages_filename = f"{self.person_with.lower()}_messages.csv"
        reader = csv.reader(open('messages.csv', 'r'))
        writer = csv.writer(open(self.person_messages_filename, 'w'))
        count = 0
        for row in reader:
            if count == 0:
                writer.writerow(row)
            if row[1] == self.person_num and row[7] != "" and row[7] != "NULL":
                writer.writerow(row)
            count += 1

    def make_num_cons_text_lists(self):
        from_who_list = self.data["IsFromMe"].tolist()
        self.me_in_a_row = []
        self.them_in_a_row = []
        prev_ind = 0
        cons_count = 0
        for ind in from_who_list:
            if ind != prev_ind:
                if prev_ind == 1:
                    self.me_in_a_row.append(cons_count)
                else:
                    self.them_in_a_row.append(cons_count)
                cons_count = 1
            else:
                cons_count += 1
            prev_ind = ind
    
    def make_text_lists(self):
        self.text_list = self.data["MessageText"].tolist()
        self.me_text_list = self.me_texts["MessageText"].tolist()
        self.them_text_list = self.them_texts["MessageText"].tolist()
    
    def make_dates_messages_dict(self):
        self.dates_messages_dict = {}
        self.dates_message_count_dict = {}
        for index, row in self.data.iterrows():
            if row["date"] not in self.dates_messages_dict.keys():
                self.dates_messages_dict[row["date"]] = [row["MessageText"]]
                self.dates_message_count_dict[row["date"]] = 1
            else:
                self.dates_messages_dict[row["date"]].append(row["MessageText"])
                self.dates_message_count_dict[row["date"]] += 1

    def generate_text_chain(self, back_and_forths: int, i_go_first=True, use_two=True):
        texts = ""
        if i_go_first:
            first = self.me
            second = self.them
        else:
            first = self.them
            second = self.me
        for i in range(back_and_forths):
            num_texts_person_one = first.get_random_text_num()
            num_texts_person_two = second.get_random_text_num()
            texts += f"{first.name}:\n\n{first.generate_multiple_texts(num_texts_person_one, use_two)}\n\n"
            texts += f"{second.name}:\n\n{second.generate_multiple_texts(num_texts_person_two, use_two)}\n\n"
        return texts
    
    def get_message_dates_count(self, phrases: list) -> dict: 
        phrase_dates_count = get_phrast_count_date_dict(phrases, self.dates_messages_dict)
        return phrase_dates_count





class Person:
    def __init__(self, name: str, texts: pandas.DataFrame, in_a_row: list):
        self.name = name
        self.texts = texts
        self.in_a_row = in_a_row
        self.text_list = texts["MessageText"].tolist()
        self.markov_setup()
        self.make_dates_messages_dict()
    
    def markov_setup(self):
        giant_string = ""
        for message_text in self.text_list:
            
            cleaned_text = message_text.replace(","," ").replace("."," ").replace("?"," ").replace("!"," ").replace(":"," ").replace(";"," ")
            words = cleaned_text.split(" ")
            for elem in words:
                if elem == "":
                    words.remove(elem)
            if words[0] not in ["Liked", "Loved", "Emphasized", "Questioned", "Laughed", "Disliked"]:
                if message_text[-1] == " ":
                    message_text = message_text[:-1]
                if message_text[-1] not in ["!", ".", "?"]:
                    message_text += ". "
                else:
                    message_text += " "
                giant_string += message_text
        self.word_list = markov.build_word_list(giant_string)
        self.next_words = markov.build_next_words(self.word_list)
        self.next_words_two = markov.build_next_two_words(self.word_list)
    
    def generate_text(self, use_two=True):
        if use_two:
            text = markov.generate_sentence_two(self.next_words_two)
        else:
            text = markov.generate_sentence(self.next_words)
        if text[-1] == "." and text[-1] != ".":
            text = text[:-1]
        return text
    
    def get_random_text_num(self):
        number_of_texts = self.in_a_row[random.choice(range(len(self.in_a_row)))]
        return number_of_texts
    
    def generate_multiple_texts(self, num_texts, use_two=True):
        texts = ""
        for i in range(num_texts):
            texts += f"{self.generate_text(use_two)}\n"
        return texts
    
    def make_dates_messages_dict(self) -> None:
        self.dates_messages_dict = {}
        self.dates_message_count_dict = {}
        for index, row in self.texts.iterrows():
            if row["date"] not in self.dates_messages_dict.keys():
                self.dates_messages_dict[row["date"]] = [row["MessageText"]]
                self.dates_message_count_dict[row["date"]] = 1
            else:
                self.dates_messages_dict[row["date"]].append(row["MessageText"])
                self.dates_message_count_dict[row["date"]] += 1
        
    def get_message_dates_count(self, phrases: list) -> dict: 
        phrase_dates_count = get_phrast_count_date_dict(phrases, self.dates_messages_dict)
        return phrase_dates_count



def get_phrase_count_date_dict(phrases: list, messages_with_dates: dict):
    messages_dates_count = {}
    for day in messages_with_dates.keys():
        messages_dates_count[day] = 0
        for message in messages_with_dates[day]:
            words = message.split(" ")
            if words[0] not in ["Liked", "Loved", "Emphasized", "Questioned", "Laughed"]:
                if any(x in message for x in phrases):
                    messages_dates_count[day] += 1
    return messages_dates_count
    

def generate_one_text(words_dict):
    sentence_two = markov.generate_sentence_two(words_dict)
    if sentence_two[-1] == "." and sentence_two[-2] != ".":
        sentence_two = sentence_two[:-1]
    return sentence_two

def generate_multiple_texts(words_dict, num_texts):
    texts = ""
    for i in range(num_texts):
        texts += f"{generate_one_text(words_dict)}\n"
    return texts

