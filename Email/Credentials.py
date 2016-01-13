class Credentials:

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@staticmethod
	def readFromFile(filename):
		f = open(filename, 'r')
		un = f.readline().split()[1]
		pw = f.readline().split()[1]
		return Credentials(un, pw)