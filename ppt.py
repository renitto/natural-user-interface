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
import cv
import os
import pyaudio,wave,sys,csv


#cv.NamedWindow("Actual",cv.CV_WINDOW_AUTOSIZE)
#cv.NamedWindow("Window_SCR",cv.CV_WINDOW_AUTOSIZE)
#cv.NamedWindow("Mask",cv.CV_WINDOW_AUTOSIZE)

storage = cv.CreateMemStorage(0)



capture=cv.CreateCameraCapture(0)#the value within () can be 0 or 1 depending on whether the webcam is inbuilt or external
frame=cv.QueryFrame(capture)
imgHSV = cv.CreateImage(cv.GetSize(frame), 8, 3)
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

yellow_flag=0  # set when there s yello detection 
lastxr,lastyr=0,0
lastxb,lastyb=0,0
lastyx,lastyy= 0,0
xr,yr,xb,yb,xg,yg,xy,yy=0,0,0,0,0,0,0,0



bmin=(97,100,100) #blue HSV
bmax=(125,255,255)

rmin = (0,110,100) # red HSV
rmax = (10, 255,255)

gmin=(40,100,100)
gmax=(80,255,255)

ymin = (20,110,100)  # yellow minimums
ymax = (30, 255, 255) #10
			
omin=(14,100,100) # Orange
omax=(18,255,255)			
flist=[]

def settingsread():
	rd=csv.reader(open('gbc.csv','rb'),delimiter=' ',quotechar='|')
	for row in rd:
		flist.append(''.join(row))
	print flist
	
settingsread()
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
	return 0,0	


def GetCoords():

	global frame,xy,yy,xr,yr,xg,yg,xb,yb
	frame=cv.QueryFrame(capture)	
	xy,yy=CalcPos(ymin,ymax) #assume no color detection 1st
	xg,yg=CalcPos(gmin,gmax)
	xb,yb=CalcPos(bmin,bmax)
	xr,yr=CalcPos(rmin,rmax)
	MarkColor(xr,yr)
	MarkColor(xy,yy)
	MarkColor(xb,yb)
	MarkColor(xg,yg)
	return xy,yy,xr,yr,xg,yg,xb,yb
def ShowFrame():

	global frame
	cv.Flip(frame,frame,1)
	cv.MoveWindow("Actual",60,60)
	cv.ShowImage("Actual",frame)	
	cv.WaitKey(10)
def MarkColor(x,y):
	global frame
	if x and y:
		cv.Line(frame, (x,y-7), (x,y+7), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x-7,y), (x+7,y), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x+5,y+5), (x-5,y-5), cv.CV_RGB(255,255,255),2)
		cv.Line(frame, (x-5,y+5), (x+5,y-5), cv.CV_RGB(255,255,255),2)



snap_gstr=0
rd=csv.reader(open('snap.csv','rb'),delimiter=' ',quotechar='|')#read snap no from file
for row in rd:
	snap_count=int(''.join(row))
snap_name="snap"


def take_snap(xr,yr,xy,yy,xg,yg,xb,yb):
	
	global snap_gstr,snap_count,snap_name
	
	
	if (yb-yr)>150 and (yy-yg)>150 and (xr-xy)>150 and (xg-xb)>150:
			print "found"
			snap_gstr=1
						
			cv.WaitKey(1500) #1100
			#src_region = cv.GetSubRect(frame, cv.Rect((xb,yb),(xr,yr), new_width, new_height) )
			while (xb or xr or xg or xy):
				#cv.WaitKey(100)
				xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
				#cnt-=1
	if snap_gstr:	
		frame=cv.QueryFrame(capture)	
		cv.SaveImage(('~/'+snap_name+str(snap_count)+".png"), frame)
		cv.DestroyWindow("Actual")
		cv.MoveWindow("Snap Shot",60,60)
		
		cv.ShowImage("Snap Shot",frame)
		cv.MoveWindow("Snap Shot",60,60)
		
		snap_count+=1
		wr=csv.writer(open('snap.csv','wb'), delimiter=' ', quotechar='|',quoting=csv.QUOTE_MINIMAL)#write 2 file
		wr.writerow(str(snap_count))
		snap_gstr=0
		cv.WaitKey(1500)
		cv.DestroyWindow("Snap Shot")
				

def CheckSnap(xr,yr,xy,yy,xg,yg,xb,yb):
	if xb and xr and xg and xy:
		print "all colors"
		if (xr-xg)<50 and (xy-xb)<50 and (yr-yg)<50 and (yy-yb)<50:
			print "trigger snap"
			take_snap(xr,yr,xy,yy,xg,yg,xb,yb)

invoke_ShowImage=0

def CheckImgV(xy,yy,xr,yr,xg,yg,xb,yb):
	global invoke_ShowImage
	if (yb and yg) and (not(yy or yr)): # if there are only yello and red	
		
		if yg-yb in range(50,90):
			invoke_ShowImage+=1
			print "show Image"
		if invoke_ShowImage==15: 
			print "invoke show Image"
			invoke_ShowImage=-5
			return 1
		
	return 0


def ShowImage(xy,yy,xr,yr,xg,yg,xb,yb):

	global frame
	global flist
	zoomed,flag=0,0
	os.system('xdg-open ~/ppt/test.ppt&')
      

	while not flag:
		
		xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
		flag=CheckImgV(xy,yy,xr,yr,xg,yg,xb,yb)
		if yr and yy and not(yg or yb):
			BackNext(yr,yy)
		if yy and yr  and yg and yb:
			zoomed=Zoom(xr,yr,xy,yy,xb,yb,xg,yg)
		if yb and yg and zoomed and not(yr or yy):
			Move(xb,yb,xg,yg)
		ShowFrame()

	if xg-xy in range(5,70):
             close+=1
	     if close>=10:
		os.system('xdotool key "Alt+F4"')
		close=0
		
		cv.WaitKey(200)	
        
        	
      
			
	cv.Flip(frame,frame,1)

inc_success=0 # decides whether or nt to go for the nxt image display
dec_success=0 # whether to go fir the previous image

def BackNext(yr,yy):
	global inc_success,dec_success 
		
	if yy-yr > 200 :
		print yy-yr
		inc_success+=1
		print "inc"
	elif inc_success:
		inc_success-=1	
	print inc_success
	if yr-yy > 200:
		print yr-yy
		dec_success+=1
		print "dec"
		print dec_success
	elif dec_success:
		dec_success-=1	
		
	if inc_success==5:
                os.system('xdotool key "F5"')
	if dec_success==5 :
		os.system('xdotool key "BackSpace"')
		cv.WaitKey(1000)	
		dec_success=-2
		inc_success=-2
			
		
	if inc_success==8:
		os.system('xdotool key "space"')
		cv.WaitKey(1000)	
		inc_success=-2
		dec_success=-2


zoomin,zoomout,zoomed=0,0,0
lxr,lyr,lxy,lyy,lxg,lyg,lxb,lyb=0,0,0,0,0,0,0,0

def Zoom(xr,yr,xy,yy,xb,yb,xg,yg):
	
	global zoomin,zoomout,lxr,lyr,lxy,lyy,lxg,lyg,lxb,lyb,zoomed
	
	if lxr ==0:
		lxr,lyr=xr,yr
	if lxy==0:
		lxy,lyy=xy,yy
	if lxb==0:
		lxb,lyb=xb,yb
	if lxg==0:
		lxg,lyg=xg,yg
 
	#if yy-yr <80 and yg-yb<80:

	if lxr<xr and lxy<xy and lxg>xg and lxb>xb:
		if lyy-lyr>yy-yr and lyg-lyb>yg-yb:
			zoomout+=1
	#if yy-yr >100 and yg-yb > 100:	
	if lxr>xr and lxy>xy and lxg<xg and lxb<xb:
		if lyy-lyr<yy-yr and lyg-lyb<yg-yb:
			zoomin+=1

	if zoomin==2:
		os.system('xdotool key "Ctrl+plus"')
		os.system('xdotool key "Ctrl+plus"')
		zoomed+=1
		print "zoom in"
		zoomin,zoomout = 0,-2
		
		

	if zoomout==2:
		os.system('xdotool key "Ctrl+minus"')
		os.system('xdotool key "Ctrl+minus"')
		os.system('xdotool key "Ctrl+minus"')
		zoomed-=1
		print "zoom out"
		zoomout,zoomin= 0,-2
		


	lxr,lyr,lxy,lyy,lxg,lyg,lxb,lyb=xr,yr,xy,yy,xg,yg,xb,yb		
	print zoomin,zoomout,"z"
	return zoomed

left,right,up,down=0,0,0,0 # ctrl movements
def Move(xb,yb,xg,yg):
	global left,right,up,down,lxg,lyg
	if yg-yb<100:
		return
	if lxg==0:
		lxg=xg
	
	if lxg>xg:
		right+=1
	elif lxg<xg:
		left+=1
	if lyg<yg:
		down+=1
	elif lyg>yg:
		up+=1

	if down==5:
		print "dwn"
		os.system('xdotool key "Down"')
		os.system('xdotool key "Down"')
		up,down=0,0
	if up==5:
		print "up"
		os.system('xdotool key "Up"')
		os.system('xdotool key "Up"')
		up,down=0,0
	if right==10:
		print "right"
		os.system('xdotool key "Right"')
		os.system('xdotool key "Right"')
		right,left=0,0
	if left==10:
		os.system('xdotool key "Left"')
		os.system('xdotool key "Left"')
		right,left=0,0
		print "left"
	lxg=xg	


close=0
clos=0
while(1):

	xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
	
        if xg-xy in range(5,70):
            close+=1
	    if close>=10:
		os.system('xdotool key "Alt+F4"')
		close=0
	
	if xr and xb and not (xy or xg):
                print "exiting"
		print xr-xb
		if xr-xb in range(50,180):
			clos+=1
		if clos>=10:
			clos=0
			sys.exit(0)
              
        if CheckImgV(xy,yy,xr,yr,xg,yg,xb,yb):
		ShowImage(xy,yy,xr,yr,xg,yg,xb,yb)
	
	ShowFrame()		# flips the frame so put nly last
