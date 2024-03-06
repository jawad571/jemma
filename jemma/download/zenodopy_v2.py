import zenodopy as zp
import re
import requests 
import os

def validate_url(url):
    """validates if URL is formatted correctly

    Returns:
        bool: True is URL is acceptable False if not acceptable
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

class Client(zp.Client):
	
	def download_file(self, filename=None, dst_path=None):
		"""download a file from project

		Args:
			filename (str): name of the file to download
			dst_path (str): destination path to download the data (default is current directory)
		"""
		if filename is None:
			print(" ** filename not supplied ** ")

		bucket_link = self.bucket

		if bucket_link is not None:
			if validate_url(bucket_link):
				url = f"{bucket_link}/{filename}"
				print(url)
				print(self._bearer_auth)
				r = requests.get(f"{bucket_link}/{filename}",
									auth=self._bearer_auth)

				# if dst_path is not set, set download to current directory
				# else download to set dst_path
				if dst_path:
					if os.path.isdir(dst_path):
						filename = dst_path + '/' + filename 
					else:
						raise FileNotFoundError(f'{dst_path} does not exist')
				print(r.header)
						
				if r.ok:
					with open(filename, 'wb') as f:
						f.write(r.content)                    
				else:
					print(f" ** Something went wrong, check that {filename} is in your poject  ** ")
					
			else:
				print(f' ** {bucket_link}/{filename} is not a valid URL ** ')
