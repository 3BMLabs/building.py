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
		
	excluded_directories = ["exchange", "specklepy", "sandbox"]
 
	header_file = "docs/single_file_header.py"

	file_dict: dict = dict()
	#files indiced by name. each file has a text node and a list of deps, relative paths to the other files.
 
	global_deps:list[str] = []
	#a list of import statements.
 
 
	def sort_file_list(file_list:list[str]):
		file_list.sort(key=lambda path:re.split('[\\\\/]', path)[-1])
		
	for subdir, dirs, files in os.walk("."):
		folder_included = True
		for excluded_dir in excluded_directories:
			if excluded_dir in subdir:
				folder_included = False
				break

		if (not folder_included) and include_files == None:
			continue

		for module_path in files:
			#no file included
			if module_path.endswith('.py'):
				longer_path = os.path.join(subdir, module_path)
				if folder_included or longer_path in include_files:
					deps = []
					with open(longer_path) as f:
						#TODO: fix error can't decode bytes in position
						lines = f.readlines()
						file_str = ""
						if len(lines) > 0 and lines[0] == Includedstr:
							copy_flag = True
							#loop over lines, skip the first line
							for line_index in range(1, len(lines)):
								line = lines[line_index].rstrip('\n')

								#check for import statements to determine order. let's also allow imports in included parts but just strip them away, for convenience.
								#possible patterns: 'from a import b' or 'import c'

								module_name = ''
								#'file' in 'from path.to import file'
								module_extra_name = None
								#we only need the first part
								if line.startswith(import_start):
									module_name = line[len(import_start):]
								elif line.startswith(from_start):
									sep_index = line.find(import_mid)

									#this might cause an error. in that case there have a malformed import statement!
									module_name = line[len(from_start):sep_index]
         
									module_extra_name = line[sep_index + len(import_mid):]
								if module_name != '':
									if line not in global_deps:
										module_path = '.'
										for part in module_name.split('.'):
											module_path = path.join(module_path, part)
	
										#examples:
										#from path.to.file import class
										#from path.to import file
										#import file
										test_paths = [module_path + '.py']
										if module_extra_name != None:
											test_paths.append(path.join(module_path, module_extra_name) + '.py')
										for test_path in test_paths:
											if os.path.isfile(test_path):
												deps.append(test_path)
												break
										else: #no valid path in test paths, so it must be a global import
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
									file_str += line + '\n'
								else:
									if no_copy_end in line:
										copy_flag = True
          
							sort_file_list(deps)
							file_dict[longer_path] = {}
							file_dict[longer_path]["text"] = file_str
							file_dict[longer_path]["deps"] = deps
 
	with open(header_file, 'r') as content_file:
		merged_str = content_file.read() + '\n\n'
		#the merged string which will be written to output_filename
  
	#sort everything to ensure consistency across different platforms
	global_deps.sort()
 

	sorted_file_keys = list(file_dict.keys())
	sort_file_list(file_list = sorted_file_keys)

	for global_dep in global_deps:
		merged_str += global_dep + '\n'
	
  
	#recursively add files to merged_str
	def add_file (relative_path: str):
		if relative_path in sorted_file_keys:
			if "added" not in file_dict[relative_path]:
				file_dict[relative_path]["added"] = True
				for dep in file_dict[relative_path]["deps"]:
					add_file(dep)
				nonlocal merged_str
				merged_str += file_dict[relative_path]["text"] + '\n'

	#now order files based on dependencies
	for longer_path in sorted_file_keys:
		add_file(longer_path)
    
    #finally, write the merged, correctly ordered file to the destination file
	with open(output_filename, 'w+') as dest_file:
		dest_file.write(merged_str)

generate_single_file('BuildingPy.py')

generate_single_file('BuildingPy-struct4u.py', include_files=['exchange/struct4U.py'])

generate_single_file('BuildingPy-gis2bim.py', include_files=['exchange/GIS2BIM.py', "packages/GIS2BIM/GIS2BIM.py", "packages/GIS2BIM/GIS2BIM_NL.py", 	"packages/GIS2BIM/GIS2BIM_NL_helpers.py", "packages/GIS2BIM/GIS2BIM_CityJSON.py", "packages/GIS2BIM/GIS2BIM_CRS.py"])

generate_single_file('BuildingPy-revit.py', include_files=['exchange/revit.py'])