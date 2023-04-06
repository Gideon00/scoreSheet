from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from helpers import get_start, listToString
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
import random
import csv
import kivy
from kivy.lang import Builder

kivy.require("1.9.1")


# Create list of regions
REGIONS = [
	"General",
	"Upper Limb",
	"Lower Limb",
	"Thorax",
	"Abdomen",
	"Pelvis",
	"Perineum",
    "Back",
    "Head",
    "Neck",
    "Face",
]


# First page      
class Mylayoutone(Screen):
    #global Region
    # radio button clicked
    limit = 0

    def checkbox_click(self, instance, value, region):
        if value == True and region in REGIONS:
            self.region = region

    # submit button clicked
    def on_submit(self):
    
        # Open file and read as dictionary to get limit
        file = open(f"//wsl.localhost/Ubuntu/home/rabboni/profAna/answers/{self.region}.csv")
        reader = csv.DictReader(file)
        self.limit = len(list(reader))



        # Check if start from user is valid
        self.start_id = int(self.ids.start_id.text)
        begin = get_start(self.start_id)
        if begin <= 0:
            exit("Negative or Zero not allowed")

        # Reject if start num exceeds end of region
        if begin > self.limit:
            exit("Number exceeds limit for this region")

        # Send region and limit to questions page
        App.get_running_app().root.ids.screen2.ids.selected_region.text = f"Practice {self.region} MCQs!"
        App.get_running_app().root.ids.screen2.ids.regionClue.text = self.region
        App.get_running_app().root.ids.screen2.ids.limit.text = str(self.limit)

        # Close file
        file.close()

        # Update question numbers
        App.get_running_app().root.ids.screen2.ids.question1.text = str(self.start_id)
        App.get_running_app().root.ids.screen2.ids.question2.text = str(self.start_id + 1)
        App.get_running_app().root.ids.screen2.ids.question3.text = str(self.start_id + 2)
        App.get_running_app().root.ids.screen2.ids.question4.text = str(self.start_id + 3)
        App.get_running_app().root.ids.screen2.ids.question5.text = str(self.start_id + 4)

# Questions Page
class Mylayoutwo(Screen):

    total_answers = 0
    final_answer = []
    question_page = 0
    first_question = 1
    marking_scheme = []
    ANSWER = []
    un_answered = []
    answer_sorted = []
    corrections = []
    question_nums = []
    quest = []
    un_ans = []
    un_ans2 = []
    reader = {}
    score = 0
    med_score = 0
    medical = 0
    first = 0
    last_q = 0

    def answer_click(self, instance, value, choice):
        # append answer and questions if clicked
        if "F" in choice and value == True:
            if f"{choice.rstrip(choice[-1])}T" in self.ANSWER:
                self.ANSWER.remove(f"{choice.rstrip(choice[-1])}T")
            self.ANSWER.append(choice)
        elif "T" in choice and value == True:
            if f"{choice.rstrip(choice[-1])}F" in self.ANSWER:
                self.ANSWER.remove(f"{choice.rstrip(choice[-1])}F")
            self.ANSWER.append(choice)
        elif choice in self.ANSWER and value == False:
            self.ANSWER.remove(choice)
            
    # Testing
    def reset_checkbox(self):
        for child in reversed(self.ids.first.children):
            if isinstance(child, CheckBox):
                child.active = False
        for child in reversed(self.ids.second.children):
            if isinstance(child, CheckBox):
                child.active = False
        for child in reversed(self.ids.third.children):
            if isinstance(child, CheckBox):
                child.active = False
        for child in reversed(self.ids.fourth.children):
            if isinstance(child, CheckBox):
                child.active = False
        for child in reversed(self.ids.fifth.children):
            if isinstance(child, CheckBox):
                child.active = False

    def on_next(self):

        # if non was selected append z to answers
        if len(self.ANSWER) == 0:
            self.last_q = int(self.ids.question1.text)
            #self.un_answered.append(self.last_q)
            for i in range(5):
                self.un_answered.append(self.last_q+i) 
            for num in self.un_answered:
                self.ANSWER.append(f"{num}Z")

        # Check for blank choice
        if len(self.ANSWER) < 5:
            self.last_q = int(self.ids.question1.text)
            for i in range(5):
               self.un_ans.append(self.last_q+i)

            for i in range(len(self.ANSWER)):       
                if int(self.ANSWER[i][:-1]) in self.un_ans:
                    self.un_ans2.append(int(self.ANSWER[i][:-1]))

            for nums in self.un_ans:
                if nums in self.un_ans2:
                    self.un_ans.remove(nums)
               
            for num in self.un_ans:
                self.ANSWER.append(f"{num}Z")


        # Append answer numbers to list of answers unsorted
        for i in range(len(self.ANSWER)):
            self.question_nums.append(int((self.ANSWER[i])[:-1]))

        # sort question's list and answer's list
        self.question_nums = sorted(self.question_nums)

        self.ANSWER = sorted(self.ANSWER)
        for i in self.question_nums:
            for l in range(len(self.question_nums)):
                if f"{i}" in self.ANSWER[l]:
                    self.final_answer.append(self.ANSWER[l])

        # Append answers to new list sorted
        for i in range(len(self.final_answer)):
            self.answer_sorted.append(self.final_answer[i][-1])

        # Update first question in second page of answer
        self.question_page += 1
        if self.question_page == 1:
            self.first_question = int(App.get_running_app().root.ids.screen1.ids.start_id.text) + 5
            self.first = int(App.get_running_app().root.ids.screen1.ids.start_id.text)

        # Update question numbers
        self.question1.text = str(self.first_question)
        self.question2.text = str(self.first_question + 1)
        self.question3.text = str(self.first_question + 2)
        self.question4.text = str(self.first_question + 3)
        self.question5.text = str(self.first_question + 4)

        # Update first question
        self.first_question = int(self.ids.question5.text) + 1

        
        # Open file and read as dictionary      
        file = open(f"answers/{self.ids.regionClue.text}.csv")
        self.reader = csv.DictReader(file)

        # Append answers to list
        for row in self.reader:
            if int(row["Question"]) in self.question_nums:
                self.marking_scheme.append(row["Answer"])
                self.quest.append(row["Question"])
        
        # Call check function
        score, med_score, _ = self.check()

        # Clear lists
        self.ANSWER.clear()
        self.final_answer.clear()
        self.question_nums.clear()
        self.un_answered.clear()
        self.un_ans.clear()

        # Close file
        file.close()

        # display score if last question answered
        if int(self.ids.question5.text)-5 == int(self.ids.limit.text):
            self.studyOver()
        self.parent.current = "questions"

        self.reset_checkbox()
        

    # Get current score
    def check(self):
        user_answer = self.answer_sorted
        mark_scheme = self.marking_scheme
        users_failures = self.quest
        self.total_answers += 5
        self.score = 0
        self.med_score = 0

        for n in range(len(user_answer)):
            # Check if user answer is correct
            if user_answer[n] == mark_scheme[n]:
                self.score += 1
                self.med_score += 1

            # Check if answer is wrong
            else:
                self.med_score -= 0.5
                if f"{self.quest[n]}. {mark_scheme[n]}" not in self.corrections:
                    self.corrections.append(f"{self.quest[n]}. {mark_scheme[n]}")

        return self.score, self.med_score, self.corrections

    def see_score(self):
        if self.hide_see.text == "See":
            self.score_id.text = str(self.score)
            self.hide_see.text = "Hide"
        else:
            self.hide_see.text = "See"
            self.score_id.text = ""
    
    def hide_score(self):
        self.hide_see.text = "See"
        self.score_id.text = ""

    def studyOver(self):

        correctionlist = listToString(self.corrections)
        
        justScore, medicosis, correct = self.check()

        App.get_running_app().root.ids.screen3.ids.congrats.text = f"Congratulations! Result for your work on {self.ids.regionClue.text}"
    
        App.get_running_app().root.ids.screen3.ids.total_questions.text = f"Total Questions tried {int(self.ids.question5.text)-4 - self.first}"

        App.get_running_app().root.ids.screen3.ids.final_score.text = f"Total Score {justScore}"

        App.get_running_app().root.ids.screen3.ids.final_medScore.text = f"Total Score Negative marking Scheme {medicosis}"
     
        
        App.get_running_app().root.ids.screen3.ids.final_percentage.text = f"{medicosis / len(self.answer_sorted) * 100} %"
      
        App.get_running_app().root.ids.screen3.ids.total_corections.text = "Questions failed and correct answers viz;"

        App.get_running_app().root.ids.screen3.ids.total_corections_list.text = f"{correctionlist}"

        self.parent.transition.direction = "down"
        self.parent.current = "result"

        
    def undo(self):
        if len(self.answer_sorted) == 0:
            exit("Can't go back!")

        # delete last 5 input from list
        for _ in range(5):
            if self.corrections:
                self.corrections.pop()
            self.answer_sorted.pop()
            self.quest.pop()
            self.marking_scheme.pop()

        # Call check to update scores
        score, med_score, _ = self.check()

        self.prev_question = int(self.ids.question5.text) - 9
        # Update question numbers
        self.question1.text = str(self.prev_question)
        self.question2.text = str(self.prev_question + 1)
        self.question3.text = str(self.prev_question + 2)
        self.question4.text = str(self.prev_question + 3)
        self.question5.text = str(self.prev_question + 4)

        self.first_question = self.prev_question + 5


class Mylayouthree(Screen):
    def end_all(self):
        exit("Study Session Over")
        


class WindowManager(ScreenManager):
    pass



class scoreSheet(App):
    def build(self):
        self.root = Builder.load_file("scoresheet.kv")
        return self.root

if __name__ == '__main__':
    scoreSheet().run()
