import pip
import importlib
import os


class Installer:
	def __init__(self, filename="requirements.txt"):
		self.filename = filename
		self.modules = self.get_modules()

	def get_modules(self):
		raw_modules = self.fetch_modules(self.filename)
		return self.clean_modules(raw_modules)

	@staticmethod
	def fetch_modules(filename):
		with open("requirements.txt", "r") as f:
			modules = f.readlines()
			f.close()
		return modules

	@staticmethod
	def clean_modules(modules):
		return [module.replace("\n", "") for module in modules]

	def set_up(self):
		print("Setting up... Please wait...")
		for module in self.modules:
			status = self.check_if_installed(module)
			if status is not None:
				print("%s module is already successfully installed." % module)
			else:
				print("%s module is being installed..." % module)
				install_status = self.install_module(module)
				if install_status == 1:
					print("Some error caused in installing %s module. Kindly report back to the forum for further information on how to fix the problem." % module)
					break
				else:
					print("%s module was successfully installed." % module)
		print("\n")
		print("Everything is set up... And Stephanie is ready to run.")
		input("Close the command line by writting exit or simply close the window.")

	@staticmethod
	def check_if_installed(module_name):
		try:
			module_status = importlib.find_loader(module_name)
		except Exception:
			module_status = importlib.util.find_spec(module_name)
		return module_status

	@staticmethod
	def install_module(module_name):
		status = pip.main(['install', module_name])
		return status


if __name__ == '__main__':
	i = Installer()
	i.set_up()
