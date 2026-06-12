from tabulate import tabulate
import math
import pdb

def pop():
    while True:
      try:
        corps = int(input("What is the total student population of your school, or group of interest? "))
      except ValueError:
        print("Enter a whole number.")

      else:
        break

    return corps


def stud():

  # Validation for AY input
  while True:
    try:
      AY = int(input("What AY is it? Ex: AY26. Enter the two digit number only. "))
    except ValueError:
      print("Enter a whole number.")

    if len(str(AY)) != 2:
      print("Enter a two digit number.")
    else:
      break

  # Validation for Years of Teaching Input
  while True:
    try:
      yr_taught = int(input("How many years have you been teaching? "))
    except ValueError:
      print("Enter a whole number.")
    else:
      break

  AYdummy = AY # Use this as a dummy var for this loop.
  term_stud = {}
  class_stud = {}
  year_names = ["firsties (seniors)", "cows (juniors)", "yearlings (sophomores)" , "plebes (freshmen)"]
  seniors = []
  juniors = []
  sophomores = []
  freshmen = []
  classes = [seniors , juniors , sophomores , freshmen]

  # Collect how many terms in the period between now and when the current seniors arrived the instructor taught.
  while AYdummy > AY - yr_taught and AYdummy >= AY - 3: # Second catch here ensures we only check years that kids could still be at academy.
    AYdummy = AYdummy
    termcount = 3

    for _ in range(1 , termcount):
      while True:
        try:
          term = int(input(f"How many students did you teach in {AYdummy}-{_}? "))
        except ValueError:
          print("Enter a whole number.")
        else:
          break

      term_stud[f"{AYdummy}-{_}"] = term # AY-T is the KEY and students taught is the VALUE
    AYdummy -= 1

  print()
  print()
  print(f"To confirm, you report teaching the following number of students in the cooresponding academic year: ")
  print(f"{term_stud}")
  temp_list = []
  for key, value in term_stud.items():
    temp_list.append(int(key[:2]))

# Ok looking at validation here. there are two components that must be validated:
# 1: must validate that the entry is an int. that is straightforward.
# 2: must validated that the sum of each AY's students is equiv to the students previously reported for that AY.
# Thinking that we need to find a way to consolidate these into just one total expression with a for loop.
# could make a list of lists, where we are able to reference each list (senior,jrs, soph, fresh) as an item in a list perhaps named classes = [].
# classes = [seniors , juniors, etc.]
  indx = 0
  counter = 0
  flag = True
  for i in temp_list: # i is each AY, the first two digits only, stored as an int(). Ex: 26, 26, 25, 25. The Term (-1, -2s) have been seperated.
    # print(f"i: {i}")
    while i >= AY - 3 and flag == True:
      indx = AY - i
      for key, value in term_stud.items():
        valid_input_term_stud = False
        while valid_input_term_stud == False:
          valid_input_term_stud = True
          try:
            # print(f"first two of key: {int(key[:2])}")
            print()
            temp = input(f"How many of your {value} students in {key} were {year_names[indx:]}?\n Separate your values with a comma! ").split(",")

            nmbrs = [int(x) for x in temp] # x is each individual value (25, etc)
            total = sum(nmbrs)

            if len(nmbrs) != len(year_names[indx:]):
              print()
              print("Improper length- ensure you input only the number of students you were asked about for each term.")
              valid_input_term_stud = False
              continue

            elif total != value and int(key[:2]) == AY:
              print()
              print(f"Sum of students is not equal to {value}. Please try again.")
              valid_input_term_stud = False
              continue

            elif total > value:
              print()
              print(f"Sum of students exceeds {value}, your reported student count this term. Please try again.")
              valid_input_term_stud = False
              continue

            else: # Consider turning this into a "else"
              cls_indx = 0
              for x in nmbrs:
                classes[cls_indx].append(x)
                cls_indx += 1
              counter += 1

          except ValueError as e:
            print()
            print(f"Caught an error: {e}")
            valid_input_term_stud = False
            continue

        if counter % 2 == 0: # Only incr indx at end of AY, not term!
          indx += 1
        if counter >= len(temp_list) or counter == 8:
          break
      if counter >= len(temp_list) or counter == 8:
        flag = False

  # Removing these vars- not reqd but there were... a lot.
  del indx
  del counter
  del temp_list
  del temp
  del nmbrs
  del total
  del flag
  del cls_indx
  del valid_input_term_stud

  print()
  print()
  print("You have entered the following, by the students' currect class:")
  print(f"[seniors] , [juniors] , [sophomores] , [freshmen]")
  print(classes)
  print()

  class_stud[AY] = sum(seniors)
  class_stud[AY + 1] = sum(juniors)
  class_stud[AY + 2] = sum(sophomores)
  class_stud[AY + 3] = sum(freshmen)

  return class_stud

def display_stud(by_class):
  print()
  print()
  print(f"A summary of your taught cadet population that remains at USMA today is below. \n {tabulate(by_class.items(), headers=["Graduation Year", "Cadets"], tablefmt="pretty")}")
  print()
  print()
  cdts_remaining = sum(by_class.values())
  print(f"Total: {cdts_remaining}")
  return(cdts_remaining)


# Grp_size function is to determine what sizes of groups they're interested in for the binomials.
def grp_size(corps):
  grps=[]
  grps_dummy = True

  print("To prepare your final probability table- what size groups are you interested in?")
  print("These groups will be tabulated at the end with the probability that 1 or more cadets in that group is a cadet you've taught.")
  while grps_dummy == True:
    valid_input = False

    while valid_input == False:
      valid_input = True
      try:
        grp_value = (input("Input an integer value. When complete, input z to move on. "))

        if grp_value == "z":
          grps_dummy = False
          break

        val = int(grp_value)
        if val <= 0:
          print()
          print("Enter a positive integer.")
          valid_input = False
          continue

        elif val >= corps:
          print()
          print(f"Enter a value less than {corps}.")
          valid_input = False
          continue

        else:
          print()
          print(f"You entered a group size of {val} successfully. ")
          grps.append(val)


      except ValueError as e:
        print()
        print(f"Caught an error: {e}. Input a positive integer value.")
        continue

  print()
  print()
  print(f"You have entered the following group sizes: {grps}")
  return grps # Returns grps as a LIST

def binomials(user_groups , cadets_at_academy , corps):
  p_one = cadets_at_academy / corps
  p_zero = 1 - p_one
  p = p_one
  q = p_zero

  # p_none = {i: 1 - sum((p**n) * (q**(i - n)) for n in range(0, i + 1)) for i in user_groups}
  p_none = {i:round((1-p)**i,3) for i in user_groups}
  p_at_least_one = {i: round(1 - p_none[i],3) for i in user_groups}
  p_all = {i: round(((cadets_at_academy / corps)**i),3) for i in user_groups}

  return (p_none , p_at_least_one , p_all)

def near_certain(cadets_at_academy , corps ):
  p_one = cadets_at_academy / corps
  p_zero = 1 - p_one
  p = p_one
  q = p_zero

  # The below equation sets the "At Least one" binomial, (1-(1-p)**x >= .9999) and solves for x.
  # math.ceil rounds up
  x99 = int(math.ceil(math.log(.0001) / math.log(1 - p))) # number of cadets that you know at least 1 with 99.99% certainty

  x50 = int(math.ceil(math.log(.5000) / math.log(1 - p))) # number of cadets that you know at least 1 with 50.00% certainty

  return [x99 , x50]





def main():

  corps = pop()

  stud_by_class = stud() # Groups the user's student population by class

  cdts_remaining = display_stud(stud_by_class) # Builds the table and also sums up how many cadets remain at the academy.

  binom_grps = grp_size(corps) # Asks the user for group sizes of interest.

  none, at_least_one , all = binomials(binom_grps,cdts_remaining,corps) # Takes in the group sizes of interests and will use the cadets remaining at academy to calc probabilities.

  nc = near_certain(cdts_remaining,corps) # Calcs the number of studentss that must be in one place for there to be a 99.99% or greater chance that you know at least 1.

  print()
  print()
  print(f"The probability that NONE of the students in the cooresponding group sizes are students you have taught is summarized below. \n {tabulate(none.items(), headers=["Group Size", "Probability"], tablefmt="pretty")}")
  print()
  print()
  print(f"The probability that AT LEAST ONE of the students in the cooresponding group sizes are students you have taught is summarized below. \n {tabulate(at_least_one.items(), headers=["Group Size", "Probability"], tablefmt="pretty")}")
  print()
  print()
  print(f"The probability that ALL of the students in the cooresponding group sizes are students you have taught is summarized below. \n {tabulate(all.items(), headers=["Group Size", "Probability"], tablefmt="pretty")}")
  print()
  print()
  print(f"Once {nc[1]} cadets are gathered in one place there is a 50% chance you will know one or more of them. ")
  print()
  print()
  print(f"Once {nc[0]} cadets are gathered in one place there is a 99.99% chance you will know one or more of them. ")


# corps = 4400
if __name__ == "__main__":
    main()
