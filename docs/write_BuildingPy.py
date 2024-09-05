import os
import glob, sys
from glob import glob
import re
from os import path

def find_ext(dr, ext):
	return glob(path.join(dr,"*.{}".format(ext)))

def generate_single_file(output_filename, include_files=None):
    #constants
	Includedstr = "# [included in BP singlefile]\n"


	no_copy_start = '# [!not included in BP singlefile - start]'
	no_copy_end = '# [!not included in BP singlefile - end]'
	from_start = 'from '
	import_start = 'import '
	import_mid = ' import '
		
	excluded_directories = ["exchange", "specklepy"]
 
	header_file = "docs/single_file_header.py"

	file_dict: dict = dict()
	#files indiced by name. each file has a text node and a list of deps, relative paths to the other files.
 
	global_deps:list[str] = []
	#a list of import statements.
		
	for subdir, dirs, files in os.walk("."):
		folder_included = True
		for excluded_dir in excluded_directories:
			if excluded_dir in subdir:
				folder_included = False
				break

		if (not folder_included) and include_files == None:
			continue

		for file_name in files:
			#no file included
			if file_name.endswith('.py'):
				longer_path = os.path.join(subdir, file_name)
				if folder_included or longer_path in include_files:
					deps = []
					with open(longer_path) as f:
						#TODO: fix error can't decode bytes in position
						lines = f.readlines()
						file_str = ""
						if len(lines) > 0 and  lines[0] == Includedstr:
							copy_flag = True
							#loop over lines, skip the first line
							for line_index in range(1, len(lines)):
								line = lines[line_index]
								#check for import statements to determine order. let's also allow imports in included parts but just strip them away, for convenience.
								#possible patterns: 'from a import b' or 'import c'

								module_name = ''
								#we only need the first part
								if line.startswith(import_start):
									module_name = line[len(import_start):]
								elif line.startswith(from_start):
									sep_index = line.find(import_mid)

									#this might cause an error. in that case there have a malformed import statement!
									module_name = line[len(from_start):sep_index]
         
								if module_name != '':
									file_name = '.'
									for part in module_name.split('.'):
										file_name = path.join(file_name, part)
									file_name += '.py'
									if os.path.isfile(file_name):
										deps.append(file_name)
									else:
										if line not in global_deps:
											#we may have multiple different import statements like 'from x import a' and 'from x import *', but that's okay
											global_deps.append(line)
									#strip away
									continue
								if copy_flag:
									if no_copy_start in line: 
										copy_flag = False
										continue
									if longer_path == "parser.py":
										line = line.replace("path.", "")
									file_str += line
								else:
									if no_copy_end in line:
										copy_flag = True
							file_dict[longer_path] = {}
							file_dict[longer_path]["text"] = file_str
							file_dict[longer_path]["deps"] = deps
	hierarchy = enumerate(file_dict)
 
	with open(header_file, 'r') as content_file:
		merged_str = content_file.read() + '\n\n'
		#the merged string which will be written to output_filename
  
	for global_dep in global_deps:
		merged_str += global_dep

	def add_file (relative_path: str):
		if relative_path in file_dict:
			if "added" not in file_dict[relative_path]:
				file_dict[relative_path]["added"] = True
				for dep in file_dict[relative_path]["deps"]:
					add_file(dep)
				nonlocal merged_str
				merged_str += file_dict[relative_path]["text"]

	#now order files based on dependencies
	for longer_path in file_dict:
		add_file(longer_path)
    

	with open(output_filename, 'w+') as dest_file:
		dest_file.write(merged_str)


generate_single_file('BuildingPy.py')

generate_single_file('BuildingPy-struct4u.py', include_files=['exchange/struct4U.py'])

generate_single_file('BuildingPy-gis2bim.py', include_files=['exchange/GIS2BIM.py', "packages/GIS2BIM/GIS2BIM.py", "packages/GIS2BIM/GIS2BIM_NL.py", 	"packages/GIS2BIM/GIS2BIM_NL_helpers.py", "packages/GIS2BIM/GIS2BIM_CityJSON.py", "packages/GIS2BIM/GIS2BIM_CRS.py"])

generate_single_file('BuildingPy-revit.py', include_files=['exchange/revit.py'])