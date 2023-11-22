# import random

# def guess_the_number():
#     secret_number = random.randint(1, 100)
    
#     attempts = 3

#     for attempt in range(attempts):
#         guess = int(input("Enter your guess (between 1 and 100): "))
        
#         if guess == secret_number:
#             print("Congratulations! You guessed the correct number.")
#             break
            
#         else:
#             attempts_left = attempts - (attempt + 1)
#             if attempts_left > 0:
#                 print(f"Wrong guess! You have {attempts_left} {'attempts' if attempts_left > 1 else 'attempt'} left.")
#                 if guess < secret_number:
#                     print(' guess number is less than secreat number')
                    
#                 elif guess > secret_number:
#                     print("guess number is greater tha secrete number") 
#             else:
#                 print(f"nikal yaha se dikhai mt dena. The correct number was {secret_number}.")

# if __name__ == "__main__":
#     guess_the_number()


def find_missing_number():

    N=10
    array=[1,4,4,5,3,6,9,11,15,2,1,2,2]

    missing=[]
    repeat=None
    outside=[]

    for i in range(1,N+1):
        if i not in array:
            missing.append(i)
    print(missing)

    for i in array:
        count=array.count(i)

        if count>1:
            repeat=i
        if i>N:
            outside.append(i)
    print(outside,repeat)


if __name__ == "__main__":
    find_missing_number()

