def move_userdata_to_respective_folders():
	os.chdir('./Data/')
	for x in os.listdir():
		if os.path.isfile(x):
			user=x.split('@')[0]
			mx.touch(f"{user}/")
			os.rename(x,f"{user}/{x}")