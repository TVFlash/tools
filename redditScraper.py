from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen, Request
from subprocess import check_output
import click

def scrapeSub(say):

	subreddit = raw_input("Subreddit: ")

	endpoint = "http://reddit.com/r/%s"
	hdr = { 'CommandLineReddit' : 'Just scraping by' }

	req = Request(endpoint % subreddit, headers=hdr)

	f = urlopen(req)
	html =  f.read()
	f.close()

	soup =  BeautifulSoup(html, 'html.parser') 

	posts =  soup.find_all('div', {'class' : 'entry'})
	print "----------Displaying top of /r/%s----------" % subreddit
	for post in posts:
		title = post.find('a', {'class': 'title'}).text
		time = post.find('time', {'class': 'live-timestamp'}).text
		poster = post.find('a', {'class': 'author'}).text
		comments = "[ \033[1m" + post.find('a', {'class': 'comments'}).text + "\033[0m ]"
		print title, "\n\tsubmitted", time , "by", poster, comments, "\n"
		if say:
			result = check_output("say \"" + title + "\"", shell=True)

if __name__ == '__main__':
	verbal = click.confirm('Would you like the posts to be verbalized?')
	response = True
	while response:
		scrapeSub(verbal)
		response = click.confirm('Another subreddit?')
	print "Get back to work!"
	print(chr(27) + "[2J")
