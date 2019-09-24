# Name: Mya Hussain 
# Date: 2018-06-04
# File Name: hangman.py
# Description: This program allows you to play the game hangman on a GUI
# using a list of secret words. It allows you to edit the secret list,
# play again, view instructions and quit. When a game ends the user 
# can no longer input letters, the program error checks all input statements.
# Test cases: Tested all functions, buttons and frames, they printed
# results/preformed successfully.

#Import libraries 
from tkinter import * 
from tkinter import messagebox
import random 


#Variables needed globally 
master_list = ["awkward","pixel", "croquet", "taco", "beryllium"]
score = 0 
incorrectGuesses = 0 
incorrectGuessValue = []
guessed = []
word = []
submission = StringVar
alreadyguessed = []


#class that creates a tkinter object 
class mainpage(Tk):

    #global variables 
    global guessed
    global word
    

    #declare a constructor to create an instance/object for this class 
    def __init__(self, *args, **kwargs):
        #this object is the GUI window created below, 
        #this is called via the 'self' keyword refering to the object of x instance
        Tk.__init__(self, *args, **kwargs)

        #set basic properties for window 
        self.title("HANGMAN GAME")
        self.geometry("800x700")

        #Make and place a frame using pack, put the frame in the window 
        #let the frame take the shape of the window by expanding and filling
        container = Frame(self)
        container.pack(side = "top", fill ="both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)


        #make a dictionary of frame objects to store different pages
        self.frames = {}

        #For each frame (page) put it in the container and add it to the dict
        for every_frame in (startpage, instructions, settings):

            #make an instance of each frame using the constructor 
            frame = every_frame(container, self)

            #add frame to the list under its name 
            self.frames[every_frame] = frame 

            #put the frame on the application window 
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        # __init__ is run when program launches thus, 
        # initialize the page shown to startpage
        self.show_frame(startpage)

    #This function raises a given frame 
    #This will create the illusion of new pages and tabs by raising frames
    def show_frame(self, framename ):
        #store the frame to be raised in a variable
        frame = self.frames[framename]
        #raise the frame to make it visable to user vis tkraise method
        frame.tkraise()
        
# frame object 
class startpage(Frame):

    global submission

    #Self is the current object, parent is the widget for the current object
    #The controller allows us to interact by being a common value between pages
    #Parent is variable 'container', controller is the Tk window 
    def __init__(self, parent, controller):
        #make the frame 
        Frame.__init__(self, parent)
        self.config(bg = "white")
        
         #Quit button, declare and pack
        self.quitbutton = Button(self, text = "Quit", command = quit)
        self.quitbutton.pack(side = LEFT, anchor = N, fill = X, expand = YES)

        #Instruction button, declare and pack 
        self.instructionbutton = Button(self, text = "Instructions", \
            command = lambda:controller.show_frame(instructions))
        self.instructionbutton.pack(side = LEFT, anchor = N, fill = X, expand = YES)

        #setting button, declare and pack 
        self.settingbutton = Button(self, text = "Settings", \
            command =lambda:controller.show_frame(settings))
        self.settingbutton.pack(side = LEFT, anchor = N, fill = X, expand = YES)
       
        #make and place game labels 
        welcomelabel = Label(self, text = "Welcome to...", font = "Ariel 18 italic", \
            bg = "lightyellow")
        welcomelabel.place(x = 350, y = 70 )
        titlegame = Label(self, text ="Hangman", font = "Ariel 45 bold italic", bg ="pink",\
           fg ="steelblue")
        titlegame.place(x = 406 , y = 100 )

        #score and incorrect guess labels 
        self.Scorelabel = Label(self, text = "Score: " + str(score), font = "Ariel 15", bg = "lightgreen")
        self.Scorelabel.place(x = 370, y = 220)
        message = "Incorrect Guesses: " + str(incorrectGuesses)
        self.incorrectlabel = Label(self, text = message, font = "Ariel 15", bg = "palevioletred")
        self.incorrectlabel.place( x = 513, y = 220)

        #make label for textbox and textbox to display missing letters 
        message1 = "The secret word is " + str(len(guessed)) + " characters long:" 
        self.boxy = Label(self, text = message1 , font ="Ariel 15")
        self.boxy.place(x = 370, y = 260)
        self.letterz = Label(self, text = guessed, font = "ariel 15")
        self.letterz.place(x = 370, y = 290)

        #enter box and enter box label 
        self.entery = Label(self, text = "Enter your guess below", font = "ariel 15")
        self.entery.place(x = 370, y = 340)
        
        self.textentry = Entry(self, width = 30, highlightbackground = "#8E82FE")
        self.textentry.place(x = 370, y = 380)
        

        #Button to activate entry box 
        self.submit = Button( self, text ="Press to submit", command = self.getinput)
        self.submit.place( x = 370, y = 400)

        #get entry (all buttons because mac and windows have different assignment)
        #self.submit.bind("<Button-3>", self.getinput)
        #self.submit.bind("<Button-2>", self.getinput)
        #self.submit.bind("<Button-1>", self.getinput)

        #THEN on rightclick evaluate responce
        #self.submit.bind("<Button-3>", game)
        #self.submit.bind("<Button-1>", game)
        #self.submit.bind("<Button-2>", game)

        #label with previously guessed letters 
        self.guessedlabel = Label(self, text = "Guessed letters:", font = "ariel 15")
        self.guessedlabel.place(x = 370, y = 440 )

        #make canvas to draw hangman 
        self.can = Canvas(self, width = 280, height = 430, highlightbackground = "mediumturquoise")
        self.can.place(x = 50, y = 68)
    
        #draw noose for man to be hanged on 
        pole = self.can.create_line(50 , 45 , 50 , 350, width = 5, fill = "black")
        rod = self.can.create_line(50 , 45 , 145 , 45, width = 5, fill = "black")
        rope = self.can.create_line(145 , 45 , 145 , 100, width = 5, fill = "black")
        base = self.can.create_line(35 , 350 , 200 , 350, width = 5, fill = "black")
        
        #draw man ( he is 'invisible' until told otherwise ) 
        self.head = self.can.create_oval(110, 100, 180, 170, width = 3, outline = "white")
        self.leftarm = self.can.create_line(190 , 240 , 145, 200, width = 5, fill = "white")
        self.rightarm = self.can.create_line(100 , 240 , 145 , 200, width = 5, fill = "white")
        self.leftleg = self.can.create_line(145 , 270 , 100 , 340, width = 5, fill = "white")
        self.rightleg = self.can.create_line(145 , 270 , 190 , 340, width = 5, fill = "white")
        self.body = self.can.create_line(145 , 170 , 145 , 270, width = 5, fill = "white")

        #Win lose label 
        self.winlose = Label(self, font = "couriernew 100", bg ="white")
        self.winlose.place(x= 165, y = 510)

        #again button, declare and pack 
        self.settingbutton = Button(self, text = "Play Again", 
                                    command = lambda a = self.submit, 
                                    b= self.guessedlabel, 
                                    c= self.incorrectlabel, 
                                    d= self.Scorelabel, 
                                    e= self.letterz, 
                                    f= self.can, 
                                    g =self.head, 
                                    h= self.body, 
                                    i = self.leftarm, 
                                    j= self.rightarm, 
                                    k =self.leftleg, 
                                    l= self.rightleg, 
                                    m = self.winlose, 
                                    n = self.boxy :self.again(a,b,c,d,e,f,g,h,i,j,k,l,m,n))
        self.settingbutton.pack(side = LEFT, anchor = N, fill = X, expand = YES)

        #when the user enters something, store, check, and execute game functions 
    def getinput (self): 
        global submission
        submission = str(self.textentry.get())
        print(submission)
        
        valid = check4validSubmission()
        winlose1 = False

        if (valid):
            if (not winlose1):
                checksubmission(self.guessedlabel, self.incorrectlabel, self.Scorelabel, \
                    self.letterz)
                hangman(self.can, self.head, self.body, self.leftarm, self.rightarm, \
                    self.leftleg, self.rightleg )
                winlose1 = winlose(self.winlose, self.submit,self.Scorelabel)
        else:
            print("invalid input")

    def again (self, submitbutton, guessedLabel, incorrectLabel, scoreLabel, missingwordlabel, \
        canvas, head, body, arm1, arm2, leg1, leg2, resultlabel, boxy):
        global score
        global guessed
        global word
        global master_list
        global incorrectGuesses
        global incorrectGuessValue
        global alreadyguessed
    
        #are you sure 
        message1 = "This will delete your current game, are you sure you want to continue"
        choice = messagebox.askyesno("Are you sure", message1)

        if choice:
            #reset to inital values 
            score = 0 
            incorrectGuesses = 0 
            incorrectGuessValue = []
            guessed = []
            word = []
            submission = StringVar
            alreadyguessed = []

            #get new word 
            guessed, word = get_word(master_list)

            #update screen values 
            guessedLabel.config(text = "Guessed letters: " + str(incorrectGuessValue))
            scoreLabel.config(text = "Score: " + str(score))
            incorrectLabel.config(text = "Incorrect Guesses: " + str(incorrectGuesses))
            missingwordlabel.config(text = guessed)
            message2 = "The secret word is " + str(len(guessed)) + " characters long:" 
            boxy.config( text = message2 )

            #clear hangman  
            canvas.itemconfig(head, outline ="white")
            canvas.itemconfig(body, fill ="white")
            canvas.itemconfig(arm2, fill ="white")
            canvas.itemconfig(arm1, fill ="white")
            canvas.itemconfig(leg1, fill ="white")
            canvas.itemconfig(leg2, fill ="white")

            #give button functionality again
            submitbutton.config(command = self.getinput)

            #get rid of result message 
            resultlabel.config( text = "", borderwidth = 0, relief = GROOVE)
            resultlabel.config( fg = "white")



class instructions(Frame):

    #Make a frame inside the controller
    def __init__(self, parent, controller):
        #Make the frame, the frame is self 
        Frame.__init__(self, parent)
        self.config(bg = "pink")

        #Make a back button and pack it 
        back = Button(self, text = "Click to go back", \
            command = lambda:controller.show_frame(startpage))
        back.place( x = 35, y = 600)
        
        #add a label 
        label = Label(self, text ="Instructions", font= "ariel 40 italic" )
        label.pack(padx = 10, pady = 10)

        #write instructions
        instruction = '''
        1) The player tries to guess all the letters in a secret word. 
        2) As one guesses correctly, letters are revealed.
        3) The player can only guess an incorrect letter five times before the man is hung. 
        4) User gets bonus points for guessing letters that reoccur throughout the word.
        5) The player can add secret words to the app in settings. 
        '''
        #Show instructions
        self.label1 = Label(self, text = instruction, font = "Vendana 14", borderwidth = 4, \
            relief = GROOVE)
        self.label1.place(x = 35, y =90)


class settings(Frame):

    #So the user can change it in this frame
    global master_list

    #Make a frame inside the controller 
    def __init__(self, parent, controller):
        #Make the frame, the frame is self 
        Frame.__init__(self, parent)
        self.config(bg = "#63D297")

        #make back button and pack it
        backk = Button(self, text="Click to go back", \
            command = lambda:controller.show_frame(startpage))
        backk.place( x = 30, y = 600)

        #labels and button to submit word to the master list 
        label = Label(self, text = "Settings", font = "Ariel 40 italic")
        label.pack(padx = 10, pady = 10)
        message1 = "To add to the list of secret words, enter a value below: "
        label1 = Label(self, text = message1, font = "Ariel 15")
        label1.place( x =30 , y = 100 )
        self.enterboxy = Entry(self, width = 20)
        self.enterboxy.place( x = 30, y = 145)
        self.submit1 = Button(self, text= "Press to submit", command = self.getinput2)
        self.submit1.place( x = 165, y = 140 )

        #label displaying info to screen 
        message2 = "To play with new words added, push the play again button on the homepage"
        label2 = Label(self, text = message2, font ="ariel 15")
        label2.place(x = 30, y = 250)

    def getinput2 (self):
        possibilities = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
        possibilities += ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        newword = str(self.enterboxy.get())
        newword = newword.strip().lower()

        #if user enters something long and annoying stop them because why not 
        if (len(newword) > 20):
            message1 = "That word is quite long, try to keep the secret word under 20 characters"
            messagebox.showinfo("Long Word", message1)

        # if user enters nothing, inform them 
        elif (newword == ""):
            messagebox.showinfo("No input", "please enter something before submitting")
        
        else: 
            checkCount = 0
            #Check to see if the word has no numbers or weird characters
            #For every letter 
            for x in range(len(newword)):

                #check to see if its in our list of alphabet 
                for i in possibilities:
                    number = False
                    # if it is count it as proper input 
                    if (newword[x] == i):
                        number = True
                        checkCount += 1
 
                    
            #If everything was successfully checked and passed, add the word 
            if checkCount == len(newword):
                master_list.append(newword)
                messagebox.showinfo("Success","your word has been added")

            #Else report to user
            else: 
                message2 = "Input must be an English word"
                messagebox.showinfo("Invalid Characters", message2)

        print (master_list)



def get_word(listy): 
    #shuffle the list
    list1 = []
    list1 = random.shuffle(listy)

    #take the last item, let that be the word
    word1 = listy[len(listy)-1]

    valid = True
    word = []
    x = 0

    #while the index of the string is valid add the character to the list
    while (valid):
        
        try:
            word.append(word1[x])
            x += 1
        except:
            valid = False

    #Create guessed list for stars
    guessed = []
    
    #Make a list of stars based on how many letters are in the word
    for everyLetter in range(len(word)):
        guessed.append("*")

    print(guessed, word)
    return guessed, word


def check4validSubmission ():

    global alreadyguessed
    #check current submission 
    global submission
    #assume all submission is invalid until proven otherwise
    #strip and lower the submission, make a list of the alphabet 
    valid = False
    submission = submission.lower().strip()
    possibilities = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
    possibilities += ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    #If the entry is a letter of alphabet, the submission is valid
    for x in possibilities :
        if (x == submission):
            valid = True

    #If the submission is not a letter, send out messagebox 
    if (valid == False) : 
        message = "Computer has spotted invalid input, you may only submit a single letter"
        messagebox.showinfo("Invalid input", message + "\nPlease Try Again")

    #If they've already guessed the letter it's not valid 
    if (valid):

        #No previous entries means a reoccurring value is impossible 
        if (len(alreadyguessed) == 0):
            alreadyguessed.append(submission)

        #if there are revious entries check for reoccurring 
        elif (len(alreadyguessed) > 0):
            for y in alreadyguessed: 
                if (submission == y):
                    message = "You have already guessed this letter!"
                    messagebox.showinfo("Invalid input", message + "\nPlease Try Again")
                    valid = False
                    break

    if valid:
        alreadyguessed.append(submission)
        
    return valid 
    print(valid)
    print(incorrectGuesses)

def checksubmission ( guessedLabel, incorrectLabel, scoreLabel, missingwordlabel): 
    #global variables  
    global word 
    global guessed
    global incorrectGuesses
    global incorrectGuessValue
    global score
    global submission
    
    #list to store correct guess indexes
    sameIndex = []
    submission = submission.lower().strip()
    
    #check to see if the letter is in the word 
    #if so add its index to a list 
    for x in range(len(word)):
        if (submission == word[x]):
            sameIndex.append(x)
            

    # If they guessed a number reveal it and add to score
    # The score multiplies based on how many reoccurring letters  
    if (len(sameIndex) > 0):
        for i in sameIndex:
            guessed.insert(i, submission)
            guessed.pop(i+1)
            score += 1 * (len(sameIndex))    
        
        #flash score because correct guess
        scoreLabel.config( fg = "green")

        scoreLabel.config( fg = "black")
    
    
    # If the guess didn't match anything, they guessed wrong
    if (len(sameIndex) == 0):
        incorrectGuesses += 1 
        incorrectGuessValue.append(submission)


    #update all labels 
    guessedLabel.config(text = "Guessed letters: " + str(incorrectGuessValue))
    scoreLabel.config(text = "Score: " + str(score))
    incorrectLabel.config(text = "Incorrect Guesses: " + str(incorrectGuesses))
    missingwordlabel.config(text = guessed)

    print(incorrectGuesses)
    
#make hangman visible by colouring objects on canvas 
def hangman(canvas, head, body, arm1, arm2, leg1, leg2):
    global incorrectGuesses

    # Depending on the number of incorrect guesses,
    # show parts of the hangman 
    if (incorrectGuesses == 1):
        canvas.itemconfig(head, outline ="black")

    if (incorrectGuesses == 2):
        canvas.itemconfig(body, fill ="black")

    if (incorrectGuesses == 3):
        canvas.itemconfig(arm1, fill ="black")

    if (incorrectGuesses == 4):
        canvas.itemconfig(arm2, fill ="black")

    if (incorrectGuesses == 5):
        canvas.itemconfig(leg1, fill ="black")
        canvas.itemconfig(leg2, fill ="black")

def winlose(resultlabel, button, scorelabel): 
    
    global word 
    global guessed
    global incorrectGuesses
    global score
    winlose = False

    print(incorrectGuesses)
    #this function changes the function of the entry box if the game is over
    def done():
        messagebox.showinfo("Game over", "The game has ended")

    #if the user wins display this message, disable button
    def win():
        resultlabel.config( text = "You Win!", borderwidth = 2, relief = RAISED)
        resultlabel.config( fg = "green")
        button.config(command = done)

    #if the user loses display this message, disable button 
    def lose():
        resultlabel.config( text = "You Lose!", borderwidth = 2, relief = RAISED)
        resultlabel.config( fg = "red")
        button.config(command = done)
        score = 0 
        scorelabel.config(text = "Score: " + str(score))

    #if the word has been guessed, they win
    if (word == guessed):
        winlose = True
        win()

    #if they guess too many times, they lose 
    elif(incorrectGuesses == 5): 
        winlose = True
        lose()

    #otherise do nothing 
    else: 
        pass
     
    #return to notify game to stop upon win or lose being true 
    return (winlose)
   
#-----------------------------START OF PROGRAM ------------------------------

#get word 
guessed, word = get_word(master_list)

#Run class to prompt GUI 
app = mainpage()

app.mainloop()

