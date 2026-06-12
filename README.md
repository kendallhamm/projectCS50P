# README
## Do I know _any_ of you?
## Video Demo:  <[URL HERE](https://youtu.be/jsnsllYbn3o)>
## Problem Origin:
I always enjoy learning about a new statistical paradox. One specifically, The Birthday Paradox, is especially neat (and a fun icebreaker if you're in a new group of people). The Birthday Paradox is a statisical proof that, to be brief, shows that when you put only about 23 people in the same room you have a > 50% chance that 2 of them share a birthday. At first this is counterintuitive, given there are 365 possible birthdates (leap years are generally ignored for simplicity). But it's in fact true. More on the Birthday Paradox can be found here: [Birthday Problem Wikipedia](https://en.wikipedia.org/wiki/Birthday_problem).

I am an instructor at West Point and find often that although I have not actually had that many students in my class, I somehow see them around the campus all the time! To me this seemed very similar to the birthday problem. At any given time the number of students I have taught still enrolled sits at around ~200, and the student body is a constant 4400. I decided to use my CS50P project as an excuse to create a calculator that would tell the user what the probability that, given a group of students, any number of them were students you had previously taught.

## Program Design
This program consists of several functions and a main() function that calls each of them.

This program was written to assist me as an instructor at West Point. However, if you are looking to run similiar analysis on a different school's student body, it should work given that the school is a four year program. Throughout the code I use the variable
```python
corps
```
for the student body size. The student body at West Point is approximately 4400 cadets. If you can look beyond this variable name you should have no trouble repurposing this program for another institution.

### Assumptions
*   Assume that students always graduate with class. For example, a junior in Academic Year (AY) 25 will graduate as a senior in AY26. This is a critical assumption to keep this calculator easy to work with.
*   Assume that all groups are equally distributed across whatever population the user may have taught. Obviously, if the user has never taught students in a particular class and a group of 15 students in that untaught class are loitering in an area there is a 0% chance the user knows any of them. However, these situations are hard to model and control for. So for the purposes of this program we assume that all groups are equally likely to contain students of the population that the user taught.

### Pop()
This function is very simple. Originally I wasn't planning on including it.- I was going to hard code the student body size at 4400 (The size of the United States Corps of Cadets), but to enable this calculator to serve others who are interested in populations that are not 4400, it was an easy addition. It includes some simple validation techniques to ensure the user inputs a whole number.

### Stud()
This function begins the hard work here. Thinking through this problem gave me a few insights:


*   I needed to know how long the user had taught at the school.
*   I needed to know what quantity of students came from the varying classes, each term that the user taught. Seniors, Juniors, Sophomores, and Freshmen. At West Point these are Firsties (First Class Cadets), Cows, Yearlings, and Plebes.
*   I needed to then decompose the classes that the students were in when they were taught and place them into groups that classified them by their current class. For example, if I taught a senior 2 years ago I don't want to include that specific senior in the math for this problem, as that student's class has long since graduated. I wanted to ask the user for inputs by the class that they had the students and then wanted to group those students by their graduating year.
*   The best way to do this seemed to be dictionaries,  lists, and lists of lists.
*   No matter how long an instructor taught, we never needed to ask about more than 4 years worth of teaching history.
*   Each year going back in time we could ask about one less 'class' worth of information, because the higher class students would have graduated and moved on.

This function led me on a journey. The initial representation of the function is below. It is guilty of something I have learned to be a cardinal sin in programming- duplication. I ask the same question over and over. This version of stud() (we'll call it V1) worked but as soon as I started to think about implementing user input validation (make sure that each input was an integer, etc) I realized that I would probably be duplicating each of those checks as well.

There had to be a better way!


#### stud() V1

```python
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

#Something to think about here- can remove one input per AY if you calc the final one by summing others and subtracting from the total.
# Ok looking at validation here. there are two components that must be validated:
# 1: must validate that the entry is an int. that is straightforward.
# 2: must validated that the sum of each AY's students is equiv to the students previously reported for that AY.
# Thinking that we need to find a way to consolidate these into just one total expression with a for loop.
# could make a list of lists, where we are able to reference each list (senior,jrs, soph, fresh) as an item in a list perhaps named classes = [].
# classes = [seniors , juniors, etc.]
  for key, value in term_stud.items():
    if int(key[:2]) == AY:
      seniors.append(int(input(f"How many of your {value} students in {key} were {year_names[0]}? "))) # Current Seniors
      juniors.append(int(input(f"How many of your {value} students in {key} were {year_names[1]}? "))) # Current Juniors
      sophomores.append(int(input(f"How many of your {value} students in {key} were {year_names[2]}? "))) # Current Soph
      freshmen.append(int(input(f"How many of your {value} students in {key} were {year_names[3]}? "))) # Current Plebe
    elif int(key[:2]) == AY - 1:
      seniors.append(int(input(f"How many of your {value} students in {key} were {year_names[1]}? "))) # Current Seniors
      juniors.append(int(input(f"How many of your {value} students in {key} were {year_names[2]}? "))) # Current Juniors
      sophomores.append(int(input(f"How many of your {value} students in {key} were {year_names[3]}? "))) # Current Soph
    elif int(key[:2]) == AY - 2:
      seniors.append(int(input(f"How many of your {value} students in {key} were {year_names[2]}? "))) # Current Seniors
      juniors.append(int(input(f"How many of your {value} students in {key} were {year_names[3]}? "))) # Current Junior
    elif int(key[:2]) == AY - 3:
      seniors.append(int(input(f"How many of your {value} students in {key} were {year_names[3]}? "))) # Current Seniors

  class_stud[AY] = sum(seniors)
  class_stud[AY + 1] = sum(juniors)
  class_stud[AY + 2] = sum(sophomores)
  class_stud[AY + 3] = sum(freshmen)

  return class_stud

```

This led me to stud() V2. V2 was an improvement but man, was it clunky. You can see it significantly improved the duplication concern I had with V1 but it didn't work flawlessly and I was having issues nesting input validation inside of it. So we moved from V2 to stud() V3, which was not a massive overhaul like V1 -> V2, but still a bit of a lift.

#### stud() V2

```python
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


# could make a list of lists, where we are able to reference each list (senior,jrs, soph, fresh) as an item in a list perhaps named classes = [].
# classes = [seniors , juniors, etc.]
  # pdb.set_trace()
  indx = 0
  counter = 0
  print(temp_list)
  for i in temp_list: # i is each AY, the first two digits only, stored as an int(). Ex: 26, 26, 25, 25. The Term (-1, -2s) have been seperated.
    while i >= AY - 3:
      indx = AY - i
      print(f"Pre- for key, value loop: indx = {indx} (outside the loop)")
      for key, value in term_stud.items():
        print(f"i - indx: {i - indx}")
        if i - indx >= AY - 3:
          for classyear in year_names:
            try:
              # Check that each input is an int.
              temp = int(input(f"How many of your {value} students in {key} were {classyear}? "))
            except ValueError:
              sys.exit("Error: Enter a whole number.")
            classes[indx].append(temp)
          counter += 1

          if counter % 2 == 0: # Only increment indx at the end of a AY, not end of term!
            indx += 1
      print(counter)
      print(len(temp_list))
      if counter >= len(temp_list) or counter == 8:
        break
    if counter >= len(temp_list) or counter == 8:
      break



  print(classes)

   class_stud[AY] = sum(seniors)
  class_stud[AY + 1] = sum(juniors)
  class_stud[AY + 2] = sum(sophomores)
  class_stud[AY + 3] = sum(freshmen)

  return class_stud
```
stud() V3 ended up being my final solution here. I was able to use the modulo operator (%) correctly to iterate through both terms and years (there are two terms each year and I wanted to address each individually). I also was able to get my input validation features working here the way I wanted.

One user input that I am concerned with not being able to validate is the number of students by class, each term lists. Intially the user provides the total number of students that they taught each term. Let's say 100, each term for the last four terms (two years). For the first two terms I could ask how many were seniors, juniors, sophomores, and freshmen and then check that the sum of those values equals the reported 100. However, as we go back in time, because I made the design decision to only ask about the classes that mattered for the math problem, I could NOT use that summation technique for any years beyond the first.

An Example:

AY26-1: 100 Students taught. All Seniors.
AY26-2: 100 Students taught. All Seniors.
AY25-1: 100 Students taught. All Seniors.
AY25-2: 100 Students taught. All Seniors.

The lists for each year would look like this:

26-1: [100,0,0,0]

26-2: [100,0,0,0]

25-1: [0,0,0]

25-2: [0,0,0]

You can see that for AY26 I can check the sum of that list against the reported 100 students, but because in AY25 the seniors taught are not consequential to the math problem (because by AY26 they have graduated) I don't collect that information and therefore can't check the total.

One additional step that I added in to V3 that turned out to be unnecessary but I retained it in final design is the code block that deletes all the variables I initiated in the class collection loop. All of these variables would be 'forgotten' as soon as the function ended but I believe it was a good idea to delete them based on the quantity I initiated and the naming conventions I chose- they could easily be confused later on.

Lastly, I am certain there is a **much** more effective way to run this class collection loop inside the stud() function. I welcome any feedback to make this loop more pythonic and simplified! This design made sense to me and it worked.

#### stud() V3
```python
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


# could make a list of lists, where we are able to reference each list (senior,jrs, soph, fresh) as an item in a list perhaps named classes = [].
# classes = [seniors , juniors, etc.]
  indx = 0
  counter = 0
  flag = True
  breakpoint()
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
            temp = input(f"How many of your {value} students in {key} were {year_names[indx:]}?\n Separate your values with a comma! ").split(",")

            nmbrs = [int(x) for x in temp] # x is each individual value (25, etc)
            total = sum(nmbrs)

            if len(nmbrs) != len(year_names[indx:]):
              print("Improper length- ensure you input only the number of students you were asked about for each term.")
              valid_input_term_stud = False
              continue

            elif total != value and int(key[:2]) == AY:
              print(f"Sum of students is not equal to {value}. Please try again.")
              valid_input_term_stud = False
              continue

            else:
              cls_indx = 0
              for x in nmbrs:
                classes[cls_indx].append(x)
                cls_indx += 1
              counter += 1

          except ValueError as e:
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

  print(classes)

  class_stud[AY] = sum(seniors)
  class_stud[AY + 1] = sum(juniors)
  class_stud[AY + 2] = sum(sophomores)
  class_stud[AY + 3] = sum(freshmen)

  return class_stud

```

### display_stud()
display_stud() sums the lists of each graduation year (class) and uses the tabulate library to produce a table for the user to see how many cadets they have still at the academy. It also sums that table and returns the total number of cadets that the user has remaining at the academy for later use.

### grp_size()
grp_size() asks the user to imagine what groups they are interested in. For example, you approach a group of 6 cadets standing outside the library, or you see a platoon of 25 cadets doing physical training together. These group sizes are returned in a list and later entered as arguments into the binomial function.

### binomials()
binomials() function performs and returns three statistical calculations:

p_none: The probability that none of the cadets in the group size listed were the user's students in a previous term.

p_at_least_one: The probability that at least one of the cadets in the group size listed were the user's students in a previous term.

p_all: The probability that all of the cadets in the group size listed were the user's students in a previous term.

The mathematical formulation for these are below:

p_know one cadet = (number of cadets previously taught) / (student body size)

$$
n = \text{group size}
$$

$$
p_{\text{none}} = (1-p)^n
$$

$$
p_{\text{at least one}} = 1 - p_{\text{none}}
$$

$$
p_{\text{all}} = p^n
$$


### near_certain()
One additional step that I added in to this calculator that is, in my opinion, the **coolest** part is the near_certain() function. This function tells the user the number of students that must be gathered in one place to say that there is a 50% and a 99.99% chance that the user has taught one of them previously. This is the part of my problem that harkens back the closest to the Birthday Paradox- for an instructor with 200 of 4400 cadets remaining at the Academy only 15 students have to be gathered in one place to give the user a 50% chance of knowning one or more of them!

This is an algeabraic rearrangement of the p_none formula:

n <= (ln(1-certainty level)) / (ln(1-p))

Where:

n = Number of cadets that must be present

certainty level = certainty level of choice (in this calculator I chose to use 50% and 99.99%)

p = probability you know one cadet, or (number of cadets previously taught / student body size)

### main
main() arranges each of these preceding functions appropriately as arguments for each other and executes the program.
