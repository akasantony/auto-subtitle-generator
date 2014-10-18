#! /usr/bin/env python

from sys import argv
import os
import urllib2
from bs4 import BeautifulSoup
import zipfile

def main():
    filenames = os.listdir(os.getcwd())
    query_url = "http://subscene.com/subtitles/release?q="
    for filename in filenames:
        if filename.endswith(('.avi','.mkv','.mp4','.3gp','.flv')):
            filename_cc = filename
            filename = filename[:-3].strip('.')
            query_url = query_url + filename
            query_url = "+".join(query_url.split())
            print "Request query URL: ", query_url
            query_content = urllib2.urlopen(query_url).read()
            print query_content
            query_parsed_html = BeautifulSoup(query_content)
            title_div =  query_parsed_html.body.findAll('div',attrs={'class':'title'})
            print title_div
        #sub_url = "http://subscene.com" + title_div[0].a['href']
        #print "Subtitle URL: ",sub_url
        #sub_content = urllib2.urlopen(sub_url).read()
        #sub_parsed_html = BeautifulSoup(sub_content)
        #print sub_parsed_html
            title_div = query_parsed_html.body.findAll('td',attrs={'class':'a1'})
            print title_div
        
            for i in range(0,len(title_div)):
                sub_dl_url = "http://subscene.com"+title_div[i].a['href']
                if('/english/' in sub_dl_url):
                    print sub_dl_url
                    dl_content = urllib2.urlopen(sub_dl_url).read()
                    dl_html = BeautifulSoup(dl_content)
                    dl_link = dl_html.body.findAll('div',attrs={'class':'download'})
                    dl_link = "http://subscene.com"+dl_link[0].a['href']
                    print dl_link
                    f = urllib2.urlopen(dl_link)
                    with open(os.path.basename("srt.zip"),"wb") as local_file:
                        local_file.write(f.read())
                        local_file.close()
                        break
        
            srt_file = open('srt.zip','rb')
            with zipfile.ZipFile(srt_file) as z:
                z.extractall()
            for srt_filename in filenames:
                if srt_filename.endswith(('.srt')):
                    print filename_cc
                    os.rename(srt_filename, filename_cc[:-3]+"srt")

#print "File name is: %s" %filename

if __name__ == "__main__":
    main()


