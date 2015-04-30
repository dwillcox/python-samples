import requests

#cd = {'cookie name':'cookie value'}
cd = {}

siteurl = 'http://en.wikipedia.org/wiki/Main_Page'

r = requests.get(siteurl,cookies=cd)
# r.content gets you all the html but you can't iterate over lines
# properly because the line breaks are messed up.
# Writing to a file, below, is a quick fix and lets you store the webpage also.
webcontent = r.content

f = open('wikipedia_main_page.txt','w')
f.write(webcontent)
f.close()

webpage = open('wikipedia_main_page.txt','rU')
# Browse the webpage as a text file with proper line breaks

# Download an image and save it.
jpgurl = 'http://upload.wikimedia.org/wikipedia/commons/e/e5/1730_Homann_Map_of_Scandinavia%2C_Norway%2C_Sweden%2C_Denmark%2C_Finland_and_the_Baltics_-_Geographicus_-_Scandinavia-homann-1730.jpg'
jpgname = 'HomannMap.jpg'
r = requests.get(jpgurl,cookies=cd)
f = open(jpgname,'wb')
f.write(r.content)
f.close()
