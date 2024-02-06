from bp_single_file import *

searchFor = "SHS200/200/8.0"
revitElement = None
ls = ["balk_gen_K200x12.5","balk_gen_K200x10","balk_gen_K200x8"]

results = searchProfile(searchFor)
elementType = "balk_gen_"
for each in results.synonyms:
    tmp = elementType+each
    if tmp in ls:
        revitElement = tmp
print(revitElement)