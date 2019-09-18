def pass_the_parcel(parcel):
    number_of_gifts = len(parcel)
    person_to_receive_gift = 1
    for i in range(number_of_gifts, 0, -1):
        gift = parcel[i]
        print("Person " + str(person_receive_gift) + " got " + gift + "!")
        person_to_recieve_gift += 1
    print("The parcel is empty!")
