import os,sys,zipfile
import requests
from bs4 import BeautifulSoup

def credits():
        print
        print "----------------------------"
        print "  A Script By Aarush"
        print "  facebook.com/arush15june"
        print "-----------------------------"
        print
        sys.exit()

print "-------------------------------"
print "| SUBSCNE SUBTITLE DOWNLOADER |"
print "-------------------------------"
print " type -c in search for credits"
print

site = "http://subscene.com"

query = "http://subscene.com/subtitles/release?q="
name = raw_input("Search (Be Specific) : ")
cname = name.replace(" ","%20")
query += cname + "&r=true"

if(name == '-c'):
        credits()

req = requests.get(query)
source = BeautifulSoup(req.text,"html.parser")

subs = source.find_all('tr')

link = site
href = ''

for sub in subs:
        tdata = sub.find_all('td')
        if "English" in tdata[0].get_text():
                href = tdata[0].find('a')['href']
                break
        
link += href

try:
	assert(link != site)
except AssertionError:
	print "\nSORRY SUB NOT FOUND"
	print "EXITING"
	sys.exit()

req = requests.get(link)
source = BeautifulSoup(req.text,"html.parser")

subname = source.find('li',class_='release')
subname = subname.find('div').get_text()
subname = subname.strip()
print "\nSubtitle Found : ",subname

choice = raw_input("Proceed? (Y/N) : ")
while(choice != 'y'):
	if(choice == 'n' or choice == 'N'):
		print "EXITING"
		sys.exit()
	choice = raw_input("Proceed? (Y/N) : ")
	
dl = source.find('div',class_='download')	
dlink = site+dl.a['href']

req = requests.get(dlink)

location = raw_input("Save Subtitle To (folder) : ")
fname = location+'sub.zip'
srtname = []

print "DOWNLOADING ZIP"
try:
        with open(fname,'wb') as subzip:
                subzip.write(req.content)
except IOError:
        print "COULD NOT WRITE ZIP"
        print "EXITING"
        sys.exit()
print "DOWNLOADED ZIP TO : ",fname

print "EXTRACTING SUBTITLE"
try:        
        with zipfile.ZipFile(fname,'r') as subzip:
                subzip.extractall(location)
except:
        os.remove(fname)
        print "ERROR"
        print "EXITING"
        sys.exit()
print "EXTRACTED SUBTITLE"

print "REMOVING ZIP"
os.remove(fname)
print "REMOVED ZIP"

srtname = location+subname+".srt"

rchoice = raw_input("Want to Rename Subtitle? (Y\N) : ")
if rchoice == 'y' or rchoice == 'Y':
        rename = raw_input('Rename to (-s for same as search) : ')
        if rename == '-s':
                rename = name
        renloc = location+rename+".srt"
        os.rename(srtname,renloc)
        print "FILE RENAMED"
        print "THANKS FOR USING THIS SCRIPT"
        sys.exit()
elif rchoice == 'n' or rchoice == 'N':
        print "THANKS FOR USING THIS SCRIPT"
        print "EXITING"
        sys.exit()
        

		
