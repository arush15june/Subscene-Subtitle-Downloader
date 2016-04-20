import os,sys,zipfile
import requests
from bs4 import BeautifulSoup

site = "http://subscene.com"


def remzip(fname):
	try:
        os.remove(fname)
    except IOError:
    	print "Couldn't delete ZIP file"


def extzip(fname):
        print os.path.dirname(fname)
        try:        
                with zipfile.ZipFile(fname,'r') as subzip:
                        subzip.extractall(os.path.dirname(fname))
        except:
                os.remove(fname)
                print "Could not extract ZIP file"
                sys.exit()
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
        if rchoice in 'yY':
                rename = raw_input('Rename to (-s for same as search) : ')
                if rename == '-s':
                        rename = name
                renloc = location+rename+".srt"
                os.rename(srtname,renloc)
                print "FILE RENAMED"
                print "THANKS FOR USING THIS SCRIPT"
                os.system("pause")
                sys.exit()
        elif rchoice in 'nN':
                print "THANKS FOR USING THIS SCRIPT"
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

       	#SUB LIST EXTRACTION

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

        try:
                assert(len(hrefs)!= 0)
        except AssertionError:
                print "SORRY SUB COULD NOT BE FOUND"
                print "EXITING"
                sys.exit(1)
                        
        schoice = int(raw_input("Select Sub : ")) - 1
        href = hrefs[schoice]	
                                        
        link += href

        try:
                assert(link != site)
        except AssertionError:
                print "\nSORRY SUB NOT FOUND"
                restart()

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

        location = os.path.abspath(raw_input("Save Subtitle To (folder) -s for current folder : "))+'\\'
        if location == '-s':
                location = os.path.abspath(os.getcwd())+"\\"
        fname = location+'sub.zip'
        srtname = location+subname+".srt"
        dlzip(fname,req)
        extzip(fname)
        remzip(fname)
        rename(srtname,location,name)

def SearchQuery(name):
	query = "http://subscene.com/subtitles/release?q="
	cname = name.replace(" ","%20")
	query += cname + "&r=true"
	return query	

def restart():
	os.system('pause')
	os.system('cls')
	os.system('"'+__file__+'"')

def credits():
        print
        print "----------------------------"
        print "  A Script By Aarush"
        print "  facebook.com/arush15june"
        print "-----------------------------"
        print
        os.system("pause")
        print


if __name__ == "__main__":        
	os.system('cls')
	print "-------------------------------"
	print "| SUBSCENE SUBTITLE DOWNLOADER |"
	print "-------------------------------"
	print " type -c in search for credits"
	print 
	
	name = raw_input("Search (Be Specific) : ")
	if(name == "-c"):
		credits()
		restart()
	else:
		try:
			findSub(SearchQuery(query))
		except:
			print
			print "// Something Went Wrong //"
			print
			restart()
			
                


		
