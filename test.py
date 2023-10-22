import sqlite3
import random

message_input_answer = "\n \33[31m ᲨᲔᲛᲝᲘᲧᲕᲐᲜᲔ ᲞᲐᲡᲣᲮᲘ ᲨᲔᲓᲔᲒᲘ ᲡᲘᲛᲑᲝᲚᲔᲑᲘᲓᲐᲜ : \33[0m"
message_answer_is_correct = "\n\33[43m\33[32m\n\n Პ Ა Ს Უ Ხ Ი    Ს Წ Ო Რ Ი Ა \n\33[0m\n"
message_answer_is_wrong = "\n\33[41m\33[34m\n\n Შ Ე Ც Დ Ო Მ Ა Ა ! ᲡᲬᲝᲠᲘ ᲞᲐᲡᲣᲮᲘᲐ: \33[0m" 
warning_uncorect_input = "\n\33[41m\33[34m\n\n ᲐᲠᲐᲙᲝᲠᲔᲥᲢᲣᲚᲘ ᲐᲠᲩᲔᲕᲐᲜᲘᲐ, ᲨᲔᲛᲝᲘᲧᲕᲐᲜᲔᲗ ᲡᲘᲛᲑᲝᲚᲝ ᲛᲝᲪᲔᲛᲣᲚᲘ ᲡᲘᲘᲓᲐᲜ!  \n\33[0m" 

# ბაზასთან დაერთება (გლობალი მჭირდება ?)
conn = sqlite3.connect('questions_db.db')
c = conn.cursor()

# ფუნქცია ბაზიდან წამოიღებს განსაზღვრულ რაოდენობა შემთხვევით კითხვას
def select_random_questions(number_of_questions):
    c.execute('SELECT question_text, answer_choices, correct_answer FROM questions ORDER BY RANDOM() LIMIT ?', (number_of_questions,))
    questions = c.fetchall()
    return questions


def get_valid_input(valid_characters):
    while True:
        user_input = input(f"{message_input_answer} ({', '.join(valid_characters)}): ")
        if len(user_input) == 1 and user_input in valid_characters:
            return user_input
        else:
            print(warning_uncorect_input)


# ვირჩევთ 10 შემთხვევით კითხვას

selected_questions = select_random_questions(10)

# პროგრამაში გამოყენებული მესიჯები გამოტანილია ცვლადებში, რათა შესაძლებელი იყოს მათი მოხერხებულად ცვლილება



# ტესტის დასაწყისი
score = 0
for question_data in selected_questions:
    question_text, answer_choices, correct_answer = question_data
    

    print("\n\33[32m" + question_text + "\33[0m\n")
    print("\n\33[34m" + answer_choices.replace('\n', '\n\n')+ "\33[0m\n")
    

    valid_characters = ['a', 'b', 'c', 'd']
    user_answer = get_valid_input(valid_characters)
    if user_answer == correct_answer:
        print(message_answer_is_correct)
        score += 1
    else:
        print(f"{message_answer_is_wrong} {correct_answer} \33[41m\33[34m\n\33[0m")
        
        
        

print(f"Вы ответили правильно на {score} из 10 вопросов.")
