import sys
import time
import curses
import pkgutil
from pixmodules import *

def displayClasses(pix):
	subclasses = PixModule.__subclasses__()
	for x in range(len(subclasses)):
		pix.pixels[int((x/5)*2)][int(x%5)] = subclasses[x](None).getColor()

def displayMenu(pix, selectedItem):
	subclasses = PixModule.__subclasses__()
	for x in range(5):
		pix.pixels[int((x/5)*2+1)][int(x%5)] = [0,0,0]
	for x in range(len(subclasses)):
		if x == selectedItem:
			pix.pixels[int((x/5)*2+1)][int(x%5)] = [255,255,255]
	pix.pixels[1] = pix.pixels[1][::-1]
	pix.pixels[3] = pix.pixels[3][::-1]

def runModuleMenu(spidev):
	# start menu
	pix = PixModule(spidev)
	pix.start()
	displayClasses(pix)
	selectedItem = 0
	try:
		while True:
			displayMenu(pix,selectedItem)
			char = stdscr.getch()
			if(char == 97): #left (NEXT)
				selectedItem = (1+selectedItem) % len(PixModule.__subclasses__())
				print selectedItem
			if(char == 115): #right (ENTER)
				break
	except:
		raise Exception()
	finally:
		pix.stop()
		pix.join()
	return selectedItem

def runSelectedMenu(selectedItem):
	a = 0
	pix = PixModule.__subclasses__()[selectedItem](spidev)
	pix.start()
	try:
		while True:
			print a
			char = stdscr.getch()
			if(char == 97):
				pix.left()
				if a < 6:
					a += 1
				else:
					a = 0
			if(char == 115):
				pix.right()
				if a > 5:
					a += 1
				else:
					a = 0
			if a == 10:
				break
	except:
		raise Exception()
	finally:
		pix.stop()
		pix.join()

if __name__ == '__main__':	
	print "Pix gestartet"
	stdscr = curses.initscr()
	spidev = file("/dev/spidev0.0", "wb")
	try:
		while True:
			# select item
			selectedItem = runModuleMenu(spidev)
			# run item
			runSelectedMenu(selectedItem)
	except Exception as e:
		print e
	finally:
		curses.endwin()	
	print "Pix beendet"

