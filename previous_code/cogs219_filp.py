from psychopy import visual,event,core,gui
import os

# create a trials folder if it doesn't already exist
try:
    os.mkdir('/Users/michelleding/Desktop/trials')
except FileExistsError:
    print('Trials directory exists; proceeding to open file')
    
f= open(f"/Users/michelleding/Desktop/trials/RP01_trials.csv","w")

#write header
separator = ","
header = separator.join(["neuron_index","total_peak","p1","p2","p3","p4","p5"])
f.write(header+'\n')

#setup path to all images
path = "/Users/michelleding/Desktop/image"

#open a window
win = visual.Window([900,700],color="gray", units ='pix',checkTiming=False)
#create placeholder and message
placeholder = visual.Rect(win,width=700,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,-300])
instruction = visual.TextStim(win,text="Please use the mouse wheel to adjust the angle and make your selection", height=20, color="black",pos=[0,-300])
#create next button
placeholder2 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[300,-300])
nextButton = visual.TextStim(win,text="-->", height=20, color="black",pos=[300,-300])

#add a mouse
mouse = event.Mouse(win=win)

#positions
positions = {"center": (0,0)}

#total number of neurons
neuron_id = 1
total_neuron = 1

#create image
#image_path = os.path.join(os.getcwd(),"image","1_.jpg")
#image = visual.ImageStim(win,image=image_path,size=[700,500],pos=positions["center"])

#loop through all neuron plots (1 to total_neuron)
while not event.getKeys(['q']):
    #create image
    image_path = os.path.join(os.getcwd(),"image",str(neuron_id)+"_.jpg")
    image = visual.ImageStim(win,image=image_path,size=[700,500],pos=positions["center"])

    # draw image
    image.draw()
    placeholder.draw()
    instruction.draw()
    placeholder2.draw()
    nextButton.draw()

    #show
    win.flip()
    
    #flip control (make sure one flip per click)
    if mouse.isPressedIn(placeholder2,buttons=[0]):
        neuron_id += 1
        win.flip()
        core.wait(0.5)
win.close()
f.close()
core.quit()