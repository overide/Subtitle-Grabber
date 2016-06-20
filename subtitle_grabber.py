#---------------------------------------------------------------------
#Name      : Subtitle Grabber
#Purpose   : Download English subtitle of movie
#Author    : Atul Kumar
#Created   : 20/06/2016
#License   : GPL V3
#Copyright : (c) 2016 Atul Kumar (www.facebook.com/atul.kr.007)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Contact Author at atulkumar0417@gmail.com
#-----------------------------------------------------------------------

import requests
import bs4
import zipfile
import re,os,sys

def download_unzip(request_obj,download_path):
	with open(download_path+".zip",'wb') as fh:
		for chunk in request_obj.iter_content(100000):
			fh.write(chunk)
		fh.close()
		zh=zipfile.ZipFile(download_path+".zip")
		zh.extractall(download_path+"\\")
		zh.close()
		os.unlink(download_path+".zip")
		print('Download Location: '+download_path)
		print("Subtitle Downloaded Successfully!")


def download_subtitle(download_url,movie_name):
	res3=requests.get(download_url)
	download_path='c:\\subtitle_grabber\\'+movie_name
	if os.path.exists('c:\\subtitle_grabber\\'):
		download_unzip(res3,download_path)

	else:
		os.makedirs('c:\\subtitle_grabber\\')
		download_unzip(res3,download_path)


def search(movie_name):
	print("Searching...")
	url1='http://www.moviesubtitles.org/search.php?q='

	try:
		res1=requests.get(url1+movie_name)
	except Exception as exp:
		print("Some Network Error occured!")
		sys.exit(1)

	movie_soup1=bs4.BeautifulSoup(res1.text,'html.parser')

	matching_movie_list=movie_soup1.select('ul a')[6:]
	if len(matching_movie_list)> 0:
		matching_movie_link=[x.attrs['href'] for x in matching_movie_list ]
		pattern='\w*\s*'+movie_name+'\s*\w*' 
		exact_match_index=[i for i,movie in enumerate(matching_movie_list) if re.findall(pattern,movie.getText(),re.I)]
		if len(exact_match_index)>0:
			movie_name=matching_movie_list[exact_match_index[0]].getText()
			url2='http://www.moviesubtitles.org/'+matching_movie_link[exact_match_index[0]]
			res2=requests.get(url2)
			movie_soup2=bs4.BeautifulSoup(res2.text,'html.parser')
			subtitle_list=movie_soup2.select(".subtitle a")
			if len(subtitle_list)>0:
				subtitle_link_list=[x.attrs['href'] for x in subtitle_list]
				sub_id=subtitle_link_list[1].split("-")[1:]

				download_url='http://www.moviesubtitles.org/download-'+sub_id[0]
				print('Downloading subtitle...')
				download_subtitle(download_url,movie_name)
			else:
				print("Subtitle for movie is not found!")
				sys.exit(2)
		else:
			print("No exact match for movie!")
			sys.exit(3)
	else:
		print("Empty search result! ")
		sys.exit(4)


def main():	
	print("*" * 60)
	print('''Subtitle Grabber Copyright (C) 2016  Atul Kumar
This program comes with ABSOLUTELY NO WARRANTY;
This is free software, and you are welcome to redistribute it
under certain conditions\nfor details view license.''')
	print("*" * 60)
	movie_name=input("\nEnter the name of the movie: ")
	search(movie_name)

if __name__ == "__main__" :
	main()