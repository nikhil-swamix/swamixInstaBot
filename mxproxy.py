import sys;success=0;importlevel="./";
for i in range(4): 
	if not success:
		try: sys.path.append(importlevel);from modulex import modulex as mx; success=1 ;mx.cleanup()
		except Exception as e: importlevel=importlevel + "../";
		
if __name__ == '__main__':
	mx