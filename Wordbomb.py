#features to add:
#-notifications for point changes?

#CREATORS NOTES
#-the rotator variable and associated code exist in order to speed up the loading of the next prompt. it does so by allowing for a qeue of prompts to generate while the player thinks and types, instead of generating only between guesses.


#---imports

import turtle, random

#---defining functions

#writes text
def write(message,fontsize,x,y,penum,alignment):
  wn.tracer(False)
  pens[penum].goto(x,y)
  pens[penum].write(message, font=('impact', fontsize, 'bold'), align=alignment)
  if penum == 2:
    wn.ontimer(noti_clear, 800)
  wn.tracer(True)

#writes text, clears previous text
def writeC(message,fontsize,x,y,penum,alignment):
  wn.tracer(False)
  pens[penum].clear()
  pens[penum].goto(x,y)
  pens[penum].write(message, font=('impact', fontsize, 'bold'), align=alignment)
  if penum == 2:
    wn.ontimer(noti_clear, 800)
  wn.tracer(True)

#clears the notification pen
def noti_clear():
  pens[2].clear()

#displays the current guess
def dispinput():
  global input
  writeC(input,45,-450,0,0,'left')

#adds extra time to timer
def updatetime():
  global deltatime, timer
  timer += deltatime
  strtime = str(timer)
  if len(strtime) == 2:
    strtime = "0" + strtime
  elif len(strtime) == 1:
    strtime = "00" + strtime
  writeC(strtime,25,-300,200,4,'center')
  deltatime = 0

#displays previously used words for this prompt
def dispused(prompt):
  cordx = -400
  cordy = -100
  pens[6].clear()
  for word in used:
    if prompt == word[:3]:
      write(word,25,cordx,cordy,6,'left')
      cordy -= 35


#adds points to the score
def updatescore():
  global points, deltapoints
  points += deltapoints
  strpoints = points
  negative = False
  if strpoints < 0:
    negative = True
    strpoints = abs(strpoints)
  strpoints = str(strpoints)
  if negative == True:
    if len(strpoints) == 2:
        strpoints = "-" + strpoints
    elif len(strpoints) == 1:
      strpoints = "-0" + strpoints
  else:
    if len(strpoints) == 2:
      strpoints = "0" + strpoints
    elif len(strpoints) == 1:
      strpoints = "00" + strpoints
  writeC(strpoints,25,300,200,3,'center')
  deltapoints = 0

#displays the three prompted letters (and hints)
def dispprompt():
  global prompt, alter
  if alter == 1:
    writeC(prompt1,45,-450,0,1,'left')
    dispused(prompt1)
  if alter == 2:
    writeC(prompt2,45,-450,0,1,'left')
    dispused(prompt2)
  if alter == 3:
    writeC(prompt3,45,-450,0,1,'left')
    dispused(prompt3)
  if alter == 4:
    writeC(prompt4,45,-450,0,1,'left')
    dispused(prompt4)

#processes letterkey and delete inputs
def pressed(letter):
  global input, pressable, started
  if started == True:
    letter = letter.upper()
    if pressable == True:
      pressable = False
      if letter == 'DELETE':
        input = input[:(len(input) - 1)]
      else:
        input = input + letter
      dispinput()
      pressable = True

#returns a random 3 letter prompt, for the specified rotation
def randprompt(rotator):
  global vowels, consonants, prompt1, prompt2, prompt3, prompt4
  prompt = ''
  available = ['CCV','CVC','CVV','VCV','VCC']
  template = random.choice(available)
  for letter in template:
    if letter == 'C':
      prompt += random.choice(consonants)
    if letter == 'V':
      prompt += random.choice(vowels)
  prompt = prompt.upper()
  if rotator == 1:
    prompt1 = prompt
  elif rotator == 2:
    prompt2 = prompt 
  elif rotator == 3:
    prompt3 = prompt
  elif rotator == 4:
    prompt4 = prompt
  return prompt

#find the words containing the three letter prompt
def findwords(rotator):
  global goodwords1, goodwords2, goodwords3, goodwords4, words
  if rotator == 1:
    goodwords1 = []
    while len(goodwords1) < 20:
      goodwords1 = []
      prompt = randprompt(rotator)
      for word in words:
        if word[:3] == prompt:
          goodwords1.append(word)
  if rotator == 2:
    goodwords2 = []
    while len(goodwords2) < 20:
      goodwords2 = []
      prompt = randprompt(rotator)
      for word in words:
        if word[:3] == prompt:
          goodwords2.append(word)
  if rotator == 3:
    goodwords3 = []
    while len(goodwords3) < 20:
      goodwords3 = []
      prompt = randprompt(rotator)
      for word in words:
        if word[:3] == prompt:
          goodwords3.append(word)
  if rotator == 4:
    goodwords4 = []
    while len(goodwords4) < 20:
      goodwords4 = []
      prompt = randprompt(rotator)
      for word in words:
        if word[:3] == prompt:
          goodwords4.append(word)

#alternates the current rotation, re-generates the new prompt
def alternate():
  global alter
  if alter == 1:
    findwords(1)
    alter = 2
  elif alter == 2:
    findwords(2)
    alter = 3
  elif alter == 3:
    findwords(3)
    alter = 4
  elif alter == 4:
    findwords(4)
    alter = 1
  dispprompt()

#starts the game from menu
def start(x,y):
  global started
  if started == False:
    started = True
    wn.ontimer(ticked, 1000)
    pen.clear()
    write('Score:',25,300,240,5,'center')
    write('Time:',25,-300,240,5,'center')
    write('Record:',25,0,240,5,'center')
    write(record,25,0,200,5,'center')
    dispprompt()
    updatetime()
    updatescore()

#processes enter command, checks guess against wordlist
def enter():
  global input, hint, alter, goodwords1, goodwords2, goodwords3, goodwords4, deltapoints, deltatime, used, started
  if started == True:
    correct = False
    if (alter == 1) and (input in goodwords1) and (input not in used):
      correct = True
    if (alter == 2) and (input in goodwords2) and (input not in used):
      correct = True
    if (alter == 3) and (input in goodwords3) and (input not in used):
      correct = True
    if (alter == 4) and (input in goodwords4) and (input not in used):
      correct = True
    if correct == True:
      used.append(input)
      alternate()
      hint = ''
      length = len(input)
      if length == 5:
        deltapoints = 1
        deltatime = 1
      else:
        deltapoints = length
        deltatime = int(length / 2)
    if correct == False:
      if len(input) < 4:
        writeC("TOO SHORT",20,-400,-40,2,'center')
      elif (alter == 1) and (input not in goodwords1):
        writeC("NOT IN WORDLIST",20,-400,-40,2,'center')
        deltapoints -= 1
      elif (alter == 2) and (input not in goodwords2):
        writeC("NOT IN WORDLIST",20,-400,-40,2,'center')
        deltapoints -= 1
      elif input in used:
        writeC("ALREADY USED",20,-400,-40,2,'center')
    input = ''
    dispinput()
    updatescore()
    updatetime()

#takes escapekey inputs, skips current prompt
def skip():
  global input, hint, deltapoints, started
  if started == True:
    input = ''
    hint = ''
    deltapoints = -5
    updatescore()
    dispinput()
    alternate()

#takes tabkey inputs, generates a hint letter
def givehint():
  global hint, alter, prompt1, prompt2, prompt3, prompt4, goodwords1, goodwords2, goodwords3, goodwords4, deltapoints, started
  if started == True:
    if alter == 1:
      if hint == '':
        hint = random.choice(goodwords1)
      if len(prompt1) < len(hint):
        prompt1 += hint[len(prompt1)]
    if alter == 2:
      if hint == '':
        hint = random.choice(goodwords2)
      if len(prompt2) < len(hint):
        prompt2 += hint[len(prompt2)]
    if alter == 3:
      if hint == '':
        hint = random.choice(goodwords3)
      if len(prompt3) < len(hint):
        prompt3 += hint[len(prompt3)]
    if alter == 4:
      if hint == '':
        hint = random.choice(goodwords4)
      if len(prompt4) < len(hint):
        prompt4 += hint[len(prompt4)]
    dispprompt()
    dispinput()
    deltapoints = -1
    updatescore()

#counts down the clock every second
def ticked():
  global timer, flashing
  if started == True:
    if timer <= 0:
      end()
      if flashing == False:
        flash()
      return
    else:
      timer -= 1
      updatetime()
  wn.ontimer(ticked, 1000)

#ends the game, closes program 5 seconds later
def end():
  global points, record, started
  if points > record:
    records = open('records.txt', 'w')
    records.write(str(points))
  started = False
  enter()
  wn.ontimer(altf4, 5000)

#closes program (needed to avoid error)
def altf4():
  exit()

#flashes the clock after game ends
def flash():
  global colour, flashing
  flashing == True
  if colour == 'blue':
    colour = 'red'
  elif colour == 'red':
    colour = 'blue'
  ttimer.color(colour)
  updatetime()
  wn.ontimer(flash, 250)

#---defining variables

wn = turtle.Screen()
flashing = False
input = ''
pressable = True
alter = 1
points = 0
timer = 60
deltatime = 0
deltapoints = 0
hint = ''
started = False
colour = 'blue'

#defining lists

abcs = list('abcdefghijklmnopqrstuvwxyz')
vowels = list('euioa')
consonants = list('qwrtypsdfghjklzxcvbnm')
colors = ['white','gray','red','gold', 'blue','white','white']
pens = []
used = []
words = []

with open('words_3.txt', 'r') as f:
  wordst = f.readlines()
for word in wordst:
  words.append(word.strip())

with open('records.txt', 'r') as f:
  record = f.readlines()
record = record[0].strip()
record = int(record)

#---creating turtles

wn.tracer(False)

wn.bgcolor('black')


pen = turtle.Turtle()
pens.append(pen)

backpen = turtle.Turtle()
pens.append(backpen)

notifications = turtle.Turtle()
pens.append(notifications)

scoreboard = turtle.Turtle()
pens.append(scoreboard)

ttimer = turtle.Turtle()
pens.append(ttimer)

ui = turtle.Turtle()
pens.append(ui)

usedpen = turtle.Turtle()
pens.append(usedpen)

for n, tortle in enumerate(pens):
  tortle.hideturtle()
  tortle.penup()
  tortle.speed(0)
  tortle.color(colors[n])

#---Preloading word sets

for i in range(4):
  findwords(i + 1)

#---printing start menu

write("CLICK TO START",50,0,-290,0,'center')
write("YOU HAVE ONE MINUTE",60,0,200,0,'center')
write("YOU ARE PROVIDED THREE LETTERS",30,0, 160,0,'center')
write("YOU MUST CREATE A WORD WITH THEM",30,0, 120,0, 'center')
write("MINUMUM WORD LENGTH IS 4",30,0, 80,0, 'center')
write("WORDS ARE SCORED ON LENGTH", 30,0, 40,0, 'center')
write("EXTRA TIME IS ALLOTED BY LENGTH", 30,0, 0,0, 'center')
write("YOU MAY NOT REUSE WORDS", 30,0, -40,0, 'center')
write("ESCAPE: SKIP",30,0,-120,0,'center')
write("TAB: HINT",30,0,-160,0,'center')
write("RETURN: ENTER",30,0,-200,0,'center')

wn.tracer(True)

#---inputs

wn.listen()

for letter in abcs:
  wn.onkeypress(lambda a=letter: pressed(a), letter)

wn.onkeypress(lambda: pressed('delete'), 'BackSpace')
wn.onkeypress(enter, 'Return')
wn.onkeypress(skip, 'Escape')
wn.onkeypress(givehint, 'Tab')

wn.onclick(start)

wn.mainloop()