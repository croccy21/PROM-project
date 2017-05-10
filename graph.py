import GnuPlot

def graph():
	file = open("AccessLog","r")
	data = [] 
	x = []
	y = []
	for line in file:
		l = line.split(",")
		time = l[0].split(" ")[3]
		time = time.split(":")
		time = time[0]+time[1]+time[3]
		x.append(time)
		if "acessed" in l[1]:
			data.append([time,2])
			y.append("2")
		elif "denied" in l[1]:
			data.append([time,1])
			y.append("1")
		else:
			data.append([time,0])
			y.append("0")
		
	
	g = Gnuplot.GnuPlot()
	g.title("Access Attempts")
	
	g.xlable("Time (hhmmss)")
	g.ylable("Success = 2, denied = 1, Other = 0")
	g("set grid")
	g("set xtic 10")
	g("set ytic 1")
	
	d = Gnuplot.Data (x,y)
	
	g.plot(d)
	g.hardcopy(filename="AccessGraph.jpg",terminal="jpg")
	del g
	