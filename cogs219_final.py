from psychopy import visual,event,core,gui
import os, random
# from helper import get_runtime_vars, generate_trials

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

#function for runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="Tuning"):
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

# generate trials
def generate_trials(subj_id, seed, num_repetitions=1):
    import os
    import random
    
    separator = ","
    num_repetitions = int(num_repetitions)
    
    #set seed
    random.seed(int(seed))
    
    # create a trials folder if it doesn't already exist
    try:
        os.mkdir('trials')
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')
    f= open(f"trials/{subj_id}_trials.csv","w")
    
    #write header
    header = separator.join(["subj_id", "seed", "number_of_trials", "neuron_index","total_peak","p1","p2","p3","p4","p5"])
    f.write(header+'\n')
    
    # write code to loop through creating trials here
    trial_data = []
    for i in range(num_repetitions):
        trial_data.append(["subj_id", "seed", "number_of_trials", "neuron_index","total_peak","p1","p2","p3","p4","p5"])
    
    #shuffle the list
    random.shuffle(trial_data)
    
    #write the trials to the trials file
    for cur_trial in trial_data:
        f.write(separator.join(map(str,cur_trial))+'\n')
    
    #close the file
    f.close()

# import_trials function from previous assignments
def import_trials (trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names)
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

#open a window ######
win = visual.Window([900,720],color="gray", units ='pix',checkTiming=False)

#get runtime variables
order =  ['participant_id','seed','number_of_trials']
runtime_vars= get_runtime_vars({'participant_id':'RP01', 'seed':10, 'number_of_trials':[50, 150, 250]}, order)
print(runtime_vars)

# generate trials
generate_trials(runtime_vars['participant_id'],runtime_vars['seed'],runtime_vars['number_of_trials'])

# load function from helper
def load_files(directory,extension,fileType,win='',restriction='*', stim_list=[]):
    """ Load all the pics and sounds. Uses pyo or pygame for the sound library (see prefs.general['audioLib'])"""
    path = os.getcwd() #set path to current directory
    if isinstance(extension,list):
        file_list = []
        for curExtension in extension:
            file_list.extend(glob.glob(os.path.join(path,directory,restriction+curExtension)))
    else:
        file_list = glob.glob(os.path.join(path,directory,restriction+extension))
    files_data = {} #initialize files_data  as a dict because it'll be accessed by file names (picture names, sound names)
    for num,curFile in enumerate(file_list):
        fullPath = curFile
        fullFileName = os.path.basename(fullPath)
        stimFile = os.path.splitext(fullFileName)[0]
        if fileType=="image":
            try:
                surface = pygame.image.load(fullPath) #gets height/width of the image
                stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
                (width,height) = (surface.get_width(),surface.get_height())
            except: #if no pygame, image dimensions may not be available
                pass
            stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
            (width,height) = (stim.size[0],stim.size[1])
            files_data[stimFile] = {'stim':stim,'fullPath':fullFileName,'filename':stimFile,'num':num,'width':width, 'height':height}
        elif fileType=="sound":
            files_data[stimFile] = {'stim':sound.Sound(fullPath), 'duration':sound.Sound(fullPath).getDuration()}
 
    #optionally check that the stimuli we *need* to load are actually available in the directory; return error if there is a discrepancy
    if stim_list and set(files_data.keys()).intersection(stim_list) != set(stim_list):
        popupError(str(set(stim_list).difference(list(files_data.keys()))) + " does not exist in " + path+'\\'+directory) 
    return files_data

#read in trials
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['participant_id']+'_trials.csv')
trial_list = import_trials(trial_path)

#open trials file and write header
try:
    os.mkdir('trials')
    print('Data directory did not exist. Created trials/')
except FileExistsError:
    pass 
separator=","
trials_file = open(os.path.join(os.getcwd(),'trials',runtime_vars['participant_id']+'_trials.csv'),'w')
header = separator.join(["participant_id", "seed", "number_of_trials", "neuron_index","total_peak","p1","p2","p3","p4","p5"])
trials_file.write(header+'\n')

#task instructions
welcome_text = "Welcome to the Tuning Curve Task!\nPress the space bar to continue:)))"
welcome = visual.TextStim(win, text = welcome_text,color="white", height=30, pos = (0,0))
#create placeholder and message
placeholder = visual.Rect(win,width=700,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[-10,-310])
instruction = visual.TextStim(win,text="Please use the mouse wheel to adjust the angle and make your selection", height=20, color="black",pos=[-10,-310])
#create next button
placeholder2 = visual.Rect(win,width=70,height=40, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[290,-310])
#nextButton = visual.TextStim(win,text="-->", height=20, color="black",pos=[290,-310])
arrow_sqr = visual.ShapeStim(win=win, size=[50, 25], vertices='rectangle', lineColor='black', pos=[265, -310], fillColor='black', ori=0)
arrow_head = visual.Polygon(win=win, edges=3, size=[50, 50], lineColor='black', pos=[290, -310], fillColor='black', ori=90)

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
total_neuron = runtime_vars['number_of_trials']

#dict of possible peaks
peak = {1:peak1, 2:peak2,3:peak3,4:peak4,5:peak5}

#total number of selected peaks
peak_num = 0

#welcome page load
welcome.draw()
win.flip()
#wait for the space key
event.waitKeys(keyList=['space'])
win.flip()
core.wait(.5)

#loop through all neuron plots 
while not event.getKeys(['q']):
    #create image
    image_path = os.path.join(os.getcwd(),"image",str(neuron_id)+ "_.jpg")
    #image = visual.ImageStim(win,image=image_path,size=[700,500],pos= [-10, -10])
    #image randomization
    rand_image = random.choice(image_path)
    image = visual.ImageStim(win, image=rand_image, size=[700,500],pos= [-10, -10])

    # draw image, nextButton, clockhand, ontime angle, selection
    image.draw()
    placeholder.draw()
    instruction.draw()
    placeholder2.draw()
    #nextButton.draw()
    arrow_sqr.draw()
    arrow_head.draw()
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
        data = separator.join([str(runtime_vars["participant_id"]), str(runtime_vars["seed"]), str(runtime_vars["number_of_trials"]), "neuron_id" ,peak1.text,peak2.text,peak3.text,peak4.text,peak5.text])
        trials_file.write(data+'\n')
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
trials_file.close()
core.quit()