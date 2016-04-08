import random
import hashlib
global fileSize; #Size of obfuscated file
global rtPointer; #Pointer to relocation table
global stPointer; #Pointer to string table
global Checksum; #Note, the integrity of the checksum does not matter in this context, since its function is similar to a key that is not included in the file, nor is the original file included.
global full_file;
def format_pointer(pointer):
    if type(pointer) == int:
      new_pointer = str(hex(pointer))[2::].upper()
    elif type(pointer) == float:
      new_pointer = str(hex(int(pointer)))[2::].upper()
      #Later add support for IEEE Float representation
    else:
      new_pointer = str(hex(int("0x" + str(pointer), 16)))[2::].upper()
    return ("0" * (8 - len(new_pointer))) + new_pointer
def unformat_pointer(pointer):
    if type(pointer) != (str or hex):
        return int(pointer)
    else:
        return int("0x" + pointer, 16)
def get_garble():
    #outputs garble and pointers
    #print (full_file)
    gStart = random.randrange(1,rtPointer - 4, 8)
    gLength = random.randrange(1,30, 8)
    # ^^^  region of data
    """
    if gStart + gLength >= rtPointer:
        gLength = rtPointer - gStart
        if gLength <= 1:
            gLength = 2
    """
    try:
        input_data = full_file[gStart:gStart + gLength]
    except: #Virtual EOF Error
        #input_data = full_file[gStart:len(full_file) - 1]
        gLength = len(full_file) - 1 - gStart
    if gLength % 8 != 0:
        gStart -= gLength % 8
        gLength += gLength % 8
        input_data = full_file[gStart:gStart + gLength]
    if gStart > (len(full_file) - 8):
        gStart -= gStart - (len(full_file) - 8)
        gLength += gStart - (len(full_file) - 8)
        input_data = full_file[gStart:gStart + gLength]
    if gLength < 8:
        gStart -= 8 - gLength
        gLength += 8 - gLength
        input_data = full_file[gStart:gStart + gLength]
    new = ""
    garble_length = random.randrange(1,30) * 2
    hex_nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"] #list of hex nums
    for i in range(0,garble_length):
        garble = ""
        for i in range(0,8):
            garble = garble + hex_nums[random.randrange(0,16)]
        new = new + garble
    start_pointer = format_pointer(int(gStart / 2)); pointer_length = format_pointer(int(gLength / 2));
    real_data_pointer = format_pointer("0")
    return [new, start_pointer, pointer_length, input_data, gStart, gLength, real_data_pointer, garble_length]
"""
def add_garble(full_file,head):
    new_garble = get_garble()
    adjust_garble_pointers(new_garble[1], new_garble[3], new_garble[5])
    garble_list.append(new_garble)
    #print ("Len of full: " + str(len(full_file)))
    #print ("New_garble[4]: " + str(new_garble[4]))
    #print ("new_garble[0]" + str(new_garble[0]))
    rttable = len(full_file[0: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3])])
    full_file = full_file[0: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3])] + new_garble[1] + new_garble[2] + new_garble[3]
    header[0] = format_pointer(len(full_file) + 24)
    header[1] = format_pointer(rttable)
    print ("".join(header) + full_file)
    return (full_file, header)
"""
def get_pointless_garble():
    hex_nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"] #list of hex nums
    random_length = random.randrange(1,10) * 2
    pointless_garble = ""
    for i in range(0,random_length):
        current_garble = ""
        for n in range(0,8):
            current_garble = current_garble + hex_nums[random.randrange(0,16)]
        pointless_garble = pointless_garble + current_garble
    return (pointless_garble, len(pointless_garble))
def add_garble(full_file,head):
    new_garble = get_garble()
    #old: adjust_garble_pointers(new_garble[1], new_garble[3], new_garble[5])
    adjust_garble_pointers(new_garble[4], new_garble[3], new_garble[6], new_garble[5])
    garble_list.append(new_garble)
    n_head = head
    print (n_head)
    for i in range(0,len(n_head)):
        n_head[i] = format_pointer(n_head[i])
    extra_garble = get_pointless_garble()
    print ("old n_head: " + n_head[1])
    n_head[1] = format_pointer(int(float(unformat_pointer(n_head[1])) / 2) + extra_garble[1] + len(new_garble[0]))
    n_head[2] = format_pointer(((unformat_pointer(n_head[2])) + int(float(extra_garble[1]) / 2) + (int(float(len(new_garble[0])) / 2))))
    print ("len of n_head: " + str(len("".join(n_head))))
    print ("new_n_head: " + n_head[1])
    real_data_position = len(full_file[0: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[0]):rtPointer]) + len(new_garble[3])
    if (real_data_position - len(new_garble[3]) + 1) % 8 != 0:
        spacing = ("0" * ((real_data_position - len(new_garble[3]) + 1) % 8))
        if len(spacing) % 2 != 0:
            spacing = spacing + "0"
        if (real_data_position + len(spacing)) % 8 != 0:
            spacing = ("0" * ((real_data_position - len(new_garble[3]) + 1) % 8))
        if len(spacing) % 2 != 0:
            spacing = spacing + "0"
        n_head[1] = format_pointer(int(float(((unformat_pointer(n_head[1]) * 2)) + 8) / 2))
        n_head[2] = format_pointer(unformat_pointer(n_head[2]) + 4)
    else:
        spacing = ""
    fake_pointers = get_fake_pointers()
    #full_file = full_file[0: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3]):rtPointer] + new_garble[3] + extra_garble[0] + full_file[rtPointer::] + str(new_garble[1]) + str(new_garble[2]) + str(format_pointer(real_data_position))
    extra_full_file = full_file[rtPointer:] +  format_pointer(16 + len(full_file[:new_garble[4]]) + len(new_garble[0]) + len(full_file[new_garble[4] + new_garble[5]: rtPointer]) + len(spacing)) + str(format_pointer((unformat_pointer(real_data_position) / 2) + 12 + (len(spacing) / 2))) + str(format_pointer(unformat_pointer(new_garble[1]) / 2)) + str(format_pointer(unformat_pointer(new_garble[2]) / 2)) + str(format_pointer(len(new_garble[0]))) + str(fake_pointers)
    # str(format_pointer(unformat_pointer(real_data_position) + len(spacing)))
    #full_file = full_file[0: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3]):rtPointer] + new_garble[3] + extra_garble[0]  + full_file[rtPointer::] + str(format_pointer(real_data_position)) + str(new_garble[1]) + str(new_garble[2])
    print ("index[0]: " + new_garble[0])
    print ("index[3]: " + new_garble[3])
    if new_garble[3] == "" or (len(new_garble[3]) < 8):
        print ("gLength: " + str(new_garble[5]))
        print ("gStart: " + str(new_garble[4]))
    print ("extra_garble: " + str(extra_garble[0]))
    print ("extra_garble[1]: " + str(extra_garble[1]))
    if (real_data_position - len(new_garble[3]) + 1) % 8 != 0:
        full_file = full_file[: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3]):rtPointer] + spacing + new_garble[3] + extra_garble[0]
        extra_full_file = ("0" * (8 - len(spacing))) + extra_full_file
                           
    else:
        spacing = ""
        full_file = full_file[: new_garble[4]] + new_garble[0] + full_file[new_garble[4] + len(new_garble[3]):rtPointer] + new_garble[3] + extra_garble[0]
    #need to readjust pointers and stuff for spacing
    print ("Full_file: " + full_file)
    print ("Header: " + "".join(n_head))
    print ("rtTable: " + extra_full_file)
    print ("len index[0]: " + str(len(new_garble[0])))
    input("Press enter to get the encoded file. ")
    print ("".join(n_head) + full_file + extra_full_file)
    return (n_head, full_file)
def get_fake_pointers():
    checksum_range = (current_iteration - (current_iteration % len(Checksum)), (current_iteration - (current_iteration % len(Checksum))) + 4)
    pointer_amount = int("0b" + str(Checksum)[checksum_range[0]:checksum_range[1]],2)
    random_pointers = []
    for i in range(0,pointer_amount):
        random_pointers.append(format_pointer(random.randrange(0,int(len(full_file[:rtPointer]) / 2),2)))
    return "".join(random_pointers)
                            
#fake pointers code
# format_pointer(random.randrange(0,len(full_file[:rtPointer]),4))
def adjust_garble_pointers(start_offset, size_dif, real_offset, size_dif2=0): #relocates garble pointer when a difference in filesize occurs
    #start_offset is offset of new garble or change
    #size_dif is garble change size/change or main change offset, always required
    #size_dif2 is real data size/change. Argument should be a repeat size_dif if not included
    if size_dif2 == 0:
        size_dif2 = size_dif
    for garble_item in range(0,len(garble_list)):
        #old if garble_list[garble_item][4] >= start_offset:
        if garble_list[garble_item][4] >= start_offset:
            garble_list[garble_item][1] = format_pointer(unformat_pointer(garble_list[garble_item][4]) + (size_dif2 - size_dif))
            garble_list[garble_item][4] = garble_list[garble_item][4] + (size_dif2 - size_dif)
            #need to add in adjusting real data pointersa
        if garble_list[garble_item][6] >= real_offset:
            if (garble_list[garble_item][6] != "00000000") and (real_offset != "00000000"):
                garble_list[garble_item][6] = format_pointer(unformat_pointer(garble_list[garble_item][6]) + size_dif)
            
my_file = input("Enter file name: ") 
hasher = hashlib.md5()
full_file = []
#gets the checksum of the file
with open(my_file, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
md5 = hasher.hexdigest()
bytes_read = open(my_file, "rb").read()
for b in bytes_read: #reads the bytes of the file and places them in a list
    #full_file.append(hex(int(str(b)[0])))
    #full_file.append(hex(int(str(b)[1])))
    full_file.append(hex(b))
    #print(hex(b))
    #print(full_file)
#print (read_binary(my_file))
#print (md5)
a = full_file
full_file = ""
for i in a:
    full_file = str(full_file) + str(i)[2::]
Checksum = (str(bin(int("0x" + md5, 16))))[2:] #binary md5
fileSize = len(full_file * 2)
rtPointer = fileSize

print(Checksum)
afile.close()
input("Press enter to continue... ")
header = [fileSize, rtPointer, int(float(rtPointer) / 4) + 16, "00000000"]
global garble_list;
global is_new;
is_new = True
garble_list = []
current_iteration = 0
print (get_fake_pointers())
input ("Press enter. ")
ffh = add_garble(full_file, header)
full_file = ffh[0]
header = ffh[1]
