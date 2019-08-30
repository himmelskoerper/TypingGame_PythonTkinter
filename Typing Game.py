import tkinter as tk
import tkinter.messagebox
import time


initial_time = 45
timeleft = initial_time
score = 0
attempt = 0
init_time = 0
username = ""
hs_counter = False


#open file and create file object to access and read data
words1file = open("words1.txt", "r")
#get the current high scores from file object
words = words1file.read()
#convert scores into a list of separate high score strings - split on space
split_words = words.split()
#close file object
words1file.close()    


#display current top scores
#open file and create file object to access and read data
highscoresfile = open("high_scores.txt", "r")
#get the current high scores from file object
high_scores = highscoresfile.read()
#convert scores into a list of separate high score strings - split on space
high_scores = high_scores.split()
#close file object
highscoresfile.close()  


#declear number of highscores   
n_o_hs = (int(len(high_scores)/2))
#declear the lowest highscore
lowest_hs = int(high_scores[(((n_o_hs)*2)-1)])


def b1_startgame():
    main_frame.pack_forget()
    game_container.pack()
    game_container.pack_propagate(0)

def b2_help():
    main_frame.pack_forget()
    help_frame.pack()
    help_frame.pack_propagate(0)
    
def b3_hs():
    main_frame.pack_forget()
    hs_frame.pack()
    
def b4_exit():
    root.destroy()
    
def display_menu():
    help_frame.pack_forget()
    hs_frame.pack_forget()
    game_container.pack_forget()
    main_frame.pack()


def startGame(event):
    global init_time
    global words
    #if there's still time left...
    if timeleft == initial_time:
        #start the countdown timer.
        countdown()
        e.config(state=tk.NORMAL)
        init_time = (time.time())
        
        text_label.config(state=tk.NORMAL)
        
        text_label.delete(1.0,2.0)
        text_label.insert(tk.END,words)
        text_label.config(state=tk.DISABLED,fg="black")
        
    
    #run the function to choose the next colour.
    nextWord()

def countdown():

    global timeleft

    #if a game is in play...
    if timeleft > 0:

        #decrement the timer.
        timeleft -= 1
        #update the time left label.
        time_label.config(text="Time left: \n" + str(timeleft))
        #run the function again after 1 second.
        time_label.after(1000, countdown)
        
        if timeleft == 3:
            time_label.config(fg="Red",font=("arial",31,"bold"))
        if timeleft == 0:
            e.config(state=tk.DISABLED)
            timeup()
   
def timeup():
    global hs_counter
    tk.messagebox.showinfo("Times up!" , "Your time is up " + "\nYour score is : " +
                          str(score) + "\nYour WPM is: " + str(WPM) + "\nYour accuracy is: " +
                          str(accuracy))
    
    if int(score) > int(lowest_hs):
        answer = tk.messagebox.askquestion("Congratulations",'''Congratulations. You have made to the highscore! \n 
        Do you want to have you score recorded?''')
        if answer == "yes":
            hs_counter = True
            get_user_name()


def get_user_name():
    
    root.unbind('<space>')
    root.bind('<space>', no_space_allowed)
    
    time_label.place_forget()
    currentword_label.place_forget()
    nextword_label.place_forget()  
    
    get_user_name_text = "PLEASE ENTER YOUR NAME BELOW"
    text_label.config(state=tk.NORMAL)
    text_label.delete(1.0,tk.END)
    text_label.insert(tk.END,get_user_name_text)
    text_label.config(state=tk.DISABLED,fg="black")
    
    e.config(state=tk.NORMAL)
    e.delete(0,tk.END)

def no_space_allowed(event):
    if hs_counter == True:
        tk.messagebox.showinfo("Sorry","No spaces are allowed in names")
        e.delete(0, tk.END)

#def highscore_record():
    


#So this is when user press space and skips to the next word or marks the word they have currently tpyed
#the if statement stops triggering nextWord() when the game hasn't started.
def space_skipword(event):
    if e.get() != "" :
        nextWord()


def nextWord():

    #use the globally declared 'score' and 'play' variables above.
    global score
    global timeleft
    global attempt
    global WPM
    global accuracy
    global username
    #if a game is currently in play...(if the split_words are not enough, game stops)
    if timeleft > 0 and int(attempt) < len(split_words):

        #...make the text entry box active.
        e.focus_set()
        
        
        each_word = split_words[int(attempt)]
        currentword_label.config(text= str(each_word))
        nextword_label.config(text= str(split_words[int(attempt)+1]))
        
        user_return = e.get()
        word_should_mark = split_words[(int(attempt)-1)]
        #At this moment this is actually marking the previous word
        #As the Attempt +1 at the last time Enter was hit, so the ones showing 
        #are actually for the next entrance as the bar would be cleared for this
        if user_return.lower() == word_should_mark .lower():
            #...add one to the score.
            score += 1
            
        elif user_return[0:len(word_should_mark)] == word_should_mark.lower():
            score += 1
                               
        attempt += 1

        e.delete(0, tk.END)

        score_label.config(text="Score: " + str(score))
        
        try:
            accuracy = int((score)/((attempt)-1)*100)
            accuracy_label.config(text="Accuracy: "+str(accuracy)+ "%")
        except ZeroDivisionError:
            accuracy_label.config(text="Accuracy: 100%")
            
        #get time difference
        time_diff = int((float(time.time())) - (float(init_time)))
        
        
        try:
            WPM = int(60/time_diff*(score))
            #config the WPM label while calculating the WPM
            # 60/time * score
            WPM_label.config(text="WPM: " + str(WPM) )
        except ZeroDivisionError:
            WPM_label.config(text="WPM: 0")

    if timeleft == 0 and hs_counter == True and e.get() != "" :
        username = e.get()
        make_new_hs()
        
def make_new_hs() :
    global score
    global lowest_hs
    global username
    global high_scores
    global hs_counter
    game_container.pack_forget()
    hs_frame.update()
    hs_frame.pack()
    b1_startgame.config(state=tk.DISABLED)
    
    if int(score) > int(lowest_hs) and hs_counter == True :
    
        score= int(score)
        
        #initialising position of at the last highscore
        pos = len(high_scores)-1
        
        #find the position of the highscore :D lucas is smart
        while score > int(high_scores[pos]) and pos > 1 :
            pos = pos-2
        
        if pos == 1:
            if score > int(high_scores[1]):
                high_scores.insert (0, str(score))
                high_scores.insert (0, str(username))
    
            else:
                high_scores.insert (pos + 1, str(score))
                high_scores.insert (pos + 1 , str(username))
        else :
            high_scores.insert (pos + 1, str(score))
            high_scores.insert (pos + 1, str(username))
        high_scores.remove(high_scores[-1])
        high_scores.remove(high_scores[-1])   

        
        highscoresfile = open("high_scores.txt", "w")
        high_scores = " ".join(high_scores)
        highscoresfile.write(high_scores)
        highscoresfile.close() 
        
        high_scores = high_scores.split()
        pack_hs()
        hs_frame.update()
        hs_counter = False

        #displaying high_scores
def pack_hs():
    global high_scores
    global hs_frame
    

    
    hs_title = tk.Label(hs_frame, text= "High score",font=("arial",32),width = 13)
    hs_title.place( x=435,y=130)
    
    hs_1_name = tk.Label(hs_frame, text = (high_scores[0]),font=("arial",25),width=7)
    hs_1_name.place(x=472,y=217)
    
    hs_1_score = tk.Label(hs_frame, text = (high_scores[1]),font=("arial",25),width=4)
    hs_1_score.place(x=675,y=217)
    
    hs_2_name = tk.Label(hs_frame, text = (high_scores[2]),font=("arial",25),width=7)
    hs_2_name.place(x=472,y=283)
    
    hs_2_score = tk.Label(hs_frame, text = (high_scores[3]),font=("arial",25),width=4)
    hs_2_score.place(x=675,y=283)
    
    hs_3_name = tk.Label(hs_frame, text = (high_scores[4]),font=("arial",25),width=7)
    hs_3_name.place(x=472,y=349)
    
    hs_3_score = tk.Label(hs_frame, text = (high_scores[5]),font=("arial",25),width=4)
    hs_3_score.place(x=675,y=349)
    
    hs_4_name = tk.Label(hs_frame, text = (high_scores[6]),font=("arial",25),width=7)
    hs_4_name.place(x=472,y=415)
    
    hs_4_score = tk.Label(hs_frame, text = (high_scores[7]),font=("arial",25),width=4)
    hs_4_score.place(x=675,y=415)
    
    hs_5_name = tk.Label(hs_frame, text = (high_scores[8]),font=("arial",25),width=7)
    hs_5_name.place(x=472,y=481)
    
    hs_5_score = tk.Label(hs_frame, text = (high_scores[9]),font=("arial",25),width=4)
    hs_5_score.place(x=675,y=481)


#create a GUI window.
root = tk.Tk()

#set the title.
root.title("Typing Game")
#set the size.
root.geometry("1200x800+100+75")

#=========Menu=================
main_frame = tk.Frame(root, width= 1200,height=800)
main_frame.pack()
main_frame.pack_propagate(0)

menu_bg = tk.Canvas(main_frame, width = 1175, height = 775, bg="Light Blue")
menu_bg.place( x=10 , y =10 )

#Frame to hold the buttons
main_menu_container = tk.Frame(main_frame, bg="Light Blue")
main_menu_container.place( x=450 , y =200 )

#Image for the buttons
b1_image = tk.PhotoImage (file="buttonbg.png")
b1_image_small = b1_image.subsample(10,10)

#ALL The buttons
b1_startgame = tk.Button(main_menu_container,text="Start Game",font=("arial",27),fg="white", command=b1_startgame)
b1_startgame.pack(pady=10)
b1_startgame.config(image=b1_image_small,compound=tk.CENTER,bg="light blue")

b2_help = tk.Button(main_menu_container,text="How To Play",font=("arial",27),fg="white",command=b2_help)
b2_help.pack(pady=10)
b2_help.config(image=b1_image_small,compound=tk.CENTER,bg="light blue")

#hs stands for highscore button
b3_hs = tk.Button(main_menu_container,text="High Scores",font=("arial",27),fg="white",command= b3_hs)
b3_hs.pack(pady=10)
b3_hs.config(image=b1_image_small,compound=tk.CENTER,bg="light blue")

b4_exit = tk.Button(main_menu_container,text="Exit",font=("arial",27),fg="white",command= b4_exit)
b4_exit.pack(pady=10)
b4_exit.config(image=b1_image_small,compound=tk.CENTER,bg="light blue")

menu_title = tk.Label(main_frame, text="Welcome To Typing Game V1", font=("arial",40,"bold"), fg="white",bg="Light blue")
menu_title.place(x=250,y=70)

#PHOTO USED LATER
help_bg = tk.PhotoImage (file="help_bg.PNG")

#==============HELP===SCREEN=====
help_frame = tk.Frame(root, width= 1200,height=800 )

help_bg_colour = tk.Canvas(help_frame, width = 1175, height = 775, bg="Light Blue")
help_bg_colour.place( x=10 , y =10 )

help_bg = help_bg.subsample(3,3)

help_box = tk.Label(help_frame, image= help_bg,bg="light blue")
help_box.place( x=310, y=70)

return_to_menu = tk.Button(help_frame,text="RETURN TO MENU",font=("arial",17),fg="white",command= display_menu)
return_to_menu.place(x=930,y=670)
return_to_menu.config(image=b1_image_small,compound=tk.CENTER)




#===============HIGHSCORE====SCREEN=====
hs_frame = tk.Frame(root, width= 1200,height=800 )

hs_bg_colour = tk.Canvas(hs_frame, width = 1175, height = 775, bg="Light Blue")
hs_bg_colour.place( x=10 , y =10 )

hs_bg = tk.PhotoImage (file="hs_bg.PNG")
hs_bg = hs_bg.subsample(5,4)

hs_box = tk.Label(hs_frame, image= hs_bg,bg="light blue")
hs_box.place( x=360, y=80)

return_to_menu = tk.Button(hs_frame,text="RETURN TO MENU",font=("arial",17),fg="white",command= display_menu)
return_to_menu.place(x=930,y=670)
return_to_menu.config(image=b1_image_small,compound=tk.CENTER)

pack_hs()

#============GAME=========FRAME==================

game_container = tk.Frame(root,width=1200, height=800)



game_bg = tk.Canvas(game_container, width = 1175, height = 775, bg="Light Blue")
game_bg.place( x=10 , y=10 )

label= tk.Label(game_container, text="stuipid",font=("arial",30),fg="white",bg="light blue")
label.place(x=100,y=100)



label_container = tk.Frame(game_container, width=1170, height = 770,bg="Light Blue")
label_container.place(x=13,y=13)


#bg image used for the labels
label_image_small = b1_image.subsample(12,12)



#ALL The labels+images
stopwatch = tk.PhotoImage(file="stopwatch.PNG")
stopwatch_small = stopwatch.subsample(3,3)

time_label = tk.Label(label_container,text="Time left: \n"  + str(timeleft),font=("arial",25),fg="Black")
time_label.place(x=15,y=15)
time_label.config(image=stopwatch_small,compound=tk.CENTER,bg="light blue")


score_label = tk.Label(label_container,text="Score: " + str(score) ,font=("arial",20),fg="white")
score_label.place(x=340, y=50)
score_label.config(image=label_image_small,compound=tk.CENTER,bg="light blue")


WPM_label = tk.Label(label_container,text="WPM: 0" ,font=("arial",20),fg="white")
WPM_label.place(x= 575, y= 50)
WPM_label.config(image=label_image_small,compound=tk.CENTER,bg="light blue")


accuracy_label = tk.Label(label_container,text="Accuracy:"+ "100% ",font=("arial",15),fg="white")
accuracy_label.place(x=800, y=50)
accuracy_label.config(image=label_image_small,compound=tk.CENTER,bg="light blue")

return_to_menu = tk.Button(label_container,text="RETURN TO MENU",font=("arial",17),fg="white",command= display_menu)
return_to_menu.place(x=930,y=670)
return_to_menu.config(image=b1_image_small,compound=tk.CENTER)


label_image_longer = b1_image.subsample(8,12)

currentword_label = tk.Label(label_container, text= "Current word", font=("arial",30),fg="white",bg="light blue")
currentword_label.place(x=150,y=495)
currentword_label.config(image=label_image_longer,compound=tk.CENTER,bg="light blue")

nextword_label = tk.Label(label_container, text= "Next word", font=("arial",30),fg="white",bg="light blue")
nextword_label.place(x=820,y=495)
nextword_label.config(image=label_image_longer,compound=tk.CENTER,bg="light blue")

entry_bg = tk.Label(label_container,bg="light blue")
entry_bg.place(x=535,y=520)
entry_bg.config(image=label_image_small)

text_label= tk.Text(label_container,height=10,width=60,wrap=tk.WORD)
text_label.place(x=240,y=175)
initial_words = "PRESS ENTER TO START GAME"
text_label.insert(tk.END,initial_words)
text_label.config(font=("times new roman",20),bd=0,fg="red")
text_label.pack_propagate(0)
text_label.config(state=tk.DISABLED)


1#add a text entry box for typing in colours.
e = tkinter.Entry(label_container,width=25,state=tk.DISABLED)

e.place(x = 560, y = 550)
#set focus on the entry box.
e.focus_set()



#run the 'startGame' function when the enter key is pressed.
root.bind('<Return>', startGame)

root.bind('<space>', space_skipword)

root.mainloop()

