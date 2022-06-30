from tkinter import *
from time import sleep
import serial
import sys
from tkinter import filedialog

port_opened=False

def set_port():
    global port_opened,arduino
    com_port= port_input.get()
    arduino=serial.Serial(com_port,9600,timeout=1)
    port_opened=True
    print ("Connected to "+com_port)

def send_arduino(servo_angle):
	global arduino
	angles = "{0:0=3d}".format(servo_angle[0])+"{0:0=3d}".format(servo_angle[1])+"{0:0=3d}".format(servo_angle[2])+"{0:0=3d}".format(servo_angle[3])+"\n"
	arduino.write(str.encode(angles))
	print(angles,end='')
	sleep(1)

save_servo_angle=[]
def save_angles():
	save_servo_angle.append([base_slider.get(), shoulder_slider.get(), elbow_slider.get(), gripper_slider.get()])
	print("Saved:"+str(save_servo_angle))

playback=False
def servo_action():
	global playback,stop
	playback=True
	stop=False
	for servo_angle in save_servo_angle:
		print("Playing:"+str(servo_angle))
		send_arduino(servo_angle)
		sleep(1)


def delete_angles():
	global save_servo_angle
	save_servo_angle=[]
	print("Deleted!")

stop=False
def stop_action():
	global stop,playback
	stop=True
	playback=False

close_program = False	
def quit_program():
	global close_program
	close_program=True
	sys.exit()

def open_file():
    global save_servo_angle
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files","*.txt*"),("all files","*.*")))
    file = open(filename, "r")
    data=file.read()
    save_servo_angle=eval(data)
    file.close()
    print("opened: "+filename)

def save_file():
    save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    save_file.write(str(save_servo_angle))
    save_file.close()
    print("saved file")

window= Tk()
window.title("CONTROL PANEL")
window.minsize(400,500)


port_label=Label(window,text="Set Port:",fg="Red");
port_label.place(x=10,y=10);
port_input=Entry(window)
port_input.place(x=10,y=35)
port_button=Button(window, text="Enter", command=set_port,fg="Red")
port_button.place(x=135,y=32)

base_slider = Scale(window, from_=0, to=180,orient=HORIZONTAL,length=300,fg="Green")
base_slider.place(x=80, y=80)
base_label=Label(window,text="     BASE      ",fg="Green",background="Yellow")
base_label.place(x=10, y=86)

shoulder_slider = Scale(window, from_=0, to=180,orient=HORIZONTAL,length=300,fg="Green")
shoulder_slider.place(x=80, y=140)
shoulder_label=Label(window,text="SHOULDER",fg="Green",background="Yellow")
shoulder_label.place(x=10, y=146)

elbow_slider = Scale(window, from_=0, to=180,orient=HORIZONTAL,length=300,fg="Green")
elbow_slider.place(x=80, y=200)
elbow_label=Label(window,text="   ELBOW    ",fg="Green",background="Yellow")
elbow_label.place(x=10, y=206)

gripper_slider = Scale(window, from_=0, to=180,orient=HORIZONTAL,length=300,fg="Green")
gripper_slider.place(x=80, y=260)
gripper_label=Label(window,text="  GRIPPER   ",fg="Green",background="Yellow")
gripper_label.place(x=10, y=266)


save_button=Button(window, text="Save actions", command=save_angles,height=3)
save_button.place(x=60,y=320)

delete_button=Button(window, text="Delete actions", command=delete_angles,height=3)
delete_button.place(x=250,y=320)

play_button=Button(window, text="Start actions", command=servo_action, height=3)
play_button.place(x=60,y=390)

stop_button=Button(window,text="    Stop loop    ",command=stop_action,height=3)
stop_button.place(x=250,y=390)

close_button=Button(window,text="Close program",command=quit_program,height=2)
close_button.place(x=150,y=455)

taskbar = Menu(window)
filemenu = Menu(taskbar, tearoff=0)
filemenu.add_command(label="Open File", command=open_file)
filemenu.add_command(label="Save File", command=save_file)
taskbar.add_cascade(label="File", menu=filemenu)


window.config(background="Orange", menu=taskbar)
while True:
    window.update()
    if(port_opened and playback==False):
    	send_arduino([base_slider.get(), shoulder_slider.get(), elbow_slider.get(), gripper_slider.get()])

    if (playback):
    	servo_action()

    if (stop):
    	stop_action()

    if (close_program):
    	quit_program()
