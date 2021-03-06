"""Author : NITHISH R,UNNIKRISHNAN T A,VISHNURAJ S
/* Institute :Federal Institute of Science And Technology,Kerala 

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *"""
import cv,os
import pyaudio,wave,sys,csv


#cv.NamedWindow("Actual",cv.CV_WINDOW_AUTOSIZE)
#cv.NamedWindow("Window_SCR",cv.CV_WINDOW_AUTOSIZE)
#cv.NamedWindow("Mask",cv.CV_WINDOW_AUTOSIZE)

storage = cv.CreateMemStorage(0)



capture=cv.CreateCameraCapture(0)#the value within () can be 0 or 1 depending on whether the webcam is inbuilt or external
frame=cv.QueryFrame(capture)

imgHSV = cv.CreateImage((640,480), 8, 3)
imgMask = cv.CreateImage(cv.GetSize(frame), 8, 1)
b_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
scribble = cv.CreateImage(cv.GetSize(frame), 8, 3) # stores scribbles
dot=cv.CreateImage(cv.GetSize(frame), 8, 3)


#kernel = cv.CreateStructuringElementEx ( 5 , 5 , 2 , 2 , cv.CV_SHAPE_RECT )

contour = 0   ## dummy stmnt

x1,y1,x2,y2=0,0,0,0	

#lx,ly= 0, 0
yellow_miss=0
green_miss=0
xr,yr,xb,yb,xg,yg,xy,yy=0,0,0,0,0,0,0,0
yellow_flag=0  # set when there s yello detection 
lastxr,lastyr=0,0
lastxb,lastyb=0,0
flist=[]
def ShowFrame():

	global frame
	cv.Flip(frame,frame,1)
	cv.MoveWindow("Actual",60,60)
	cv.ShowImage("Actual",frame)	
	cv.WaitKey(10)


def CalcPos(min_color,max_color):

	global frame
	
	cv.Smooth(frame,b_frame, cv.CV_GAUSSIAN, 9, 9)
	cv.CvtColor(b_frame, imgHSV, cv.CV_BGR2HSV)
	cv.InRangeS(imgHSV,min_color,max_color,imgMask)
	cv.Erode(imgMask,imgMask, None ,4)
	cv.Dilate(imgMask,imgMask, None ,4)
	contour = cv.FindContours(imgMask, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []
	c1_x,c1_y,c2_x,c2_y=0,0,0,0
	count_pix=0
	x,y=1,1
	
	#cv.Add(imgMask,frame,frame)
        while contour:
        	bound_rect = cv.BoundingRect(list(contour))
		if contour:
			area= abs(cv.ContourArea(contour))
			#print area
			if area : #in range(10,3000):
				 
				c1_x+=bound_rect[0]
				c1_y+=bound_rect[1]
				c2_x+=bound_rect[2]+bound_rect[0]
				c2_y+=bound_rect[3]+bound_rect[1]
				count_pix+=1
				
                
		contour = contour.h_next()

                
	
	if count_pix : 
        	c1_x/=count_pix 
                c1_y/=count_pix
                c2_x/=count_pix
	        c2_y/=count_pix
		x=(c1_x+c2_x)/2
		y=(c1_y+c2_y)/2	


		
		pt1,pt2=(c1_x,c1_y),(c2_x,c2_y)

		return x,y
	MarkColor(xr,yr)
	MarkColor(xy,yy)
	MarkColor(xb,yb)
	MarkColor(xg,yg)
	return 0,0
		

bmin=(100,100,100) #blue HSV
bmax=(125,255,255)

rmin = (0,150,100) # red HSV
rmax = (8, 255, 255)

gmin=(40,100,100)
gmax=(80,255,255)

ymin = (20,100,100)  # yellow minimums
ymax = (30, 255, 255) #10
			
omin=(14,100,100) # Orange
omax=(18,255,255)			
flist=[]


eject_count=0
yellow_count=0

lastxr,lastyr=0,0
def settingsread():
	rd=csv.reader(open('gbc.csv','rb'),delimiter=' ',quotechar='|')
	for row in rd:
		flist.append(''.join(row))
	print flist
	
settingsread()
def MarkColor(x,y):
	global frame
	if x and y:
		cv.Line(frame, (x,y-7), (x,y+7), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x-7,y), (x+7,y), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x+5,y+5), (x-5,y-5), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x-5,y+5), (x+5,y-5), cv.CV_RGB(255,255,255),2)


def PlayBeep(sound):
		
	chunk = 1024
	wf = wave.open(sound, 'rb')
	p = pyaudio.PyAudio()
	# open stream
	stream = p.open(format =p.get_format_from_width(wf.getsampwidth()),channels = wf.getnchannels(),rate = wf.getframerate(),output = True)
	# read data
	data = wf.readframes(chunk)
	# play stream
	while data != '':
	    stream.write(data)
	    data = wf.readframes(chunk)

	stream.close()
	p.terminate()


pick,drop = 0,0
click_count=0
def MouseInterface(xr,yr,xy,yy):
	
	global pick,drop
	if xr :
		xr=640-xr
		
		x=xr*2.125 # scaling to native resolution
		y=yr*1.6
		os.system('xdotool mousemove '+str(x)+' '+str(y))
	global click_count
	if xr and xy :
		click_count+=1
	
	if click_count>5:
		
		print "click"
		os.system('xdotool click 1')
		os.system('xdotool click 1')
		click_count=0
	#print "p",pick,"d",drop
close=0
flag=0
while(1):
	
	
	frame=cv.QueryFrame(capture)	
	xy,yy=CalcPos(ymin,ymax) # assume no color detection 1st
	xg,yg=CalcPos(gmin,gmax)
	xb,yb=CalcPos(bmin,bmax)
	xr,yr=CalcPos(rmin,rmax)
	global flist
	if not flag:	
        	os.system(''+flist[2]+' http://chrome.angrybirds.com/ &')
		flag=1
	if xr and xb:
		print xr-xb
		if xr-xb in range(50,180) and abs(yr-yb)<30:
			close+=1
		if close>=10:
			close=0
			sys.exit(0)

	MouseInterface(xr,yr,xy,yy)
	#cv.Circle(frame,(xg,yg),7,cv.CV_RGB(255,136,136),-2)  #(234,173,173),-2)

	
	
	#cv.MoveWindow("Actual",60,60)
	#cv.Flip(frame,frame,1)
	#cv.ShowImage("Actual",frame)	
	#cv.ShowImage("Window_SCR",dot)
	#cv.ShowImage("Mask",imgMask)
        ShowFrame()
