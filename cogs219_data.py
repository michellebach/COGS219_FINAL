from psychopy import visual,event,core,gui
import os

def draw_clock (wheel_movement): 
    """ 
    function takes current wheel movement (float) to show on-time angle
    returns current angle degree (str)
    """
    clockhand.ori += int(wheel_movement*5)
    clockhand.draw()
    #invert sign, negative for clockwise and positive for counter-clockwise
    angle = clockhand.ori * -1
    #compute angle and update on win
    #nearest integer with degree sign
    angle_text = str(int(angle % 360))
    #angle_show = visual.TextStim(win,text= angle_text+'\N{DEGREE SIGN}', height=50, color="black",pos=[290,180])
    #angle_show.draw()
    return angle_text
        
        
# create a trials folder if it doesn't already exist
try:
    os.mkdir('/Users/michelleding/Desktop/trials')
except FileExistsError:
    print('Trials directory exists; proceeding to open file')
    
f= open(f"/Users/michelleding/Desktop/trials/RP01_trials.csv","w")

#write header
separator = ","
header = separator.join(["participant_id","neuron_index","p1","p2","p3","p4","p5"])
f.write(header+'\n')

#setup path to all images
path = "/Users/michelleding/Desktop/image"

#open a window
win = visual.Window([900,720],color="gray", units ='pix',checkTiming=False)
#task instructions
welcome_text = "Welcome to the Tuning Curve!\nPress the space bar to continue:)))"
welcome = visual.TextStim(win, text = welcome_text,color="white", height=30, pos = (0,0))
#create placeholder and message
placeholder = visual.Rect(win,width=700,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[-10,-310])
instruction = visual.TextStim(win,text="Please use the mouse wheel to adjust the angle and make your selection", height=20, color="black",pos=[-10,-310])
#create next button
placeholder2 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[290,-310])
nextButton = visual.TextStim(win,text="-->", height=20, color="black",pos=[290,-310])
# Draw clock_hand
#coordinate = ((12, 8), (104, 13), (220, 8),(104,3))
coordinate = ((200, 0), (0, 10), (0,-10))
clockhand = visual.ShapeStim(win, units='', colorSpace='rgb', fillColor='#EC9706', lineColor='#EC9706', lineWidth=1.5, vertices=coordinate)
# center circle of clock hand
cen_circle = visual.Circle(win=win, radius=10, lineColor='black', fillColor='black', pos=[0, 0])
#cen_triangle = visual.Polygon(win=win, edges=3, size=[10, 240], lineColor='black', pos=[75, 10], fillColor='black', ori=90) 
#on-time angle 
angle_show = visual.TextStim(win,text="0"+"\N{DEGREE SIGN}", height=50, color="black",pos=[290,180])
#create selection
placeholder3 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[290,50])
selection = visual.TextStim(win,text="select", height=20, color="black",pos=[290,50])
#create five peak boxes
position = {1:[-290,150], 2:[-290,70],3:[-290,-10],4:[-290,-90],5:[-290,-170]}
placeholder4 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=position.get(1))
placeholder5 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=position.get(2))
placeholder6 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=position.get(3))
placeholder7 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=position.get(4))
placeholder8 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=position.get(5))
peak1 = visual.TextStim(win,text="peak 1", height=20, color="black",pos=position.get(1))
peak2 = visual.TextStim(win,text="peak 2", height=20, color="black",pos=position.get(2))
peak3 = visual.TextStim(win,text="peak 3", height=20, color="black",pos=position.get(3))
peak4 = visual.TextStim(win,text="peak 4", height=20, color="black",pos=position.get(4))
peak5 = visual.TextStim(win,text="peak 5", height=20, color="black",pos=position.get(5))
#create cancel 
placeholder9 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[290,-50])
cancel = visual.TextStim(win,text="cancel", height=20, color="black",pos=[290,-50])

#initialize mouse
#add a mouse
mouse = event.Mouse(win=win)
#discard old mouse events
event.clearEvents('mouse')

#total number of neurons
neuron_id = 1
total_neuron = 295

#dict of possible peaks
peak = {1:peak1, 2:peak2,3:peak3,4:peak4,5:peak5}

#total number of selected peaks
peak_num = 0

#create image
#image_path = os.path.join(os.getcwd(),"image","1_.jpg")
#image = visual.ImageStim(win,image=image_path,size=[700,500],pos=positions["center"])

#welcome page load
welcome.draw()
win.flip()
#wait for the space key
event.waitKeys(keyList=['space'])
win.flip()
core.wait(.5)

#loop through all neuron plots (1 to total_neuron)
while not event.getKeys(['q']):
    #create image
    image_path = os.path.join(os.getcwd(),"image",str(neuron_id)+"_.jpg")
    image = visual.ImageStim(win,image=image_path,size=[700,500],pos= [-10, -10])

    # draw image, nextButton, clockhand, ontime angle, selection
    image.draw()
    placeholder.draw()
    instruction.draw()
    placeholder2.draw()
    nextButton.draw()
    clockhand.draw()
    cen_circle.draw()
    #cen_triangle.draw()
    angle_show.draw()
    placeholder3.draw()
    selection.draw()
    placeholder4.draw()
    placeholder5.draw()
    placeholder6.draw()
    placeholder7.draw()
    placeholder8.draw()
    peak1.draw()
    peak2.draw()
    peak3.draw()
    peak4.draw()
    peak5.draw()
    placeholder9.draw()
    cancel.draw()
    
    #wheel movement
    wheel_movement = mouse.getWheelRel() [1]
    
    #rotate clockhand and show on-time angle
    angle_text = draw_clock (wheel_movement)
    angle_show.text = angle_text+'\N{DEGREE SIGN}'
    angle_show.draw()
    cen_circle.draw()
    
    #show
    win.flip()
    
    #click selection button
    if mouse.isPressedIn(placeholder3,buttons=[0]) and peak_num <= 5:
        peak_num += 1
        core.wait(0.3)
        # if selected peaks > 5
        # disable select
        if peak_num > 5:
            selection.text = 'MAX'
            selection.color = 'darkred'
            selection.draw()
        #show selected angle and its corresponding box
        else:
            selected_peak = peak.get(peak_num)
            selected_peak.text = angle_text
            selected_peak.draw()
            
    #click cancel button
    elif mouse.isPressedIn(placeholder9,buttons=[0]) and peak_num > 0 and peak_num <= 6:
        core.wait(0.3)
        #if selected peaks > 5 but cancelled
        #enable 'select'
        if peak_num > 5: 
            selection.text = 'select'
            selection.color = 'black'
            selection.draw()
            peak_num = 5
        #cancel last selected peak
        cancel_peak = peak.get(peak_num)
        cancel_peak.text = 'peak '+ str(peak_num)
        cancel_peak.draw()
        peak_num -= 1
    #flip control (make sure one flip per click)
    elif mouse.isPressedIn(placeholder2,buttons=[0]):
        neuron_id += 1
        win.flip()
        core.wait(0.5)
        #write selected peaks to csv
        data = separator.join(["participant_id","neuron_index",peak1.text,peak2.text,peak3.text,peak4.text,peak5.text])
        f.write(data+'\n')
        #reset to original
        selection.color = 'black'
        selection.text = 'select'
        peak1.text = 'peak 1'
        peak2.text = 'peak 2'
        peak3.text = 'peak 3'
        peak4.text = 'peak 4'
        peak5.text = 'peak 5'
        peak_num = 0
win.close()
f.close()
core.quit()