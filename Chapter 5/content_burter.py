import urllib2
import threading
import Queue
import urllib

threads=50
target_url="http://testphp.vulnweb.com"
wordlist_file="/tmp/all.txt" #from SVNDigger
resume=None
user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):

	#读入字典文件
	fd=open(wordlist_file,"rb")
	raw_words=fd.readlines()
	fd.close()

	found_resume=False
	words=Queue.Queue()

	for(word in raw_words):
		word=word.rstrip()

		if(resume isn not None):
			words.put(word)
		else:
			if word==resume:
				found_resume=True
				print("Resuming wordlist from: %s" % resume)


		else:
			words.put(word)

	return words

def dir_bruter(word_queue,extensions=None):
	while(not word_queue.empty()):
		attempt=word_queue.get()
		attempt_list=[]

		#检查是否有文件扩展名，如果没有
		#就是我们要暴力破解的路径
		if("." not in attempt):
			attempt_list.append("/%s/",attempt)
		else:
			attempt_list.append("/%s",attempt)

		#如果我们想要暴力扩展
		if(extensions):
			for(extension in extensions):
				attempt_list.append("/%s%s" % (attempt,extension))

		#迭代我们要尝试的文件列表
		for brute in attempt_list:
			url="%s%s" % (target_url,urllib.quote(brute))

			try:
				headers={}
				headers["User-Agent"]=user_agent
				r=urllib2.Request(url,headers=headers)

				response=urllib2.urlopen(r)

				if(len(response.read())):
					print("[%d] => %s" % (response.code,url))

			except urllib2.URLError as e:
				if(hasattr(e,'code') and e.code !=404):
					print("!!! %d => %s" % (e.code,url))
				pass


word_queue=build_wordlist(wordlist_file)
extensions=[".php",".bak",".orig",".inc"]

for i in range(threads):
	=threading.Thread(target=dir_bruter,args=(word_queue,extensions))
	t.start()
	