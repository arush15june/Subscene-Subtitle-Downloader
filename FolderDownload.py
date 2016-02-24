import os,sys,zipfile
import requests
import glob
from bs4 import BeautifulSoup

def extzip(fname,location):
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

def dlzip(fname,req):
        print "DOWNLOADING ZIP"
        try:
                with open(fname,'wb') as subzip:
                        subzip.write(req.content)
        except IOError:
                print "COULD NOT WRITE ZIP"
                print "EXITING"
                sys.exit()
        print "DOWNLOADED ZIP TO : ",fname

def delzip(fname):
        print "REMOVING ZIP"
        os.remove(fname)
        print "REMOVED ZIP"

def rename(srtname,location,name):
        #rchoice = raw_input("Want to Rename Subtitle? (Y\N) : ")
        #if rchoice == 'y' or rchoice == 'Y':
                                #rename = raw_input('Rename to (-s for same as search) : ')
                #if rename == '-s':
        renloc = location+name+".srt"
        print srtname
        print renloc
        os.rename(srtname,renloc)
        print "FILE RENAMED"
        print "THANKS FOR USING THIS SCRIPT"
        sys.exit()
        #elif rchoice == 'n' or rchoice == 'N':
        #        print "THANKS FOR USING THIS SCRIPT"
        #        print "EXITING"
        #        sys.exit()

def findSub(query,location,name):
        req = requests.get(query)
        source = BeautifulSoup(req.text,"html.parser")

        subs = source.find_all('tr')
        site = "http://subscene.com"

        link = site
        #hrefs = []
        href = ''
        #nsub =0
        #snames = []
        sname = ''
        for sub in subs:
                tdata = sub.find_all('td')
                if "English" in tdata[0].get_text():
                        #nsub += 1
                        sname = tdata[0].find_all('span')[1].get_text().strip()
                        #snames.append(sname)
                        #if nsub > 10:
                        #        break
                        #print nsub,". ",sname
                        href = tdata[0].find('a')['href']
                        print "1.",sname
                        break
                        
        #schoice = int(raw_input("Select Sub : ")) - 1
                                        
        link += href

        try:
                assert(link != site)
        except AssertionError:
                print "\nSORRY SUB NOT FOUND"
                print "EXITING"
                sys.exit()

        req = requests.get(link)
        source = BeautifulSoup(req.text,"html.parser")

        subname = sname
        print "\nSubtitle : ",subname

        #choice = raw_input("Proceed? (Y/N) : ")
        #while(choice != 'y'):
        #        if(choice == 'n' or choice == 'N'):
        #                print "EXITING"
        #                sys.exit()
        #        choice = raw_input("Proceed? (Y/N) : ")
        #        

        dl = source.find('div',class_='download')	
        dlink = site+dl.a['href']

        req = requests.get(dlink)

        #location = raw_input("Save Subtitle To (folder) : ")
        if(location[len(location)-1] != '\\'):
                location += '\\'
        fname = location+'sub.zip'
        srtname = location+subname+".srt"
        dlzip(fname,req)
        extzip(fname,location)
        delzip(fname)
        rename(srtname,location,name)

def FolderSearch(currloc):
	query = "http://subscene.com/subtitles/release?q="
	formats = ['mkv','mp4']
	form = ''
	for forms in formats:
		if(len(glob.glob(currloc+'\*.%s' % forms)) > 0):
			currfile = glob.glob(currloc+'\*.%s' % forms)
			form = forms
			break;
	searchname = os.path.basename(currfile[0])
	searchname = searchname.replace(".%s" % form,"")
	name = searchname.replace(".%s" % form,"")
	print name
	searchname = searchname.replace(" ","%20")
	query += searchname+"&r=true"
	findSub(query,currloc,name)
	
def credits():
        print
        print "----------------------------"
        print "  A Script By Aarush"
        print "  facebook.com/arush15june"
        print "-----------------------------"
        print
        sys.exit()
        
#############################################

print         
print "-------------------------------"
print "| SUBSCENE SUBTITLE DOWNLOADER |"
print "-------------------------------"
print


currloc = os.path.abspath(os.getcwd())
FolderSearch(currloc)

                


		
