
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
import pickle
  
substr = '/r/AskReddit/comments/'

class RedditPost:
    def __init__(self, title, url):
        self.url = url
        self.title = title
        self.comments = []
        
    def add_comment(self, comment):
        self.comments.append(comment)
        
    def add_list(self, list):
        for x in list:
            self.comments.append(x)
            
    def printinfo(self):
        for x in self.comments:
            print(' by {} : {} || {} upvotes \n'.format(x.user, x.text, x.upvotes))

class Comment:
    def __init__(self, text, upvotes, user):
        self.text = text
        self.upvotes = upvotes
        self.user = user




def getWeekly():
      
    url = "https://www.reddit.com/r/AskReddit/top/?t=day"
    
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url) 
    
    time.sleep(5) 
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find('div', {'class' : 'rpBJOHq2PR60pnwJlUyP0'})
    posts = set(all_divs.find_all('a', href=True))
    titles = set(all_divs.find_all('h3'))

    rList = []
    for post in posts:
        rurl = post['href']
        
        if substr in (rurl):
            possible_title = (rurl[29:])
            remove_under = possible_title.replace('_', ' ')
            remove_slash = remove_under.replace('/', '')
            
            for x in titles:
                if (remove_slash) in (x.text).lower():
                    rList.append(RedditPost(x.text, 'https://www.reddit.com'+rurl))
        
    driver.close() # closing the webdriver
    return rList



def getPostData(post):

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(post.url) 
    
    time.sleep(5) 
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find_all('div', {'class' : '_3tw__eCCe7j-epNCKGXUKk'})
    
    commentList = []
    for x in all_divs:
        comment = x.text
        if 'level 1' in comment:
            
            remove_level = comment.replace('level 1', '')
            sub = comment.find('ago')
            endlocation = comment.find('Reply')
            username = (remove_level[:sub-16])
            trimmed = remove_level[sub-4:endlocation-7]

            # to find upvotes
            c=5
            
            for x in trimmed[-5:]:
                c-=1
                if x.isnumeric():
                    break
            
            text = (trimmed[:len(trimmed)-(c+1)])
            upvotes =  (trimmed[len(trimmed)-(c+1):])
            
            redditComment = Comment(text, upvotes, username)
            commentList.append(redditComment)
    
    return commentList

        
def main():
    p = getWeekly()
    with open('posts.json', 'wb') as file:
        for x in p:
            x.add_list(getPostData(x))
            pickle.dump(x, file)
    
    
main()
