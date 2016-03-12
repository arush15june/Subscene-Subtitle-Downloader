import os,sys,zipfile
import requests
from bs4 import BeautifulSoup


def remzip(fname):
        print "REMOVING ZIP"
        os.remove(fname)
        print "REMOVED ZIP"
        
def extzip(fname):
        print "EXTRACTING SUBTITLE"
        print os.path.dirname(fname)
        try:        
                with zipfile.ZipFile(fname,'r') as subzip:
                        subzip.extractall(os.path.dirname(fname))
        except:
                os.remove(fname)
                print "ERROR"
                print "EXITING"
                sys.exit()
        print "EXTRACTED SUBTITLE"

def dlzip(fname,req):
        print "DOWNLOADING ZIP"
        try:
                with open(fname,'wb') as subzip:
                        subzip.write(req.content)
        except IOError:
                print "COULD NOT WRITE ZIP"
                print "EXITING"
                os.system("pause")
                sys.exit()
        print "DOWNLOADED ZIP TO : ",fname


def rename(srtname,location,name):
        rchoice = raw_input("Want to Rename Subtitle? (Y\N) : ")
        if rchoice == 'y' or rchoice == 'Y':
                rename = raw_input('Rename to (-s for same as search) : ')
                if rename == '-s':
                        rename = name
                renloc = location+rename+".srt"
                os.rename(srtname,renloc)
                print "FILE RENAMED"
                print "THANKS FOR USING THIS SCRIPT"
                os.system("pause")
                sys.exit()
        elif rchoice == 'n' or rchoice == 'N':
                print "THANKS FOR USING THIS SCRIPT"
                print "EXITING"
                os.system("pause")
                sys.exit()

def findSub(query):
        req = requests.get(query)
        source = BeautifulSoup(req.text,"html.parser")

        subs = source.find_all('tr')


        link = site
        hrefs = []
        nsub = 0
        snames = []
        for sub in subs:
                tdata = sub.find_all('td')
                if "English" in tdata[0].get_text():
                        nsub += 1
                        sname = tdata[0].find_all('span')[1].get_text().strip()
                        snames.append(sname)
                        if nsub > 10:
                                break
                        print nsub,". ",sname
                        hrefs.append(tdata[0].find('a')['href'])
                        
        schoice = int(raw_input("Select Sub : ")) - 1
        href = hrefs[schoice]	
                                        
        link += href

        try:
                assert(link != site)
        except AssertionError:
                print "\nSORRY SUB NOT FOUND"
                print "EXITING"
                os.system("pause")
                sys.exit()

        req = requests.get(link)
        source = BeautifulSoup(req.text,"html.parser")

        subname = snames[schoice]
        print "\nSubtitle : ",subname

        choice = raw_input("Proceed? (Y/N) : ")
        while(choice != 'y'):
                if(choice == 'n' or choice == 'N'):
                        print "EXITING"
                        os.system("pause")
                        sys.exit()
                choice = raw_input("Proceed? (Y/N) : ")
                
        dl = source.find('div',class_='download')	
        dlink = site+dl.a['href']

        req = requests.get(dlink)

        location = os.path.abspath(raw_input("Save Subtitle To (folder) : "))+'\\'
        fname = location+'sub.zip'
        srtname = location+subname+".srt"
        dlzip(fname,req)
        extzip(fname)
        remzip(fname)
        rename(srtname,location,name)
		
def credits():
        print
        print "----------------------------"
        print "  A Script By Aarush"
        print "  facebook.com/arush15june"
        print "-----------------------------"
        print
        os.system("pause")
        sys.exit()
        
#############################################
        
print "-------------------------------"
print "| SUBSCENE SUBTITLE DOWNLOADER |"
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
findSub(query)


                


		
