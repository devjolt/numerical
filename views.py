from random import choice, randint, shuffle

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64
from matplotlib.ticker import LinearLocator

import numpy as np

from django.shortcuts import render
from django.views.generic import TemplateView, ListView

class HomeView(TemplateView):
    template_name = 'numerical/home.html'



class BarChartFourBars():
    """Bar chart with four bars
    """
    question_count = 0
    
    def __init__(self):
        self.generate_context()
        self.generate_data()
        self.make_sub_questions()
        self.generate_diagram()
        
    def generate_context(self):
        print('generate_context')
        context_options = (
            {'establishment':'restaurant', 'users':'customers', 'verb':'visited'},
            {'establishment':'website', 'users':'users', 'verb':'viewed'},
            {'establishment':'road', 'users':'drivers', 'verb':'used'},
            )
        context_choice = choice(context_options)
        self.description = f'The bar chart shows the number of {context_choice["users"]} who {context_choice["verb"]} a {context_choice["establishment"]} on one particular day' 
        self.context = {
            'selected': context_choice,
            'description':self.description,
            }

        print(self.context['description'])
        
    def generate_data(self):
        print('generate_data')
        self.labels = ['A','B','C','D']
        self.values = [randint(10, 150) for i in range(4)]
        self.data = {}
        for i in range(len(self.labels)):
            self.data[self.labels[i]] = self.values[i]

    def generate_diagram(self):
        def valuelabel(key,values):
            for i in range(len(key)):
                plt.text(i,values[i],values[i], ha = 'center')

        plt.bar(self.data.keys(), self.data.values()) # plot bar chart
        valuelabel(list(self.data.keys()), list(self.data.values()))
        plt.xlabel(self.context['selected']['establishment'].capitalize()) # define labels
        plt.ylabel(f"No. of {self.context['selected']['users']}")
        plt.grid(axis="y")
        plt.show() # display plot

        flike = io.BytesIO()
        plt.savefig(flike)
        self.b64 = base64.b64encode(flike.getvalue()).decode()
        plt.close() # otherwise plot keeps on writing to itself again and again

    def sub_how_many(self):
        print('sub_how_many')
        question = f"How many {self.context['selected']['users']} {self.context['selected']['verb']} all of the {self.context['selected']['establishment']}s in total?"
        #print(question)
        """
        [item: answer text, indicator = correct/incorrect, id = int]
        """
        letters = ['b','c','d','e']
        correct_value = sum(self.values)
        items = [{'item':correct_value,'indicator':'correct','id':f'{self.question_count}a'}]
        #print(items[0])
        used = []
        while len(items)!=5:
            if randint(0,1)==0:
                val = randint(1,5)
            else:
                val = randint(-5,-1)
            if val not in used:
                items.append({
                    'item':correct_value+val,
                    'indicator':'incorrect',
                    'id':f'{self.question_count}{letters[len(used)]}'})
                used.append(val)
            else:
                continue
            shuffle(items)  
        return {'question':question, 'items':items}

    def difference(self):
        print('difference')
        
        first_choice = choice(self.labels)
        second_choice = first_choice
        while first_choice==second_choice:
            second_choice = choice(self.labels)
   
        question = f"What is the difference in the number of {self.context['selected']['users']} who {self.context['selected']['verb']} {self.context['selected']['establishment']}s {first_choice} and {second_choice}?"
        #print(question)
        
        """
        [item: answer text, indicator = correct/incorrect, id = int]
        """
        letters = ['b','c','d','e']
        correct_value = abs(self.data[first_choice]-self.data[second_choice])
        items = [{'item':correct_value,'indicator':'correct','id':f'{self.question_count}a'}]
        #print(items[0])
        used = [correct_value]
        attempt_count = 0
        while len(items)!=5:
            print(used)
            print(items)
            print(self.labels)
            wrong_first_choice = choice(self.labels)
            wrong_second_choice = wrong_first_choice
            while wrong_first_choice==wrong_second_choice:
                wrong_second_choice = choice(self.labels)
            val = abs(self.data[wrong_first_choice]-self.data[wrong_second_choice])
            
            if val not in used:
                items.append({
                    'item':correct_value+val,
                    'indicator':'incorrect',
                    'id':f'{self.question_count}{letters[len(used)-1]}'})
                used.append(val)
            else:
                print('this one used:', val)
                attempt_count+=1
                if attempt_count>10:
                    val = randint(1,100)
                    items.append({
                        'item':correct_value+val,
                        'indicator':'incorrect',
                        'id':f'{self.question_count}{letters[len(used)-1]}'})
                    used.append(val)
                else:
                    continue
        shuffle(items)  
        return {'question':question, 'items':items}

    def following_day(self):
        #print('following_day')
        
        percentages = [5, 10, 15, 20, 25, 30, 35]
        percentage = choice(percentages)
        first_choice = choice(self.labels)
        change_type = choice(['increased', 'decreased'])
        
        question = f"On another day, the number of {self.context['selected']['users']} who {self.context['selected']['verb']} {self.context['selected']['establishment']} {first_choice} {change_type} by {percentage}% (rounded to the nearest 5%). How many {self.context['selected']['users']} {self.context['selected']['verb']} {self.context['selected']['establishment']} {first_choice} during this day?"
        #print(question)
        
        """
        [item: answer text, indicator = correct/incorrect, id = int]
        """
        letters = ['b','c','d','e']
        difference = round(self.data[first_choice]/100*percentage)
        correct_value = self.data[first_choice] + difference if change_type == 'increased' else self.data[first_choice] - difference 
        items = [{'item':correct_value,'indicator':'correct','id':f'{self.question_count}a'}]
        #print(items[0])
        used = [correct_value]
        while len(items)!=5:
            r = randint(0,4)
            if r==0:# same percentage, different letter
                other_letter = first_choice
                while other_letter == first_choice:
                    other_letter = choice(self.labels)
                difference = round(self.data[other_letter]/100*percentage)
                incorrect_value = self.data[other_letter] + difference if change_type == 'increased' else self.data[other_letter] - difference 
            
            elif r==1: # same letter and percentage, wrong way
                incorrect_value = self.data[first_choice] - difference if change_type == 'increased' else self.data[first_choice] + difference 
            elif r==2:
                incorrect_value= correct_value+randint(1,3)
            elif r==3:
                incorrect_value=correct_value-randint(1,3)
            else: # same letter, different percentage
                other_percentage = percentage
                while other_percentage == percentage:
                    other_percentage = choice(percentages)
                difference = round(self.data[first_choice]/100*other_percentage)
                incorrect_value = self.data[first_choice] + difference if change_type == 'increased' else self.data[first_choice] - difference 

            if incorrect_value not in used:
                items.append({
                    'item':incorrect_value,
                    'indicator':'incorrect',
                    'id':f'{self.question_count}{letters[len(used)-1]}'})
                used.append(incorrect_value)
            else:
                continue
            shuffle(items)  
        return {'question':question, 'items':items}
    
    def make_sub_questions(self):
        print('make_sub_questions')
        only_once = {
            'sub_how_many':self.sub_how_many,
        }
        question_options = {
            'difference':self.difference,
            'following_day':self.following_day,
        }
        used = []
        self.questions = []

        for question in only_once.keys():
            self.questions.append(only_once[question]())
            self.question_count+=1

        while len(self.questions)!=5:
            stuff = choice(list(question_options.keys()))
            if question_options[stuff]()['question'] not in used:
                print(question_options[stuff]()['question'])
                self.questions.append(question_options[stuff]())
                self.question_count+=1
                used.append(question_options[stuff]()['question'])

    def return_data_dict(self):
        self.question_count = 0
        return {
            'diagram':self.b64,
            'description':self.description,
            'questions':self.questions
        }

class Graph():
    """
    Bar chart with four bars
    """
    question_count = 0
    
    def __init__(self):
        self.generate_context()
        self.generate_data()
        
        self.make_sub_questions()
        self.generate_diagram()
        
        
    def generate_context(self):
        """
        preposition
        subject
        object
        verb
        unit
        unit_description
        """
        print('generate_context')
        
        context_options = (
            {'preposition':'far','subject':'employees','object':'company','verb':'travel', 'end':'travel to work each day', 'unit':'mile','unit_description':'distance', 'range':[1,5,10,15,20], 'sigma':5},
            {'preposition':'high','subject':'players','object':'basketball team', 'verb':'jump','end':'can jump', 'unit':'cm', 'unit_description':'height','range':[80,90,100,110,120],'sigma':10}
            )
        self.context_choice = choice(context_options)
        self.context = {
            'selected': self.context_choice,
            'description':f'The table shows how {self.context_choice["preposition"]} {self.context_choice["subject"]} in one {self.context_choice["object"]} {self.context_choice["end"]}',
            }

        print(self.context['description'])
        
    def generate_data(self):
        print('generate_data')
        self.labels = self.context['selected']['range']
        self.better_labels = []
        for i in range(len(self.labels)+1):
            #print(i)
            if i == 0: # first item
                #print('first item')
                self.better_labels.append(f'Less than {self.labels[i]} {self.context_choice["unit"]}')
            elif i == len(self.labels):
                #print('last item')
                self.better_labels.append(f'More than {self.labels[-1]} {self.context_choice["unit"]}')
            else:
                #print('middle item')
                gap = self.labels[-1] - previous_val
                self.better_labels.append(f'{self.labels[i-1]} to {self.labels[i]} {self.context_choice["unit"]}')
                
            if i!=5:
                previous_val = self.labels[i]

            #print(self.better_labels)
        range_value = self.labels[-1]-self.labels[0]
        mean_value = range_value/2+self.labels[0]
        self.number_of = randint(40, 90) 
        all_values = np.random.normal(mean_value, self.context_choice["sigma"], self.number_of)
        #print(all_values)
        values = [0 for i in range(len(self.labels)+1)]

        for value in all_values:
            value = round(value)
            if value <= self.labels[0]:
                values[0]+=1
            elif self.labels[0]<value<=self.labels[1]:
                values[1]+=1
            elif self.labels[1]<value<=self.labels[2]:
                values[2]+=1
            elif self.labels[2]<value<=self.labels[3]:
                values[3]+=1
            elif self.labels[3]<value<=self.labels[4]:
                values[4]+=1
            elif self.labels[4]<=value:
                values[5]+=1
        
        self.values = [str(v) for v in values]

        self.data = {}
        for i in range(len(self.labels)+1):
            self.data[self.better_labels[i]] = self.values[i]
        print(self.data)
        
    def generate_diagram(self):
                 
        data = [[value] for value in self.values]
        print(data)
        columns = "Number of {self.context['selected']['subject']}"
        rows = self.better_labels
             
        # Get some pastel shades for the colors
        colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
        n_rows = len(data)
                
        # Plot bars and create text labels for the table
        cell_text = data

        fig, ax = plt.subplots()
        ax.set_axis_off()
        #print('dir(ax)',dir(ax))
        #print('dir(fig)',dir(fig))
        #help(ax.set_autoscale_on)
        #ax.set_autoscale_on(True)
        the_table = ax.table(
            cellText=cell_text,
            rowLabels=rows,
            #rowColours=colors,
            colLabels=columns,
            rowLoc='right',
            cellLoc='center',
            loc='upper right',   
        )
                  
        plt.show()

    # to add:
    # total increases. by. What is the new total?
    # top two / bottom two increase by. What is the new total?
    # each day, increase by 5% (rounded down to the nearest person. How many after x days)
    """
        preposition
        subject
        object
        verb
        unit
        unit_description
    """
    
    def sub_how_many(self):
        print('sub_how_many')
        question = f"How many {self.context['selected']['subject']} are there in total?"
        #print(question)
        """
        [item: answer text, indicator = correct/incorrect, id = int]
        """
        letters = ['b','c','d','e']
        correct_value = self.number_of
        items = [{'item':correct_value,'indicator':'correct','id':f'{self.question_count}a'}]
        #print(items[0])
        used = []
        while len(items)!=5:
            if randint(0,1)==0:
                val = randint(1,5)
            else:
                val = randint(-5,-1)
            if val not in used:
                items.append({
                    'item':correct_value+val,
                    'indicator':'incorrect',
                    'id':f'{self.question_count}{letters[len(used)]}'})
                used.append(val)
            else:
                continue
            shuffle(items)  
        return {'question':question, 'items':items}

    def how_many_x_or_more(self):
        # how many travel x or more to work (cam't tell)
        """
        3/4 questions to have an actual value as an answer
        1/4 questions to have a value which is "can't tell"

        if actual value:
        1. pick above or below
        2. if above, 
        3. pick a category boundary index NOT including -1
        4. question = how many are above {category[index]}
        5. correct answer = sum(index:end)
        6. incorrect answers =
        7. sum (any number except 0 or index: end)
        8. OR sum(index:end)+or-randint(1,5)
        9. OR can't tell
        10. if below,
        11. pick a category boundary index NOT including 0
        12. question = how many are below {category[index]}
        13. correct answer = sum(0:index)
        14. incorrect answers =
        15. sum (start: any number except index)
        16. OR sum(index:end)+or-randint(1,5)
        17. OR can't tell

        if not actual value:
        correct answer: can't tell
        incorrect answers:
        pick above or below,
        pick boundary index, calculate
        if randint(0,3)==0: + or - randint(1,5)
        """
        pass

    def most_least_common(self):
        # what is the most/least common distance that employees travel
        """
        select most or least common.
        if most common:
        get index of highest value, and corresponding index of category name
        for correct answer
        every other incorrect answer are every other random answers

        """
        pass

    def what_percentage(self):
        # what percentage travel between (1-3 categories)
        """
        pick two random indexes
        calculate percentage
        other percentages +- steps of 2 or 3
        """
        pass

    def change_move_from_one_cateory_to_another(self):
        # x employees change from one category to another. what percentage now..
        """
        choose category from and to
        select rantint value between two category values
        transfer value
        choose pick either from or to category
        what percentage in this category
        """
        pass

    def ratio_of_employees_two_categories():
        # ratio of employees who travel (one category to all others) cant tell
        """
        
        """
        pass


    def ratio_of_employees_above_below():
        """
        if time
        """
        pass
        
    def difference(self):
        print('difference')
        
        first_choice = choice(self.labels)
        second_choice = first_choice
        while first_choice==second_choice:
            second_choice = choice(self.labels)
   
        question = f"What is the difference in the number of {self.context['selected']['users']} who {self.context['selected']['verb']} {self.context['selected']['establishment']}s {first_choice} and {second_choice}?"
        #print(question)
        
        """
        [item: answer text, indicator = correct/incorrect, id = int]
        """
        letters = ['b','c','d','e']
        correct_value = abs(self.data[first_choice]-self.data[second_choice])
        items = [{'item':correct_value,'indicator':'correct','id':f'{self.question_count}a'}]
        #print(items[0])
        used = [correct_value]
        print(used)
        while len(items)!=5:
            print(items)
            wrong_first_choice = choice(self.labels)
            wrong_second_choice = wrong_first_choice
            while wrong_first_choice==wrong_second_choice:
                wrong_second_choice = choice(self.labels)
            val = abs(self.data[wrong_first_choice]-self.data[wrong_second_choice])
            
            if val not in used:
                items.append({
                    'item':correct_value+val,
                    'indicator':'incorrect',
                    'id':f'{self.question_count}{letters[len(used)-1]}'})
                used.append(val)
            else:
                continue
        shuffle(items)  
        return {'question':question, 'items':items}

    def make_sub_questions(self):
        print('make_sub_questions')
        sub_question_options = {
                'sub_how_many':self.sub_how_many,
                #'difference':self.difference,
                #'following_day':self.following_day,
            }
        sub_questions = []
        while len(sub_questions)!=5:
            stuff = choice(list(sub_question_options.keys()))
            sub_questions.append(sub_question_options[stuff]())
            self.question_count+=1

        for question in sub_questions:
            print()
            print(question)
        



class QuestionView(TemplateView):
    template_name = 'numerical/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        question_options = [
            BarChartFourBars
            ]

        generator = choice(question_options)()
        question_data = generator.return_data_dict()

        context['diagram'] = question_data['diagram']
        context['description'] = question_data['description']
        context['question0'] = question_data['questions'][0]['question']
        context['items0'] = question_data['questions'][0]['items']
        context['question1'] = question_data['questions'][1]['question']
        context['items1'] = question_data['questions'][1]['items']
        context['question2'] = question_data['questions'][2]['question']
        context['items2'] = question_data['questions'][2]['items']
        context['question3'] = question_data['questions'][3]['question']
        context['items3'] = question_data['questions'][3]['items']
        context['question4'] = question_data['questions'][4]['question']
        context['items4'] = question_data['questions'][4]['items']
        
        return context

    # select question type
    # generate
    # pass through

#https://spapas.github.io/2021/02/08/django-matplotlib/
# note: maths questions
# physics questions
# pure awesome

class SampleView(TemplateView):
    template_name = 'numerical/test.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days = [i for i in range(10)]
        counts = [randint(1,100) for i in range(10)]
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(days, counts, '--bo')

        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.set_title('By date')
        ax.set_ylabel("Count")
        ax.set_xlabel("Date")
        ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
        ax.yaxis.set_minor_locator(LinearLocator(25))

        flike = io.BytesIO()
        fig.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        context['chart'] = b64
        return context