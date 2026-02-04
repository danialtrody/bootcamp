a: int = int(input("Enter first number (a): "))
b: int = int(input("Enter second number (b): "))
c: int = int(input("Enter third number (c): "))
print(f"a = {a}, b = {b}, c = {c}\n")


print("Is a equal to c?", a == c)
print("Is a less than b?", a < b)
print("Is b greater than or equal to a?", b >= a)
print("Is a not equal to b?", a != b)
print("Are both a < b AND b > c true?" , a < b and b > c)
print("Is at least one true: a > b OR a == c?", a > b or a == c)
print("Is it NOT true that a equals b?", not a == b ,"\n")


word1: str = input("Enter first word: ")
word2: str = input("Enter second word: ")
print(f"word1 = {word1}, word2 = {word2}\n")


print("Are the strings equal?", word1 == word2)
print("Are the strings equal (lowercase)?", word1.lower() == word2.lower())
print("Length of word1:", len(word1))