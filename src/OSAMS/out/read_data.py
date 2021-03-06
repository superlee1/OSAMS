import shutil
import os

def read_data(t_file,tag):
	'''
	read_data
	reads data denoted by @DATA@{TAG}=number
	args:
		t_file:	file
		tag: tag
	'''
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	value = 0.0
	for sline in old:
		line = sline.strip()
		words = line.split('=')
		if words[0]==(f"@DATA@{tag}"):
			value = float(words[1])
		else:
			new.write(sline)
			pass
	old.close()
	new.close()
	os.remove(t_file+'~')
	return value
