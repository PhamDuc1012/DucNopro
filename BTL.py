#Thư viện giao tiếp với Arduino
import serial

#Thư viện lấy thời gian và thời gian delay
from time import sleep
import datetime

#Thư viện dùng cho thao tác với file csv và database
import csv
import pyrebase

#Thư viện dùng cho việc gửi mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Thư viện dùng cho vẽ biểu đồ
import matplotlib.pyplot as plt
from drawnow import drawnow

#Thư viện làm giao diện 
from tkinter import *
import tkinter.ttk as ttk

# Tạo giao diện gốc
root = Tk()
logo = PhotoImage(file="/home/pi/Downloads/background.png")
root.title("HOME")
pos_bgd = Label(root,image=logo).pack(side=TOP)
root.geometry('850x450')


# Hàm xem lại lịch sử dữ liệu từ file csv đã lưu
def history():
	# Tạo cửa sổ mới
    history_win = Toplevel(root)
    history_win.title("History")
    history_win.geometry('400x400')
    TableMargin = Frame(history_win)
    TableMargin.pack(side=TOP,fill=X)

    #Tạo thanh cuộn dọc và Treeview để hiển thị dữ liệu
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("DATE","TIME","TEMP"), height=400,yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)

    # cài đặt heading và các cột hiển thị dữ liệu
    
    tree.heading('DATE', text="DATE", anchor=CENTER)
    tree.heading('TIME', text="TIME", anchor=CENTER)
    tree.heading('TEMP', text="TEMP", anchor=CENTER)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('DATE', stretch=NO, minwidth=0, width=120,anchor=CENTER)
    tree.column('TIME', stretch=NO, minwidth=0, width=120,anchor=CENTER)
    tree.column('TEMP', stretch=NO, minwidth=0, width=90,anchor=CENTER)
    tree.pack()

    # lấy dữ liệu từ file csv
    with open('temp1.csv','r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            tree.insert("", "end", values=row)

# Hàm cài đặt biểu đồ
def makeFig():
	plt.title('Temperature') # Tên biểu đồ
	plt.xlabel(datetime.datetime.now().strftime("%Y-%m-%d")) # Nhãn trục x
	plt.ylabel('Temp') # Nhãn trục y
	plt.plot(date_time,temp_data,'ro-', label='Degrees C') #Vẽ biểu đồ 
	plt.legend(loc='upper left') # Vị trí chú thích
	plt.xticks(rotation=45, ha='right') # Cài đặt các phần tử trục x quay 45 độ về bên phải
	plt.subplots_adjust(bottom=0.30) # Căn lề dưới của biểu đồ

# Hàm vẽ biểu đồ
def plott(cnt):
	drawnow(makeFig) #drawnow: cập nhật biểu đồ theo thời gian thực
	sleep(0.2)
	#Giới hạn biểu đồ trong 10 điểm
	if cnt > 10:
		temp_data.pop(0)
		date_time.pop(0)

# Hàm gửi mail
def mail(nhiet_do, thoi_gian ):
	mail_content = f"The time is {thoi_gian}, the temperature is {nhiet_do}"

	#The mail addresses and password
	sender_address = 'abc.clone.duy@gmail.com'
	sender_pass = 'duy2632001'	
	receiver_address = 'abc.clone.duy@gmail.com'

	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Warning temperature '   #The subject line
	
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail Sent successful')

# Thoát chương trình
def quit():
	global stop
	stop = True
	sys.exit()

# Tạm dừng chương trình
def pause():
	global stop_plot
	stop_plot=True

temp_data = [] # lưu dữ liệu nhiệt độ
date_time = [] # lưu thời gian giờ phút giây
plt.ion() # chế độ vẽ thời gian thực
cnt=0  #biến cnt để giới hạn biểu đồ
def main():

	config ={
	"apiKey": "AIzaSyAZjJaDyVx7I4zw-8z4ktmkk2Tmid8B8Pw",
  	"authDomain": "pyrebaserealtimedatabase-bd3ac.firebaseapp.com",
  	"databaseURL": "https://pyrebaserealtimedatabase-bd3ac-default-rtdb.asia-southeast1.firebasedatabase.app",
  	"storageBucket": "pyrebaserealtimedatabase-bd3ac.appspot.com"}
	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

	# Khai báo biến toàn cục
	global temp_data,date_time, stop,stop_plot,cnt
	stop = False
	stop_plot = False
	
	with serial.Serial("/dev/ttyUSB0",9600, timeout=1) as arduino:
		sleep(0.1)
		if arduino.isOpen():
			print("{} connected!".format(arduino.port))
			with open("temp1.csv","a") as file:
				while True:
					if stop == False and stop_plot == False:
						now = datetime.datetime.now()
						x = str(arduino.readline())
						x = x.strip("',b,\,n,r")
						if len(x) > 0:
							# Đẩy dữ liệu lên firebase
							data = {"Datetime": now.strftime("%Y-%m-%d"), "Time": now.strftime("%H:%M:%S"), "Temp": x}
							db.child("Last value").update(data)
							db.child("Push").push(data)

							#Lưu dữ liệu vào file csv
							writer = csv.writer(file)
							writer.writerow([now.strftime("%Y-%m-%d"),now.strftime("%H:%M:%S"),x])
							
							# Cập nhât dữ liệu nhiệt độ và thời gian vào list lưu nhiệt độ và list đo thời gian
							temp_data.append(float(x))
							date_time.append(now.strftime("%H:%M:%S"))
							
							# Sau mỗi vòng lặp tăng biến cnt lên 1
							cnt = cnt+1
							
							# Vẽ biểu đồ
							plott(cnt)
							
							# Gửi mail cảnh báo, bật đèn và còi báo động khi nhiệt độ cao
							if float(x)>40:
								#Gửi mail cảnh báo
								#mail(float(x),now.strftime("%H:%M:%S"))

								# Truyền tín hiệu cho arduino
								arduino.write(str.encode('1'))
					elif stop == False and stop_plot == True:
						break
					else:
						sys.exit()


# Cài đặt các nút trên giao diện              
temp_button = Button(root,text="REAL TIME TEMPERATURE GRAPH",height=4,command=main)
temp_button.pack(side=LEFT)
stop_button = Button(root,text="QUIT PROGRAM",height=4,command=quit)
stop_button.pack(side=RIGHT)
pause_button = Button(root,text="PAUSE",height=4,command=main)
pause_button.pack(side=LEFT)
history_button = Button(root,text="HISTORY",height=4,command=history)
history_button.pack(side=RIGHT)
root.mainloop()

