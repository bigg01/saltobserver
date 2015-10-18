import getpass
from apitest import SaltApiManager



if __name__ == '__main__':
	username = str(raw_input('user: ')) or getpass.getuser()
	password = getpass.getpass()
	saltrun = SaltApiManager(user = username,
						  password = password,
						  SALT_API = 'http://10.0.0.4',
						  PORT = '8000'
						  )
	saltrun.listkeys()
	saltrun.run(tgt='*', fun= 'user.info', arg='guo')
	saltrun.run(tgt='*', fun= 'status.loadavg')
	saltrun.logout()
	print saltrun