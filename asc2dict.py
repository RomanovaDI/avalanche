print("Write a file of ASCII map or type enter and file name will be \"relief_22.asc\"")
map_name = input()
if map_name == "":
	map_name = "relief_22.asc"
print("Opening file: \"" + map_name + "\"")
file_map = open(map_name, "r")
print(file_map.readline())
file_map.close()
