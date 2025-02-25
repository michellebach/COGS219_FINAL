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
win = visual.Window([800,800],color="grey", units='pix', checkTiming=False) 

#positions
positions = {"center": (0,0)}

#create image
image_path = os.path.join(os.getcwd(),"image","1_.jpg")
image = visual.ImageStim(win,image=image_path,size=[400,400],pos=positions["center"])

print(image_path)

# draw image
image.draw()

#show
win.flip()
win.close()
f.close()