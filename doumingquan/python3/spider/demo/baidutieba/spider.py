import re;
import urllib.request;

def get_content(url):
	html = urllib.request.urlopen(url);
	content = html.read();
	# urllib.close();
	return content;
def get_image(data):
	regex = r'class="BDE_Image" src="(.+?\.jpg)"'
	pat = re.compile(regex)
	html=data.decode('utf-8')#python3
	images_code = re.findall(pat,html)
	print(images_code);
	i=0
	for image_url in images_code:
		print(image_url) 
		urllib.request.urlretrieve(image_url,'%s.jpg'%i)
		i+=1
result = get_content('https://tieba.baidu.com/p/2772656630');
get_image(result);
# print(result);