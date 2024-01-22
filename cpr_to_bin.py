import os
import sys

# convert Amstrad ROM files from .cpr format to .bin format

n = len(sys.argv)

input_file = ""
output_file = ""

if (n == 1): # just the command? output usage
	print ("Usage: cpr_to_bin <input_filename>.cpr [<output_filename>.bin]")
	exit()
	
if (n == 2): # command plus one arg, generate the output name
	input_file = sys.argv[1]
	if os.path.exists(input_file) == False:
		print ("Input file does not exist!")
		exit()

	if input_file.lower().endswith(".cpr") == False:
		print ("Not a .cpr file!")
		exit()
		
	stub_length = len(input_file) - 4
	output_file = input_file[:stub_length] + ".bin"
	#print("output file: " + output_file)

if (n == 3): # command plus both args
	input_file = sys.argv[1]
	output_file = sys.argv[2]

if (output_file.lower().endswith(".bin") == False):
	output_file += ".bin"
	
if os.path.exists(output_file):
	print ("Output file already exists!")
	exit()

		
cprfile = open(input_file, "rb")
riff_header = cprfile.read(4)
riff_header = riff_header.decode()
#print(riff_header)

if riff_header != "RIFF":
	print("Not an RIFF chunk file - missing 'RIFF' tag!")
	cprfile.close()
	exit()

file_length_binary = cprfile.read(4) # file length in little endian format, minus the RIFF header but including the AMS! type

file_length = int(file_length_binary[3] << 24)
file_length |= int(file_length_binary[2] << 16)
file_length |= int(file_length_binary[1] << 8)
file_length |= int(file_length_binary[0])

ams_type = (cprfile.read(4)) # AMS! type
ams_type = ams_type.decode()
#print (ams_type)

if ams_type != "AMS!":
	print("Not an Amstrad ROM chunk file - missing 'AMS!' tag!")
	cprfile.close()
	exit()

# use file_length_chunks_and_headers_only to loop over all chunks, and dump them without the header info

file_length_chunks_and_headers_only = file_length - 4
#print (file_length_chunks_and_headers_only)

file_length_remaining = file_length_chunks_and_headers_only

bin_output_file = open(output_file, "xb")

# chunks

while (file_length_remaining > 0):
	block_id = cprfile.read(4) # cbNN - block NN from 00, 01, ...
	#print (block_id)

	chunk_length_binary = cprfile.read(4)

	file_length_remaining = file_length_remaining - 4 - 4

	chunk_length = int(chunk_length_binary[3] << 24)
	chunk_length |= int(chunk_length_binary[2] << 16)
	chunk_length |= int(chunk_length_binary[1] << 8)
	chunk_length |= int(chunk_length_binary[0])

	chunk = cprfile.read(chunk_length) # chunk data

	# write chunk data to .bin file
	bin_output_file.write(chunk)

	file_length_remaining = file_length_remaining - chunk_length

bin_output_file.close()
cprfile.close()

print("Completed Successfully!")
