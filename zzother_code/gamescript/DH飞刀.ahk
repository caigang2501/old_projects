;MsgBox ToolTip
global TESTNUM := 0
global HOOKKEY :=0
global BARPOWERRINGTIMER := 0
global BARKEY := 0
global DHKEY := 0
global TK := 0
global VERSTATUS := 0
global THREADID := 0
global CURENTTOWN := 0
global PUTBOXTIME := 0
global PUTBOXY := 0
global TimeA := 0
global TimeB := 0
global BARSTATUS := 1
global VERSTATUS := 2
global CRUSTATUS := 3
global RUNTIME := 1
global Tik := 1




F8::
getSkillColor()
return


autoFunction(fun, interval) {
    SetTimer, %fun%, %interval%
}

stopAutoFunction(fun) {
    SetTimer, %fun%, Off
	THREADID := 0
}

isHomePage(){
	PixelGetColor, home_page_color,1025,929,RGB
	return (home_page_color = 0x230400) ? True : False
}

closeBossWindow(){
	PixelGetColor, boss_winda_color, 1209,764 ,RGB
	PixelGetColor, boss_windb_color, 1119,71 ,RGB
	PixelGetColor, back_town_color, 740,850 ,RGB
	if(boss_winda_color = 0x110808){
		click,1124,916
	}
	if(boss_windb_color = 0x000000){
		click,1064,617
	}
	if(back_town_color = 0x310000){
		click,950,850
	}
}

putOneBox(x,y){
	click,right,%x%,%y%
}

decomposeOne(x,y){
	x -= 10
	y -= 15
	sum_color = 0
	Loop,2{	
		PixelGetColor, weapon_color,x,y,RGB
		r := weapon_color//0x010000
		g := Mod(weapon_color//0x000100,16*16)
		b := Mod(weapon_color,0x000100)
		sum_color += % (r+g+b)//3
		x++
	}
	aver_color = % sum_color//2
	clipboard := clipboard aver_color " "
	if(aver_color>15){
		click,%x%,%y%	
		send {Enter}
	}else{
	}
}


upDateOne(x,y){
	click,right,266,402
	click,right,%x%,%y%
	click,711,843
	click,250,834
	sleep 2000
}

upDateARow(y){
	x := 1420
	while(x < 1900){
		upDateOne(x,y)
		x += 50
	}
}
decomposeARow(y){
	x := 1420
	clipboard := clipboard "`r"
	while(x < 1900){
		decomposeOne(x,y)
		x += 50
	}
}



decomposeWeapon(){
	clipboard := ""
	decom(0x3F3E3F,253,279)
	decom(0x0B2141,316,280)
	decom(0x4C3D0A,385,278)
	click,175,280
	y := 580
	while (y < 850) {
		decomposeARow(y)		
		Y += 100
	}	
}

decom(c,x,y){
	PixelGetColor, tem_color,x,y,RGB
	if(tem_color = c){
		click,%x%,%y%	
		send {Enter}
	}
}

decomposeRing(){
	click,175,280
	y := 580
	while (y < 850) {
		decomposeARow(y)		
		Y += 50
	}
}

upDateRing(){
	y := 580
	while (y < 850) {
		upDateARow(y)
		Y += 50
	}
}

upDateWeapon(){
	y := 580
	while (y < 850) {
		upDateARow(y)		
		Y += 100
	}
}

upDateOneRow(){
	y := 580
	upDateARow(y)
}

putBox(){

	send m
	click right,1399,851
	click,1090,516
	click,881,281
	sleep 7000
	
	click, 945,484
	click right,1399,851
	click,738,615
	click,1022,488
	sleep 5000
	
    send c
	sleep 500
	PixelGetColor, box_color,1670,700, RGB
	if(box_color = 0xDAAB2A){
		click,664,110
		sleep,3000
		PUTBOXTIME := PUTBOXTIME+1		
		switch PUTBOXTIME {
		Case 1,2:
			click,160,177
			click,510,772
		Case 3,4:
			click,160,177
			click,510,657
		Case 5,6:
			click,160,177
			click,510,542
		Case 7,8:
			click,160,177
			click,510,427	
		Case 9,10:
			click,205,177
			click,510,542
		Case 11,12:
			click,205,177
			click,510,427
		}
		
		
		y := 600
		while(y < 850 ){
			x := 1420
			while(x < 1900){
				putOneBox(x,y)
				x += 50
			}						
			if(y = 800){
				click,510,312
				y :=610
			}
			y += 100
		}
	}
	send {Space}
}



getInGame(){
	if(isHomePage()){
		send {Escape}{Space}{Space}  
		click,237,523
	}
}

getOutGame(){
	send {Space}{Escape}
	sleep 100
	click,240,479
	send {Escape}
	sleep 500
	send {Space}
}

backToTownAndTakeBox(a,b,c,d,e,f){
	send m
	click right,1399,851
	click,%a%,%b%
	click,%c%,%d%
	
	sleep 5000
	click,%e%,%f%
	sleep 2000
	send {space}{space}
}

randomPosAndFight(){
	Random, TOWNPOS, 1, 5
	randomTown(TOWNPOS)
	;autoFight()
	;sleep 120000
	;StopAutoFight()
}

 

randomTown(p){
	send m
	click right,1399,851
	switch p{
		Case 1:
			click,738,616
			doTaskInTown(1,ta)					
		Case 2:
			click,1086,512
			doTaskInTown(2,tb)
		Case 3:
			click,713,397
			doTaskInTown(3,tc)
		Case 4:
			click,592,545
			doTaskInTown(4,td)
		Case 5:
			click,1452,359
			doTaskInTown(5,te)	
	}
	
}

doTaskInTown(town,a){
	i := 1
	t := a.Length()//3
	Loop, %t%{
		if(a[3*i-2] = 0){
			if(isModelExist(a[3*i-1],a[3*i],5,5,tm,town,i)){
				click,a[3*i-1],a[3*i]
				return
			}else if(i = t){
				Tik := 3
				runSign()
				Random, TOWNPOS, 1, 5
				randomTown(TOWNPOS)
			}
		}else{
			if(ifModelExist(a[3*i-1],a[3*i],tm,town,i)){
				click,a[3*i-1],a[3*i]
				return
			}else if(i = t){
				Random, TOWNPOS, 1, 5
				randomTown(TOWNPOS)
			}
		}		
		i++	
	}
}

isModelExist(x0,y0,w,h,m,t,p){
	x := x0
	y := y0
	mh := m.pop()
	mw := m.pop()
	Tik := 3
	runSign()
	Loop, %h%{
		Loop, %w%{
			runSign()
			if(ifModelExist(x,y,m,t,p) ){
				return true
			}else if(x = x0+mw-1 && y = y0+mh-1){
				return false
			}
			x++
		}
		x := x0
		y++
	}
	
}

ifModelExist(x,y,m,t,p){
	mh := m.pop()
	mw := m.pop()
	i := 1
	d := 0
	k := 0
	Loop, %mh%{
		Loop, %mw%{
			if(m[2*i-1] = 1){
				d += d(m,2,i,x,y)
				k++
			}					
			i++
			x++
		}			
		x := x - mw
		y++
	}
	x := x - mw
	y := y - mh
	if(d//k < 5){
		FileAppend, `n %t% %p% %x% %y%, C:\Users\dell\Desktop\place.txt
		return true
	}else{
		return false
	}
}


haveTask(a,b){
	if(1){
		return true
	}else{
		return false
	}
	
}

autoFight(){
	;TODO autofigh algorithm
}

StopAutoFight(){

}



backToTown(){
	CURENTTOWN++
	if(CURENTTOWN = 6){
		CURENTTOWN := 1
	}
	Switch CURENTTOWN {
		Case 1:	
			backToTownAndTakeBox(738,615,1022,488,452,401)
		Case 2:									
			backToTownAndTakeBox(1086,512,1040,779,739,177)
		Case 3:
			backToTownAndTakeBox(713,397,510,482,1310,330)
		Case 4:
			backToTownAndTakeBox(592,545,1165,620,470,343)
		Case 5:
			backToTownAndTakeBox(1452,359,508,744,1320,327)
	}
}

autoGame(){
	ReJoinGame:
	i  := 0
	autoFunction("getInGame",1000)
	sleep 60000
	putBox()
	stopAutoFunction("getInGame")
	PixelGetColor, portrait3_color1,62,472,RGB
	PixelGetColor, portrait3_color2,62,472,RGB
	while(i < 30 && portrait3_color1 = portrait3_color2 ){
		sleep 60000
		if(!isHomePage()){	
			PixelGetColor, portrait3_color1,62,472,RGB
			backToTown()
			i++
			PixelGetColor, portrait3_color2,62,472,RGB
		}else{
			FileAppend, `n Kicked out %i%, C:\Users\dell\Desktop\HookLog.txt
			goto, ReJoinGame
		}
	}
	
	FileAppend, `n GetoutGame %i%, C:\Users\dell\Desktop\HookLog.txt
	getOutGame()
	
}

LeftClick(){
	Click left
}

RightClick(){
	Click right
}

isBusy(){
	PixelGetColor, back_color, 863,328 ,RGB
	PixelGetColor, closet_color, 15,12 ,RGB
	return (back_color = 0x0A0A09 || closet_color = 0x120E0A) ? True : False
}

autoCast(a,b,c,d,e,color_a,color_b,color_c,color_d,color_e){
	if(a = 1){
		PixelGetColor, skilla_color, 658,1008 ,RGB
		if(skilla_color = color_a && !isBusy()){
			send 1
		}
	}
	
	if(b = 1){
		PixelGetColor, skillb_color, 724,1008 ,RGB
		if(skillb_color = color_b && !isBusy()){
			send 2
		}
	}else if(b = 2){
		PixelGetColor, buff_color, 705,996 ,RGB
		if(buff_color = 0x000000 || buff_color = 0x080808 && !isBusy()){
			send 2
		}
	}
	
	if(c = 1){
		PixelGetColor, skillc_color, 790,1008 ,RGB
		if(skillc_color = color_c && !isBusy()){
			send 3
		}
	}else if(c = 2){
		PixelGetColor, buff_color, 777,996 ,RGB
		if(buff_color = 0x000000 || buff_color = 0x050505 && !isBusy()){
			send 3
		}
	}
	
	if(d = 1){
		PixelGetColor, skilld_color, 858,1008 ,RGB
		if(skilld_color = color_d && !isBusy()){
			send 4
		}
	}else if(d = 2){
		PixelGetColor, buff_color, 835,996 ,RGB
		if(buff_color = 0x000000 || buff_color = 0x0A0B0B && !isBusy()){
			send 4
		}
	}else if(d = 3){
		PixelGetColor, skilld_color, 858,1008 ,RGB
		if(skilld_color = color_d && !isBusy()){
			send !z
		}
	}
	
	if(e = 1){
		PixelGetColor, skille_color, 927,1008 ,RGB
		if(skille_color = color_e && !isBusy()){
			send {e down}{click left}{e up}
		}
	}
	
	
	PixelGetColor, bloode_color, 60,126 ,RGB
	if(bloode_color = 0x000000){
		send q
	}
		
}


F5::
HOOKKEY := !HOOKKEY
if (HOOKKEY) {
	autoFunction("closeBossWindow", 2000)
	send !a
}else {
	stopAutoFunction("closeBossWindow")
}
return

!a::
while(HOOKKEY){
	autoGame()
}
Return

barAutoCastA(){
	autoCast(0,1,1,0,0,0,0x6C1C0E,0xAE3C10,0,0)
}

F1::
BARKEY := !BARKEY 
if (BARKEY) {
    send 4
	send {e down}
	click left
	send {e up}
	autoFunction("barAutoCastA", 500)
	autoFunction("barLoopB", 500)
	send {1 down}
	
}else {
	stopAutoFunction("barAutoCastA")
	stopAutoFunction("barLoopB")
	send {1 up}
}
return



barLoopA() {
	if(TimeA = 15){
		send {1 up}
		send {RButton down}		
	}else if(TimeA = 18){
		send {RButton up}
		send {1 down}
		TimeA := 0
	}
	if(TimeB = 27){
		send 4
		TimeB := 0
	}
	TimeA += 1	
	TimeB += 1		
}

barLoopB() {
	if(TimeA = 5){
		click right
		TimeA := 0
	}
	TimeA += 1			
}

barLoopD() {
	if(TimeA = 9 && !isBusy()){
		click right
		TimeA := 0
	}
	TimeA += 1			
}

barLoopC() {	
	if(TimeA = 3){
		send 4
		TimeA := 0
	}	
	TimeA += 1			
}

!z::
switch THREADID {
	Case 1:
}
return

~RButton & LButton::
return

XButton1::
	F_AutoPick := !F_AutoPick 
if(F_AutoPick){
	autoFunction("LeftClick" ,3)
}else{
	stopAutoFunction("LeftClick")
}	
return


^1::
Loop, 30 {
	Click, Right, 1
	}
return


!d::
upDateWeapon()
Return

^d::
decomposeWeapon()
Return

^f::
decomposeRing()
Return

Up::
click 229,393
click 261,778
sleep 500
click 261,778
return

^2::
upDateRing()
Return

^3::
upDateOneRow()
Return


PixeSearch(){
	PixelSearch, x, y, xx,xx,xx,xx, 0xffffff, 4, Fast
if ErrorLevel
    return False
else
    return True
}

getMousePos(){
	MouseGetPos , x , y
	Clipboard = %x%,%y%
}

getPosColor(x,y){
	PixelGetColor, color , x , y , RGB
	Clipboard = %color%
}

getMousePosAndColor(){
	MouseGetPos , x , y
	PixelGetColor, color , x , y , RGB
	Clipboard = %color% %x%,%y%
}

getMouseAreaColor(w,h){
	MouseGetPos , x , y
	clipboard = %x%,%y% `r
	Loop, %h%{
		Loop, %w%{
			PixelGetColor,c1,x,y, RGB
			Clipboard := Clipboard c1 " "
			x++
		}
		Clipboard := Clipboard "`r"
		y++
	}
}

getDecomedMouseAreaColor(w,h){
	MouseGetPos , x , y
	clipboard = %x%,%y% `r
	Loop, %h%{
		Loop, %w%{
			PixelGetColor,c1,x,y, RGB
			r := c1//0x010000
			g := Mod(c1//0x000100,16*16)
			b := Mod(c1,0x000100)
			aver_color = % (r+g+b)//3
			Clipboard := Clipboard aver_color " "
			x++
		}
		Clipboard := Clipboard "`r"
		y++
	}
}

getAreaColor(x,y,w,h){
	clipboard := "" 
	Loop, %h%{
		Loop, %w%{
			PixelGetColor,c,x,y, RGB
			x++
			Clipboard := Clipboard c " "
		}
		Clipboard := Clipboard "`r"
		y++
	}
}

getDecomAreaColor(x,y,w,h){
	clipboard := "" 
	Loop, %h%{
		Loop, %w%{
			PixelGetColor,c,x,y, RGB			
			r := c//0x010000
			g := Mod(c//0x000100,16*16)
			b := Mod(c,0x000100)
			aver_color = % (r+g+b)//3
			Clipboard := Clipboard aver_color " "
			x++
		}
		Clipboard := Clipboard "`r"
		y++
	}
}

getTaskPos(){
	MouseGetPos , x , y
	Clipboard := Clipboard "0," x "," y ","
}


getSkillColor(){
	PixelGetColor, color_a , 658 , 1008 , RGB
	PixelGetColor, color_b , 724 , 1008 , RGB
	PixelGetColor, color_c , 790 , 1008 , RGB
	PixelGetColor, color_d , 858 , 1008 , RGB
	PixelGetColor, color_e , 927 , 1008 , RGB
	Clipboard = %color_a%,%color_b%,%color_c%,%color_d%,%color_e%
}

overlapFindModel(){
	


}


generateModel(w,h){
	MouseGetPos , x , y
	Loop, %h%{
		Loop, %w%{
			PixelGetColor,c,x,y, RGB
			r0 := c//0x010000
			g0 := Mod(c//0x000100,r0*16*16)
			b0 := Mod(c,0x000100)
			r += r0
			g += g0
			b += b0
			x++
		}
		y++
	}
	return Array(r//w//h,g//w//h,b//w//h)
}

findModelByComparison(w,h,r){	
	model := []
	if(RUNTIME = 1){
		MouseGetPos , x , y
		global mousex := x
		global mousey := y
		global arr := []
		Loop, %h%{
			Loop, %w%{
				PixelGetColor,c,x,y, RGB
				arr.push(c)
				x++
			}
			x := mousex
			y++
		}
		RUNTIME := 2
	}else{
		minx := 2000
		miny := 0
		i := 1
		d := 1
		x := mousex
		y := mousey
		Loop, %h%{
			Loop, %w%{
				d := d(arr,1,i,x,y)	
				if(d > 50){
					model.push(1)
					
					if(miny = 0){
						miny := y
					}
					if(x < minx ){
						minx := x
					}
					if(x > maxx){
						maxx := x
					}
					if(y > maxy){
						maxy := y
					}
				}else{
					model.push(0)
				}
				
				if(r = 1){
					model.push(arr[i])
				}else{
					model.push(c2)
				}
				i++				
				x++
			}
			x := mousex			
			y++
		}
		x += w-1
		y--		
		x1 := x 
		y1 := y
		RUNTIME := 1
		MsgBox % minx " " miny " " maxx " " maxy "`r" mousex " " mousey " " x " " y
		MsgBox % "unCut:" model.Length()
		
		i := h*w
		Loop, %h%{
			Loop, %w%{  
				if(x < minx || y < miny || x > maxx || y > maxy){
					model.removeAt(2*i)
					model.removeAt(2*i-1)
				}
				x--
				i--
			}
			x := x1
			y--
		}
		
		Loop, %h%{
			Loop, %w%{
				i++
				FileAppend, % model[2*i-1] " ", C:\Users\dell\Desktop\model.txt				
			}
			FileAppend, `n , C:\Users\dell\Desktop\model.txt
		}
		MsgBox % "cutted:" model.Length()
		model.push(maxx-minx+1,maxy-miny+1)
		return model
	}		
}

	

d(a,n,i,x,y){
	r1 := a[n*i]//0x010000
	g1 := Mod(a[n*i]//0x000100,16*16)
	b1 := Mod(a[n*i],0x000100)
	PixelGetColor,c,x,y, RGB
	r2 := c//0x010000
	g2 := Mod(c//0x000100,16*16)
	b2 := Mod(c,0x000100)
	return (Abs(r1-r2)+Abs(g1-g2)+Abs(b1-b2))//3
}

iterator(m){
	Loop, 10{
		MsgBox % m[A_Index]
	}
}
	
runSign(){
	if(Tik = 1){
		click,100,100
		Tik := 2
	}else if(Tik = 3){
		click,100,900
		Tik := 1
	}else{
		click,100,140
		Tik := 1
	}
	
}


modelDectance(a,b){
	return Abs(a[1]-b[1])+Abs(a[2]-b[2])+Abs(a[3]-b[3])
}

F10::
global tm := [0,0x4E260A,1,0x8D683F,1,0xE6DAB2,1,0xD8C19D,1,0x8E5832,0,0x5C3217,0,0x7F6C49,1,0x618F8A,1,0x42A8B3,1,0x43C6C0,1,0x9D5C19,1,0xE2A150,1,0xE6DAB2,1,0xFFFBD6,1,0xD9C39F,0,0x804A1E,0,0x512913,0,0x58837F,1,0x40AAB7,1,0x35D4D1,1,0xC37720,1,0xBC7E3A,0,0xC9AE87,0,0xE1D3AB,1,0xE1D3AB,1,0xE48F35,0,0x320D00,0,0x514966,1,0x3C8CB9,1,0x28ACD9,0,0x854207,1,0xC36B16,1,0xCA8E40,1,0xE6A850,1,0xE6A850,1,0x915117,0,0x0F0706,0,0x5C5D6E,1,0x33B2BD,1,0x1B7CDF,0,0x5A2700,0,0x864A0E,1,0xD28D30,1,0xEFA239,0,0x814D15,0,0x562605,0,0x6F473C,1,0x3B8FAA,1,0x1F9AD3,1,0x1063E5,1,0x62432E,0,0x3A2007,1,0xB67526,0,0x865116,0,0x431E02,0,0x784F3B,1,0x517A88,1,0x20BFD6,1,0x0880F0,1,0x0A5EE8,0,0x576074,0,0x634638,0,0x462817,0,0x45291B,0,0x4C5461,0,0x4D6A8B,1,0x1FA0D4,1,0x09A4F3,1,0x0457F1,1,0x095FEB,1,0x2D85C4,1,0x4262A1,0,0x4D5C90,1,0x465E9A,1,0x3868AF,1,0x2390D0,1,0x10BEED,1,0x036BF4,1,0x0173F9,1,0x096EED,1,0x1EC4EA,1,0x1E7FDC,1,0x1F68D4,1,0x1F67D4,1,0x1972E0,1,0x18ABEC,1,0x0B88F4,1,0x0250F1,1,0x0567F4,1,0x178BE8,1,0x14CFFB,1,0x0F9CF6,1,0x096EF3,1,0x096EF3,1,0x0E98F6,1,0x12C6F8,1,0x0352F2,1,0x045EF3,1,0x077FF6,1,0x1998EC,10,10]
global ta := [0,442,317,0,459,443,0,469,662,0,520,789,0,577,577,0,581,242,0,622,365,0,684,477,0,749,649,0,806,787,0,785,202,0,883,329,0,973,725,0,1097,284,0,1287,361,0,1396,442,0,1316,553]  
global tb := [0,464,296,0,479,515,0,582,230,0,872,270,0,874,550,0,851,662,0,1141,361,0,1279,593,0,1429,374,0,1315,216]  
global tc := [0,571,598,0,526,715,0,702,788,0,628,325,0,603,210,0,797,454,0,870,301,0,1053,158,0,1134,778,0,1314,598,0,1404,463,0,1315,328,0,1382,167]  
global td := [0,467,271,0,634,343,0,550,509,0,686,617,0,983,379,0,1027,559,0,1035,751,0,1028,239,0,1227,418,0,1382,570,0,1472,436,0,1473,293,0,1373,162]  
global te := [0,514,279,0,477,621,0,520,800,0,768,703,0,788,318,0,1044,165,0,1167,391,0,1427,454,0,1410,285,0,1315,107]
return

F9::
i := 1
Loop % model.Length(){
	clipboard := clipboard model[i] ","
	i++
}
return

F6::
Tik := 3
return





