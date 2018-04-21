from selenium import webdriver
from bs4 import BeautifulSoup
import csv


driver = webdriver.PhantomJS('phantomjs.exe')

def DownloadPageHtml(url):
	print 'Downloading : ' + url
	driver.get(url)
	html = driver.page_source
	return html
# http://moviescounter.co/page/497/ -- End Page
# Start page = 1
start_page = 10
end_page = 11

for x in xrange(start_page,end_page + 1):

	url = 'http://moviescounter.co/page/{}/'.format(str(x))
	filename = str(x) + '.csv'
	html = DownloadPageHtml(url)

	soup = BeautifulSoup(html,'lxml')
	maincontainer = soup.find('div',{'id':'content_box'})
	allmovie  = maincontainer.find_all('article')

	f = open(filename,'a+')
	data = [['post_type','post_status','post_title','post_content','post_category','post_tags']]
	with f:
		writer  = csv.writer(f)
		writer.writerows(data)

	for movie in allmovie:
		print movie.find('a')['href']
		soup = BeautifulSoup(DownloadPageHtml(movie.find('a')['href']),'lxml')

		post_type = 'post'
		post_status = 'publish'

		single_post_content  = soup.find('div',class_ = 'single_post')
		post_title = single_post_content.find('h1').text.encode('utf-8')

		post_content = single_post_content.find('div',class_ = 'thecontent')
		post_content.find('div',class_ = 'topad').decompose()
		post_content.find('script',{'type':'text/javascript'}).decompose()
		post_content.encode('utf-8')

		alltagandcatagory = soup.find('div',class_ = 'g')['class']


		alltag = ''
		for x in xrange(8,len(alltagandcatagory) - 1):
			alltagandcatagory[x] = alltagandcatagory[x].replace('tag-','')
			x = alltagandcatagory[x].replace('category-','')

			if x == '720p':
				alltag += x + '  '
			else:
				alltag += x + ' '


		post_tags = alltag.rsplit('  ',1)[-1].replace(' ',',')
		post_category = alltag.replace(post_tags,'').replace(' ',',')

		data = [[post_type,post_status,post_title,post_content,post_category,post_tags]]
		f = open(filename,'a+')

		with f:
			writer  = csv.writer(f)
			writer.writerows(data)


f.close()
driver.close()