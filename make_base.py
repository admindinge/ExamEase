import sqlite3
import os
import shutil

class Question:
    def __init__(self, question_text, answer_choices, correct_answer,current_difficulty):
        self.question_text = question_text
        self.answer_choices = answer_choices
        self.correct_answer = correct_answer
        self.current_difficulty = current_difficulty

def create_database():
    conn = sqlite3.connect('questions_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (question_text TEXT, answer_choices TEXT, correct_answer TEXT, difficulty TEXT)''')
    conn.commit()
    conn.close()

def is_question_unique(question):
    conn = sqlite3.connect('questions_db.db')
    c = conn.cursor()
    c.execute("SELECT question_text FROM questions WHERE question_text = ?", (question.question_text,))
    existing_question = c.fetchone()
    conn.close()
    return existing_question is None

def add_question(question):
    message_record_exist = "ეს კითხვა უკვე არსებობს ბაზაში და აღარ დაემატება"
    if is_question_unique(question):
        conn = sqlite3.connect('questions_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO questions VALUES (?, ?, ?, ?)", (question.question_text, "\n".join(question.answer_choices), question.correct_answer,question.current_difficulty))
        conn.commit()
        conn.close()
    else:
        print(message_record_exist)

def add_questions_from_text_files(directory):
    output_directory = "processed_questions"
    search_difficulty_text = "სირთულე: "
    search_correct_text = "პასუხი: " 
    search_question_text = "კითხვა: "   
    os.makedirs(output_directory, exist_ok=True)

    current_difficulty = None
    current_question_text = ""
    current_answer_choices = []
    current_correct_answer = None

    for filename in os.listdir(directory):
        if filename.startswith("questions") and filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                counter = 0
                for line in lines:
                    line = line.strip()
                    if line:
                        if line.startswith(search_difficulty_text):
                            current_difficulty = line.split(search_difficulty_text)[1].strip()
                            
                        elif line.startswith(search_correct_text):
                            current_correct_answer = line.split(search_correct_text)[1].strip()
                            if current_difficulty and current_question_text and current_answer_choices and current_correct_answer:
                                counter += 1
                                print(f"ჩავწერე {counter}")
                                question = Question(current_question_text, current_answer_choices, current_correct_answer, current_difficulty)
                                add_question(question)
                                current_answer_choices = []
                        elif line.startswith(search_question_text):
                                current_question_text =  line.split(search_question_text)[1].strip()
                        # elif line[1] == ')':
                        else:
                            current_answer_choices.append(line)
                    
    shutil.move(os.path.join(directory, filename), os.path.join(output_directory, filename))

if __name__ == "__main__":
    create_database()
    
    questions_directory = "questions_files"
    add_questions_from_text_files(questions_directory)
    
    
