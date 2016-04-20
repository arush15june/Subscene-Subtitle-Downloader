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

def dlzip(fname,content):
        print "DOWNLOADING ZIP"
        try:
                with open(fname,'wb') as subzip:
                        subzip.write(content)
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
        
        renloc = location+name+".srt"
        print srtname, renloc
        os.rename(srtname,renloc)
        print "FILE RENAMED"
        print "THANKS FOR USING THIS SCRIPT"
        os.system("pause")
        sys.exit()

def findSub(query,location,name):
        req = requests.get(query)
        source = BeautifulSoup(req.text,"html.parser")

        subs = source.find_all('tr')
        site = "http://subscene.com"

        link = site
        href = ''
        sname = ''
        for sub in subs:
                tdata = sub.find_all('td')
                if "English" in tdata[0].get_text():
                        sname = tdata[0].find_all('span')[1].get_text().strip()
                        href = tdata[0].find('a')['href']
                        print "1.",sname
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

        subname = sname
        print "\nSubtitle : ",subname
        dl = source.find('div',class_='download')	
        dlink = site+dl.a['href']

        req = requests.get(dlink)

        fname = location+'sub.zip'
        srtname = location+subname+".srt"
        dlzip(fname,req.content)
        extzip(fname,location)
        delzip(fname)

        rename(srtname,location,name)

def FolderSearch(currloc):
	currloc = os.path.abspath(currloc)
	query = "http://subscene.com/subtitles/release?q="
	formats = ['mkv','mp4']
	form = ''
	for forms in formats:
		if(len(glob.glob(currloc+'*.%s' % forms)) > 0):
			currfile = glob.glob(currloc+'\*.%s' % forms)
			form = forms
			break;
	searchname = os.path.basename(currfile[0])
	searchname = searchname.replace(".%s" % form,"")
	name = searchname.replace(".%s" % form,"")
	print "File Found : ",name
	searchname = searchname.replace(" ","%20")
	query += searchname+"&r=true"
	print currloc
	findSub(query,currloc,name)
	

#############################################
if __name__ == "__main__":
	print         
	print "-------------------------------------"
	print "| SUBSCENE AUTO SUBTITLE DOWNLOADER |"
	print "-------------------------------------"
	print


	currloc = os.path.abspath(raw_input("Enter Folder Path : "))+"\\"
	FolderSearch(currloc)

                


		
