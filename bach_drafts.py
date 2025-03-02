from psychopy import visual, event, core, sound, gui
import random
import os

#open a window
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#positions
positions = {"center": (0,0)}

#create image
image_path = os.path.join(os.getcwd(),"trials","1_.jpg")
image = visual.ImageStim(win,image=image_path,size=[500,500],pos=positions["center"])

#initialize mouse
mouse = event.Mouse() 
#discard old mouse events
event.clearEvents('mouse')

#task instructions
instruction_text = "Welcome to the Tuning Curve! Press the space bar to continue."
instruction = visual.TextStim(win, text = instruction_text,color="white", height=30, pos = (0,0))
instruction.draw()
win.flip()
#wait for the space key
event.waitKeys(keyList=['space'])
win.flip()
core.wait(.5)
# intruction 2
instruction_text = "Scroll the indicator to match the peak. Press 'n' to identify more peaks or press 'enter' to move onto the next image."
instruction = visual.TextStim(win, text = instruction_text,color="white", height=30, pos = (0,0))
instruction.draw()
win.flip()
# wait for the space key
event.waitKeys(keyList=['space'])
win.flip()
core.wait(.5)

while True: 
    #wheel movement
    wheel_movement = mouse.getWheelRel() [1]  
    # draw current image
    image.draw()
    #show 
    win.flip()
    #mouse click
    if wheel_movement != 0:
        print (wheel_movement)
        win.flip()
        core.wait(2)
        core.quit()
    
#quit
if event.getKeys(['q']):
    core.quit()
