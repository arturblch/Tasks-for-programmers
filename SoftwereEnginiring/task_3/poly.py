# Написать функцию на питоне, определяющую палендомы, без учета цыфр и символов. Нельзя использовать циклы! 

def check_poly(text):
    text = "".join(list(filter(lambda a: a.isalpha(), text))).lower()
    return text == text[::-1]


assert check_poly("казак") == True
assert check_poly("asd") == False
assert check_poly("_Ab54ba") == True  # четное число
assert check_poly("_ab5a_") == True  # не четное число
