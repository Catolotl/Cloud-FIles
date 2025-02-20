import array
import random

MAX_LEGNTH = 12

DIDGETS = ['0', '1','2','3','4','5','6','7','8','9']

LOCASE_LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

UPCASE_LETTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

SYMBOLS = ['@','#','$','%','=',':','?','.','/','|','~','>','*','(',')','<']

COMBINED_LIST = DIDGETS + LOCASE_LETTERS + UPCASE_LETTERS + SYMBOLS

rand_digit = random.choice(DIDGETS)
rand_upper = random.choice(UPCASE_LETTERS)
rand_lower = random.choice(LOCASE_LETTERS)
rand_symbol = random.choice(SYMBOLS)

temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

for x in range(MAX_LEGNTH - 4):

    temp_pass = temp_pass + random.choice(COMBINED_LIST)

    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)


password = ""

for x in temp_pass_list:
    password = password + x

print(f"Your random password is: {password}")