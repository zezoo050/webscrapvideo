from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
options = Options()
options.headless = True
DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
driver.get('INSERT LINK HERE')
login = driver.find_element_by_name("data[User][username]").send_keys("USERNAME")
password = driver.find_element_by_name("data[User][password]").send_keys("PASSWORD")
submit = driver.find_element_by_css_selector("input[value='Login']").click()
pages=['https://SAMPLE.COM/student/courses/video_list/','https://SAMPLE.COM/student/courses/video_list/']
ablinks = []
for p in pages:
	driver.get(p)
	time.sleep(10)
	links = driver.find_elements_by_css_selector("#grid_grid a")
	pglinks=[]
	for i in links:
		pglinks.append(i.get_attribute('href'))
	for i in pglinks:
		driver.get(i)
		vi = driver.find_element_by_tag_name("iframe").get_attribute('src')
		ablinks.append([i,vi])
driver.quit()
import sqlite3 as db
db = db.connect("db1.db")
row = db.execute("select * from links")
links = []
for i in row:
	links.append(str(i[0]))
x = 0
xlinks = []
for i in ablinks:
	if i[1][-9:] in links:
		xlinks.append(ablinks[x])
	x = x+1
for i in xlinks:
	ablinks.remove(i)
for i in ablinks:
	print(i)
if len(ablinks) > 0:
	from subprocess import run
	for i in ablinks:
		run('youtube-dl -v "'+i[1]+'" --refer "'+i[0]+'" -f http-240p')
	for i in ablinks:
		db.execute("insert into links values (?)",(i[1][-9:],))
		db.commit()
		print("---"+str(len(ablinks))+"---  was downloaded")
else:
	print("no new videos founded")
