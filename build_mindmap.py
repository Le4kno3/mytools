#!/usr/bin/python3

import re

def main():

	# There is a limit on number of functions here, it should be less than 100.
	LIMIT = 100
	with open('ERC721.sol') as file:
		fn_name = [None] * LIMIT
		fn_modifier = [None] * LIMIT
		fn_visibility = [None] * LIMIT
		fn_mutability = [None] * LIMIT
		fn_arguments = [None] * LIMIT
		fn_returns = [None] * LIMIT	#bool
		fn_return_type = [None] * LIMIT
		fn_outlier = [None] * LIMIT
		fn_outlier_name = [None] * LIMIT
		fn_outlier_arguments = [None] * LIMIT
		
		data = file.read()
		# print(data)

		pattern=r"function [\S\s]*?{"

		matches = re.finditer(pattern, data, re.MULTILINE)

		counter = 0
		for matchNum, match in enumerate(matches, start=1):
			tmp = str(match.group())

			#checks if function returns or not and then set respective values.
			if ("returns" in tmp):
				fn_returns[counter] = True
			else:
				fn_returns[counter] = False

			#only detected: "override(", "override ("
			if (("override (" in tmp) or ("override(" in tmp) ):
				fn_outlier[counter] = True
				fn_outlier_name[counter] = "override"
			else:
				fn_outlier[counter] = False


			tmp = tmp.replace("(", ")")
			tmp = tmp.replace("returns (", ")")
			tmp = tmp.replace("returns(", ")")
			fn_array = tmp.split(")")
			if(len(fn_array) < 3):
				print("Detected an Errorneous Pattern, Possible Outlier: "+str(fn_array))
				print("---------------\n")
				counter += 1
				continue

			#remove newlines in fn_arguments
			if ("\n" in fn_array[1]):
				fn_array[1] = fn_array[1].replace("\n", "")
				fn_array[1] = fn_array[1].replace("        ", " ")

			if (fn_returns[counter] == False and fn_outlier[counter] == False):
				fn_name[counter] = fn_array[0][9:]
				fn_arguments[counter] = fn_array[1]
				fn_modifier[counter] = fn_array[2][:-2]
			elif (fn_returns[counter] == True and fn_outlier[counter] == False):
				fn_name[counter] = fn_array[0][9:]
				fn_arguments[counter] = fn_array[1]
				fn_modifier[counter] = fn_array[2][:-8]
				fn_return_type[counter] = fn_array[3]
			elif (fn_returns[counter] == True and fn_outlier[counter] == True):
				fn_name[counter] = fn_array[0][9:]
				fn_arguments[counter] = fn_array[1]
				fn_modifier[counter] = fn_array[2][:-8]
				fn_outlier_arguments[counter] = fn_array[3]
				fn_return_type[counter] = fn_array[5]
			elif (fn_returns[counter] == False and fn_outlier[counter] == True):
				fn_name[counter] = fn_array[0][9:]
				fn_arguments[counter] = fn_array[1]
				fn_modifier[counter] = fn_array[2][:-2]
				fn_outlier_arguments[counter] = fn_array[3]
			else:
				fn_name[counter] = fn_array
				print("Detected an Errorneous Pattern, Possible Outlier: "+fn_array)
				print("---------------\n")

			counter += 1
		
		#comment this for loop to see only outliers, "begining of the output".
		for i in range(0, counter):
			if(fn_name[i]):
				if( not fn_returns[i] and not fn_outlier[i]):
					print("Function Name: "+fn_name[i])
					print("Function Arguments: "+fn_arguments[i])
					print("Function Modifier: "+fn_modifier[i])
					print("---------------\n")
				if(fn_returns[i] and not fn_outlier[i]):
					print("Function Name: "+fn_name[i])
					print("Function Arguments: "+fn_arguments[i])
					print("Function Modifier: "+fn_modifier[i])
					print("Function Returns: "+str(fn_returns[i]))
					print("Function Return Type: "+fn_return_type[i])
					print("---------------\n")
				if(fn_returns[i] and fn_outlier[i]):
					print("Function Name: "+fn_name[i])
					print("Function Arguments: "+fn_arguments[i])
					print("Function Modifier: "+fn_modifier[i])
					print("Function Returns : "+str(fn_returns[i]))
					print("Function Return Type: "+fn_return_type[i])
					print("Function Outlier Name : "+fn_outlier_name[i])
					print("Function Outlier Arguments: "+fn_outlier_arguments[i])
					print("---------------\n")
				if(not fn_returns[i] and fn_outlier[i]):
					print("Function Name: "+fn_name[i])
					print("Function Arguments: "+fn_arguments[i])
					print("Function Modifier: "+fn_modifier[i])
					print("Function Outlier Name : "+fn_outlier_name[i])
					print("Function Outlier Arguments: "+fn_outlier_arguments[i])
					print("---------------\n")

#not needed if this is a standalone python script
if __name__ == "__main__":
	main()

