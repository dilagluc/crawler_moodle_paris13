from datetime import datetime
import urllib
import mechanize #install
from bs4 import Tag, NavigableString, BeautifulSoup #install
import urllib.request as urllib2
import http.cookiejar as cookielib
#import cookielib #install
import os, errno 
import re #install
import pdfcrowd #install
import wget
import cgi

moodle_login_url = "https://cas.univ-paris13.fr/cas/login?service=https%3A%2F%2Fmoodlelms.univ-paris13.fr%2Flogin%2Findex.php%3FauthCAS%3DCAS"
moodle_login_redirect_page = "https://moodlelms.univ-paris13.fr/my/"



		# self.br.download_link(link=url, file=path)



def init(moodle_username,moodle_password):
	# cj = cookielib.CookieJar()
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	#Browser Options
	br.set_handle_equiv(True)
	# br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Chrome')]

	#Open PUCRS Moodle
	br.open(moodle_login_url)
	br.select_form(nr=0)
	br['username'] = moodle_username
	br['password'] = moodle_password
	br.submit()

	if not br.geturl() == moodle_login_redirect_page:
		print ('Username and/or password invalid')
		return 0
	else:
		print ('Logged in')
		
	p=br.select_form(nr=1)
	
	
	soup = BeautifulSoup(br.response().read(),'lxml')
	
	# print "\n\n\n\n"
	if not os.path.exists('./output'):
		os.makedirs('./output')
	soup.findAll('script')[0].extract()
	#save_pdf(soup,'./output/my.pdf')

	soup = soup.find(role='main')
	#print(soup)
	soup = soup.findAll("div",{"data-region":{"course-events-container"}}) #data-region="course-events-container
	#print (soup)
	links = []
	name = []
	for course in soup:
		# course_name = course.find("h3",{"class":{"name"}})
		course_info = course.find('div',{'class':{'course-info-container'}}) #course-info-container
		course_name = course_info.h4.a
		#print(course_name)
		course_link = course_name['href']
		links.append(course_link)
		#name.append(course_title)
		#print(course_link)
		course_title = course_name.string	
		name.append(course_title)
		course_data = "Course: "+course_title+"\n"+"Link: "+course_link+"\n"	
	    
	for j in range(len(links)):
		#print(links[j])
		br.open(str(links[j]))
		soup_course = BeautifulSoup(br.response().read(),'lxml')
		p=soup_course.find('div',{'class':{'container outercont'}})
		
		course_content = p.find('div',{'class':{'course-content'}})
		modsections = course_content.findAll('div',{'class':{'activityinstance'}})
		course_dir = "./"+ 'output/' + name[j]
		if not os.path.exists(course_dir):
			os.makedirs(course_dir)
		for ii in modsections:
		    if ii.a == None:
		        jjj=""
		    else:
		        try:
		            jjj=ii.a['href']
		            br.open(jjj)
		            soup_cou = BeautifulSoup(br.response().read(),'lxml')
		            aa=soup_cou.find('section',{'id':{'region-main'}})
		            try:
		                tt=aa.a['href']
		                if(aa.a.string !=None ):
		                    nom = aa.a.string
		                resp = br.open(tt)
		                file_type = resp.info()['Content-Disposition']
		                print(file_type)
		                ff = datetime.now().strftime("%I:%M:%S")
		                print(ff)
		                if(file_type != None):
		                    val, param = cgi.parse_header(file_type)
		                    filename = param["filename"]
		                    f = open(str(course_dir)+"//"+ff+filename, "wb")
		                    f.write(resp.read())
		            except Exception:
		                pass
		        
		                   
                    
		    
		        
		        except Exception:
		            pass



    
		
		'''course_content = course_content.findAll('a',{'class':{''}})
		for i in course_content:
		    #link = i['href'].find("resource")
		    if (i['href'].find("resource") != -1):
		        link = i['href']
		        
		        #wget.download(link)
		       # r = br.click_link(link)
		        resp = br.open(link)
		        #resp.raise_for_status()
           
		        file_type = resp.info()['Content-Disposition']
		        j=j+1
		        type(file_type)
		        #print (resp.read())
		        if(file_type != None):
		            val, param = cgi.parse_header(file_type)
		            filename = param["filename"]
		            oo = datetime.now().strftime("%I:%M:%S")
		            #print(filename)
		            f = open(str(course_dir)+"//"+oo+filename, "wb")
		            f.write(resp.read())
		        '''
		        #file_type= file_type.strip('Content')
		        #br.retrieve(link)[0]
		        
		     #   print(file_type)
		        
        
		
		#print(link)
		
		
		    
		# course_topics = course_content.find('ul',{'class':{'topics'}}).findAll('li')
		#course_topics = course_content.ul
		
	
		    
		
		

name= input("votre numero etudiant")
mdp= input("mot de passe")
init(name, mdp)
