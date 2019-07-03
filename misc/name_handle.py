import json
import random
from misc.term import Term


class Name_Handler:
    noun_dict = []
    adj_dict = []
    fname_dict = []
    lname_dict = []

    def __init__(self):
        self.read_data()

    def read_data(self):
        word_type = ""
        with open('data/terms.txt') as terms:
            for index, line in enumerate(terms):
                if (line[0] == "["):
                    print(line)
                    word_type = line.replace("\n", "").replace("\t", "")
                elif (line == "\n"):
                    print("Blank Line Spacer")
                else:
                    t_info = json.loads(line)
                    cur_term = Term()
                    cur_term.set_name(t_info["word"])
                    cur_term.set_assocs(t_info["definitions"]["tags"])

                    if (word_type == "[Nouns]"):
                        cur_term.set_plural(t_info["definitions"]["plural"])
                        self.noun_dict.append(cur_term)
                    elif (word_type == "[Adjectives]"):
                        self.adj_dict.append(cur_term)
                    elif (word_type == "[FirstName]"):
                        self.fname_dict.append(cur_term)
                    elif (word_type == "[LastName]"):
                        self.lname_dict.append(cur_term)

        print(len(self.noun_dict))
        print(len(self.adj_dict))
        print(len(self.fname_dict))
        print(len(self.lname_dict))

    def get_random_name(self):
        f_name = self.fname_dict[random.randint(0, len(self.fname_dict) - 1)]
        l_name = self.lname_dict[random.randint(0, len(self.lname_dict) - 1)]
        return [f_name, l_name]
