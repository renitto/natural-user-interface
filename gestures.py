import cv
import os
import pyaudio,wave,sys,csv




storage = cv.CreateMemStorage(0)



capture=cv.CreateCameraCapture(0)#the value within () can be 0 or 1 depending on whether the webcam is inbuilt or external
frame=cv.QueryFrame(capture)
imgHSV = cv.CreateImage(cv.GetSize(frame), 8, 3)
imgMask = cv.CreateImage(cv.GetSize(frame), 8, 1)
b_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
scribble = cv.CreateImage(cv.GetSize(frame), 8, 3) # stores scribbles
dot=cv.CreateImage(cv.GetSize(frame), 8, 3)



contour = 0   ## dummy stmnt

x1,y1,x2,y2=0,0,0,0	


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
	
	stream = p.open(format =p.get_format_from_width(wf.getsampwidth()),channels = wf.getnchannels(),rate = wf.getframerate(),output = True)
	
	data = wf.readframes(chunk)
	
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
	
	
        while contour:
        	bound_rect = cv.BoundingRect(list(contour))
		if contour:
			area= abs(cv.ContourArea(contour))
			
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
	
	print "found"
	snap_gstr=1
						
	cv.WaitKey(1500) #1100
	
	while (xb or xr or xg or xy):
				
	        xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
				
	if snap_gstr:	
		frame=cv.QueryFrame(capture)	
		cv.SaveImage(('/home/tom/snapshot'+snap_name+str(snap_count)+".png"), frame)
		cv.DestroyWindow("Actual")
		cv.MoveWindow("Snap Shot",60,60)
		
		cv.ShowImage("Snap Shot",frame)
		cv.MoveWindow("Snap Shot",60,60)
		
		snap_count+=1
		wr=csv.writer(open('snap.csv','wb'), delimiter=' ', quotechar='|',quoting=csv.QUOTE_MINIMAL)
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
	if (yb and yg) and (not(yy or yr)):	
		
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
	os.system(''+flist[1]+' ~/Pictures &')
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

	if flag:
		os.system('xdotool key "Alt+F4"')
		cv.WaitKey(200)	
			
	cv.Flip(frame,frame,1)
        if xg-xy in range(5,70):
            close+=1
	    if close>=10:
		os.system('xdotool key "Alt+F4"')
		close=0
	
	if xr and xb and not(xy or xg) :
                print "exiting"
		print xr-xb
		if xr-xb in range(50,180):
			clos+=1
		if clos>=10:
			clos=0
			sys.exit(0)

inc_success=0 
dec_success=0 

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
		
		dec_success+=1
		print "dec"
		print dec_success
	elif dec_success:
		dec_success-=1		
	
	if dec_success==10 :
		os.system('xdotool key "BackSpace"')
		cv.WaitKey(1000)	
		dec_success=-2
		inc_success=-2
			
		
	if inc_success==10:
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
 
	

	if lxr<xr and lxy<xy and lxg>xg and lxb>xb:
		if lyy-lyr>yy-yr and lyg-lyb>yg-yb:
			zoomout+=1
	
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


mgstr= 0
def CheckMouse(xr,yr,xb,yb,xy,yy):

	global mgstr
	if yr and yb and yy ==0:
		return 0
	if yy-yr in range(5,60) and abs(xy-xr)<50:
		print xb-xr,"xb-xr" 
		if xb-xr in range(60,120):
			mgstr+=1 
	if mgstr==10:
		mgstr=0
		PlayBeep('active.wav')
		return 1
				
	return 0

toggle_count=0
mouse_t=1


def MouseToggle(xr,xb):
	global toggle_count,mouse_t
	if xr and xb and not xg:
		print xb-xr
	
		if xb-xr in range(5,70):
			toggle_count+=1
		elif toggle_count :
			toggle_count-=1
	if toggle_count>18:   
		print "mouse t"
		mouse_t*=-1
		toggle_count=0
		PlayBeep('active.wav')
		
	


click_count=0


def MouseInterface(xr,yr,xy,yy):
	
	
	if xr :
		xr=640-xr
		x=xr*2.125 # scaling to native resolution
		y=yr*1.6
		os.system('xdotool mousemove '+str(x)+' '+str(y))
		
		
def Click(xr,yr,xy,yy):


	global click_count
	if xr and xy :
		click_count+=1
	
	if click_count>10:
		
		print "click"
		os.system('xdotool click 1')
		os.system('xdotool click 1')
		click_count=0


drag,drop= 0,0

def DragnDrop(xr,yr,xy,yy):

	global lastyy,lastyr,drag,drop,ddloop

	
		
	if yr and yy == 0:
		return  
		
	if lastyy==0:
		lastyy=yy
	if lastyr==0:
		lastyr=yr


	if lastyy<yy and yr<lastyr:     #lastyr>yr and 
		drop+=1
	elif drop :
	 	drop-=1
	elif yy-yr>200:
		Click(xr,yr,xy,yy)    # if the gstr is nt for drag n drop, then check for click 

		
	
		
	


	if lastyy>yy and yr>lastyr:
		drag+=1
	elif drag:
		drag-=1

	lastyr,lastyy= yr,yy

	if drag>4:
		print "drag"
		
		os.system('xdotool mousedown 1')
		drag,drop=0,0
		return
	elif drop>4:
		print "drop"
		os.system('xdotool mouseup 1')
		drag,drop=0,0
		
		return

	
right,left,up,down=0,0,0,0
yellow_flag=0
back,fwd=0,0
altab,keydown=0,0
close=0
def KeyInterface(xr,yr,xy,yy,xb,yb,xg,yg):
	global lastxr,lastyr,right,left,up,down,yellow_flag,back,fwd,altab,keydown,close
	print "key"
	if lastxr==0:
		lastxr=xr
	if lastyr==0:
		lastyr=yr


	if xr and not(xg):
		if yr>lastyr:
			down+=1
		if yr<lastyr:
			up+=1 
		if xr>lastxr:
			left+=1
		if xr<lastxr:
			right+=1
		
	
		if down==10:
			os.system('xdotool key "Down"')
			right,left,up,down=0,0,0,0
		if up==10:
			os.system('xdotool key "Up"')		
			right,left,up,down=0,0,0,0	
		if left==10:
			os.system('xdotool key "Left"')
			right,left,up,down=0,0,0,0 
		if right==10:
			os.system('xdotool key "Right"')
			right,left,up,down=0,0,0,0
	


		if yy and yy-yr > 200:
			yellow_flag+=1
	
		if yellow_flag==6:
			os.system('xdotool key "Return"')
			yellow_flag=0



	if xb and xg and xr :

		if yy:
			
			if yy-yr>150:
				fwd+=1
				print "r"
			elif yr-yy>150:
				print "b"
				back+=1 

		else:
			if yr>lastyr:
				down+=1	
				print down
			elif down:
				down-=1

			
		
		if down>=10:
			os.system('xdotool key "Alt+F9"')
			down=0
		if back>=15:
			os.system('xdotool key "BackSpace"')
			back,fwd=0,0
			cv.WaitKey(100)

		if fwd>=15:
			os.system('xdotool key "space"')
			back,fwd=0,0
			cv.WaitKey(100)


	if yy-yr>150 and yg-yb>150 and xb-xr>100 and xg-xy>100 and (xr and xy and xb and xg):
		altab+=1
	elif altab>0:
		altab-=1
	print altab
	if altab>=10 :
		print "alt"
		os.system('xdotool keydown "Alt"')
		os.system('xdotool key "Tab"')
		cv.WaitKey(700)
		altab=5
		keydown=1
	if keydown==1 and altab==0:
					
		os.system('xdotool key "Return"')
		os.system('xdotool key "Alt"')
		keydown=0 
	
	if xr and xb:
		if xr-xb in range(50,180) and abs(yr-yb)<30:
			close+=1
		if close>=10:
			os.system('xdotool key "Alt+F4"')
			close=0
	lastxr,lastyr = xr,yr		
	
eject_count=0
yellow_count=0


def CheckEject(xb,yb,xr,yr,xy,yy,xg,yg):

	global eject_count
	if xb and xr and xg and xy:
		
		if xb-xr  in range(70,220) and xg-xy in range(70,200):
			
			if yg-yb in range(90,150) and yy-yr in range(90,150):
				eject_count+=1
				print "f"
	 
			elif eject_count:
				eject_count-=1
	if eject_count==5:
		os.system('eject')
		print "triggered"
		eject_count=0


def TriggerDrawCheck(xb,yb,xr,yr,xy,yy,xg,yg):

	global yellow_count,yellow_miss
	
	if xy and xr and not(xb or xg):
		print yy-yr
		if yy-yr > 190:
			print "yellow"
			yellow_count+=1
			if yellow_miss:
				yellow_miss-=1 # when yellow is found miss shud b decreased

			
	else :

		yellow_miss+=1

	if yellow_miss == 20:  			# then there s no detectn, reset yellow counter and limit miss counter by 20 !!
		yellow_miss,yellow_count = 0,0 
	
		#os.system('pkill vlc')
	
	if yellow_count>=15 :
		yellow_miss,yellow_count = 0,0
		PlayBeep('active.wav')				
		DrawCheck(xr,yr)
		cv.WaitKey(1000)

yellow_miss=0
green_miss=0

yellow_flag=0  # set when there s yello detection 
lastxr,lastyr=0,0
lastxb,lastyb=0,0




open_apps = [] # list of open apps 
v_corner=0  # it checks if the corner in launcher gstrs was detected
x_corner_b,x_corner_t =0,0 # bottom ad top corners of X writen in a single stroke 
c_corner_t,c_corner_b = 0,0


def DrawCheck(x,y):
	

	global v_corner,x_corner_b,x_corner_t,frame
	global c_corner_t,c_corner_b
	v_corner=0
	x_corner_b,x_corner_t = 0,0 
	c_corner_t,c_corner_b= 0,0

	firstx,firsty=x,y
	loop=90 # count the max no of frames for the gesture
	lx,ly=0,0
	red_det=50
	vright,vleft,cx = 0,0,0    # hw many frames on the either side satisfies our check for v cx-x cordinate at the corner of v
	xright,xleft,xtop = 0,0,0 # used for close gstr "X"
	cleft,cdown,cright = 0,0,0

	print "fn invoke"
	while red_det and loop<>0:
		frame=cv.QueryFrame(capture)	
		x,y=CalcPos(rmin,rmax)
		MarkColor(x,y)
		if x <> 0 :
			
			if lx==0 :
				lx,ly = x,y 
				
			vright,vleft,loop,cx=CheckVlc(lx,ly,x,y,firsty,vright,vleft,loop,cx)
			xright,xleft,xtop,loop=CheckClose(lx,ly,x,y,firstx,firsty,xright,xleft,xtop,loop)
			cleft,cdown,cright,loop=CheckChrome(lx,ly,x,y,firstx,firsty,cleft,cdown,cright,loop)			
	
		if x and y:
			lx,ly = x,y 
		else:
			red_det-=1
		ShowFrame()
		#print loop
		loop-=1
	if not loop:
		print "end of loop"
	print "return"	
	#PlayBeep('error.wav')
	cv.Flip(frame,frame,1)



""" there must be a corner where lx>x and with y at a certain distance frm the initiation of the gstr (y-firsty)
before this corner, y must be increasing and after this corner, y must b decreasing to 
get the shape "V" """


span=0 # how mant frames hav sufficient span of V

def CheckVlc(lx,ly,x,y,firsty,right,left,loop,cx):
	global flist
	global v_corner,open_apps,span 
	#print y-firsty	
	
	
	if y-firsty>130 and lx>x:
		v_corner+=1
		print "corner"
		
	if x<lx :
			if y>ly and v_corner<=10:
				right+=1
			elif ly>y and v_corner>3:
				left+=1
	
	
	if v_corner :
		if cx==0:
			cx=x
		#print "cx",cx,"x",x,cx-x
	
	#print cx-x
	if cx-x in range(280,350):
		
		print "span"
		span+=1
	if right>15 and left>15 and span>5:
		if right-left<15:  # to ensure symmetry of 'v'
			print "vlc"
			os.system(''+flist[0]+' ~/Documents/pixar.mkv &')
			ListApps('vlc')
			cv.WaitKey(500)
			loop=1
			span=0
	print right,left, 'span',span
	return right,left,loop,cx
	

def CheckClose(lx,ly,x,y,firstx,firsty,right,left,top,loop):

	global x_corner_b,x_corner_t,open_apps	
	if y-firsty>200 and lx>x and x_corner_t<8:
		x_corner_b+=1
		print "bottom corner", x_corner_b
		#print "yd",y-firsty
	if x_corner_b>5 and firstx-x >200 and ly>y:
		x_corner_t+=1
		print "top corner", x_corner_t
		#print "xd",firstx-x
	
	
	if x<lx :
		if y>ly and x_corner_b<8:
			right+=1
	if x>lx:
		if y>ly and x_corner_b>5 and x_corner_t>6:
			left+=1
	if x_corner_t<8 and x_corner_b>5:
		if abs(x-lx)< 10 and y<ly :
			top+=1
	print "r",right,"l",left,"t",top

	if right>15 and left>10 and top>3 :
		print "CLOSE"
		
		#if open_apps:
		#	name=open_apps.pop()
		#	print name
			
		os.system('xdotool key "Alt+F4"')
			
		loop=1
	return right,left,top,loop



def CheckChrome(lx,ly,x,y,firstx,firsty,left,down,right,loop):
	global c_corner_t,c_corner_b
	print c_corner_t,"top"    # 15
	if x-firstx> 200 and abs(y-ly)<5 and c_corner_b<8 and x>lx:
		c_corner_t+=1
	
	print c_corner_b, "bottom"  # 15
	if c_corner_t>5 and y-firsty> 120 and y>ly :
		c_corner_b+=1
	
	
	if c_corner_t<9 and x>lx and abs(y-ly)<30:
		left+=1
	if c_corner_t>7  and y>ly and abs(x-lx)<30:   # and c_corner_b< 14
		down+=1		

	if c_corner_b>7 and x<lx and abs(y-ly)<20:
		right+=1
	print "l",left,"d",down,"r",right
	if left>15 and down>15 and right>15:
		os.system(''+flist[2]+' www.google.co.in &')
		loop=1
		ListApps('chromium')
	return left,down,right,loop


def ListApps(name):
	global open_apps
	if name not in open_apps:
		open_apps.append(name)
	
	#print open_apps
exp_count,expf=0,0
def CheckExplorer(xr,yr,xb,yb):
	
	global lastyr,lastyb,exp_count,expf
	print xb-xr
	if lastyr==0:
		lastyr=yr
	if lastyb==0:
		lastyb=yb
	if xb-xr < 120:
		print "x fine"
		expf+=1
	if expf>4:
		if lastyr<yr and lastyb<yb:
			exp_count+=1
		elif exp_count:
			exp_count-=1
		
	if exp_count>10:
		os.system('nautilus '+flist[3])
		exp_count=0
		expf=0
	print "c",exp_count
	lastyr,lastyb=yr,yb
clos=0
close=0
while(1):

	xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
        if xg-xy in range(5,70):
            close+=1
	    if close>=10:
		os.system('xdotool key "Alt+F4"')
		close=0
	
	if xr and xb and not(xy or xg) :
                print "exiting"
		print xr-xb
		if xr-xb in range(50,180):
			clos+=1
		if clos>=10:
			clos=0
			sys.exit(0)
	CheckSnap(xr,yr,xy,yy,xg,yg,xb,yb)
	
	mouse=CheckMouse(xr,yr,xb,yb,xy,yy)
	
	if mouse==1:
		#print "mouse active"
		mouse=0
		while mouse<>1:
			print "mouse"
			#print mouse,"m",mouse_t
			xy,yy,xr,yr,xg,yg,xb,yb=GetCoords()
			mouse=CheckMouse(xr,yr,xb,yb,xy,yy)
			MouseToggle(xr,xb)
			if mouse_t==1:
				#print "Mouse"
				MouseInterface(xr,yr,xy,yy)
				DragnDrop(xr,yr,xy,yy)
			if mouse_t==-1:
				
				KeyInterface(xr,yr,xy,yy,xb,yb,xg,yg)
					
			ShowFrame() 
			cv.Flip(frame,frame,1)
			
	if xb and xr and not(xy):
		CheckExplorer(xr,yr,xb,yb) 
	CheckEject(xb,yb,xr,yr,xy,yy,xg,yg)
	if xy and xr and not(xb or xg): 	  # check for tray eject (static gstr)
		TriggerDrawCheck(xb,yb,xr,yr,xy,yy,xg,yg) # check if the gstr is to trgr a drawing gstr
        if CheckImgV(xy,yy,xr,yr,xg,yg,xb,yb):
		ShowImage(xy,yy,xr,yr,xg,yg,xb,yb)
		
        ShowFrame()		# flips the frame so put nly last
