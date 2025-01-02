# author name:-Rajveer Singh
# date:-2020-05-16
# usage:- python pdbtool.py pdbfilename
# description:- command line input:- pdb file name
# interative input:- commands
# possible command inputs are atomfreq, resfreq, reslength, help, quit
# the outputs of each command is explained below
# atomfreq: prints element name: occurrence frequency for every atom in the file
# resfreq: prints residue name: distinct occurrence frequency for every  residue in the file
# reslength :- Usage -reslength residue_name chain_id residue_seq_num
# reslength:- output length of the residue specified
# help:- outputs possible commands and correct usage
# quit:- exits the program

import sys


# number of arguments
n = len(sys.argv)

# checking if enough command line arguments
if n<2:
    sys.stderr.write("Error: Not enough command line arguments!\nCorrect Usage:- pdbtool.py pdbfilename\n")
    sys.exit()
file_path = sys.argv[1]

# error catching for opening the file
try:
    f = open(file_path, "r")
except FileNotFoundError:
    sys.stderr.write("Error: file path specified doesn't exist.\n")
    sys.exit()
except PermissionError:
    sys.stderr.write("Error: file path specified cannot be read(no read permissions).\n")
    sys.exit()
except Exception as err:
    sys.stderr.write("Error: unkown error while opening the file.\n")
    sys.exit()

# function to get atom frequencies
def atom_frequencies(atoms_records):
    # frequency dictionary
    freq={}
    for atom in atoms_records:
        try:
            freq[atom['element_name']] += 1
        except KeyError:
            freq[atom['element_name']] = 1
    return freq


# function to get residue frequencies
def residue_frequencies(atoms_records):

    # finding all residue sequence numbers an residue has
    all_occurences = {}
    for atom in atoms_records:
        try:
            all_occurences[atom['residue']].append(atom['sq_num'])
        except KeyError:
            all_occurences[atom['residue']] = [atom['sq_num']]

    # finding all count of distinct residue sequence numbers an residue has
    freq = {}
    for i in all_occurences.keys():
        freq[i] = len(set(all_occurences[i]))
    return freq


# function to calculate the length of a residue
def diameter(atom_records, residue_name, chain_id, residue_seq_num):
    # list storing locations of all atoms in a residue
    locations = []
    for atom in atom_records:
        if residue_name == atom['residue'] and chain_id == atom['chain_id']\
                and residue_seq_num == atom['sq_num']:
            locations.append([atom['x'], atom['y'], atom['z']])
    # if residue not found
    if len(locations) == 0:
        sys.stderr.write("Error! Residue not found! Try again\n")
        return None
    # finding points which are farthest apart in locations
    max_dis = 0
    for i in range(len(locations)):
        for j in range(i):
            dist = 0
            for k in range(3):
                dist += (locations[i][k]-locations[j][k])**2
            dist = (dist)**(.5)
            if max_dis < dist:
                max_dis = dist
    return max_dis


atom_records = []  # list to store atom_records

model_count = 0  # number of times MODEL line has come
line_count=0
for line in f:
    line_count+=1
    if line[0:5] == "MODEL":
        model_count += 1
        # if first model has been read
        if model_count > 1:
            break
    elif line[0:5] == "ATOM ":
        if line[16].isspace():

            # checking if line record is valid
            # checking if columns corresponding to residue name are correct
            if line[17:20].isspace():
                sys.stderr.write("Error:- Invalid Atom record found, name of residue at line "+str(line_count)+ " is invalid")
                sys.exit()
            
            # checking if columns corresponding to chain id is correct
            if not line[21].isalpha() or not line[21].isupper():
                sys.stderr.write("Error:- Invalid Atom record found, chain id at line "+str(line_count)+ " is invalid")
                sys.exit()
            
            # checking if columns corresponding to residue sequence number are correct
            try:
                int(line[22:26])
            except ValueError:
                sys.stderr.write("Error:- Invalid Atom record found, residue sequence number at line "+str(line_count)+ " is invalid")
                sys.exit()
                
            # checking if columns corresponding to x-coordinate are correct
            try:
                float(line[30:38])
            except ValueError:
                sys.stderr.write("Error:- Invalid Atom record found, x-coordinate at line "+str(line_count)+ " is invalid")
                sys.exit()
                
            # checking if columns corresponding to y coordinate are correct
            try:
                float(line[38:46])
            except ValueError:
                sys.stderr.write("Error:- Invalid Atom record found, y-coordinate at line "+str(line_count)+ " is invalid")
                sys.exit()
            
            # checking if columns corresponding to z-coordinate are correct
            try:
                float(line[46:54])
            except ValueError:
                sys.stderr.write("Error:- Invalid Atom record found, z-coordinate at line "+str(line_count)+ " is invalid")
                sys.exit()
                
            # checking if columns corresponding to element name are correct
            if not line[76:78].strip().isalpha():
                sys.stderr.write("Error:- Invalid Atom record found, element name at line "+str(line_count)+ " is invalid")
                sys.exit()
                
            # making an atom record
            temp_dict = {}
            temp_dict['residue'] = line[17:20].strip()
            temp_dict['chain_id'] = line[21]
            temp_dict['sq_num'] = int(line[22:26])
            temp_dict['x'] = float(line[30:38])
            temp_dict['y'] = float(line[38:46])
            temp_dict['z'] = float(line[46:54])
            temp_dict['element_name'] = line[76:78].strip()
            # adjusting capitalization in element name
            if len(temp_dict['element_name']) == 1:
                temp_dict['element_name'] = temp_dict['element_name'].upper()
            elif len(temp_dict['element_name']) == 2:
                temp_dict['element_name'] =\
                    temp_dict['element_name'][0].upper()\
                    + temp_dict['element_name'][1].lower()
            atom_records.append(temp_dict)
print(len(atom_records), "atoms recorded.")
f.close()

command = ''
while(command.lower() != 'quit'):
    print("command:",end=' ')
    # taking command input
    command = input()
    
    if len(command)==0:
        sys.stderr.write("Error: No command entered!, Enter again\n")
    # if command is atomfreq
    elif command.lower() == "atomfreq":
        atom_freq = atom_frequencies(atom_records)
        temp=atom_freq.keys()
        temp=sorted(temp)
        for i in temp:
            print(i,": ",atom_freq[i],sep='')
    # if command is resfreq
    elif command.lower()=="resfreq":
        res_locs=residue_frequencies(atom_records)
        temp=res_locs.keys()
        temp=sorted(temp)
        for i in temp:
            print(i,": ",res_locs[i],sep='')
    # if command is quit
    elif command.lower()=="quit":
        sys.exit()
    # if command is help
    elif command.lower()=='help':
        print('The possible commands of the pdbtool program are:-')
        print("\tatomfreq")
        print("\tresfreq")
        print("\treslength, Usage:-reslength residue_name chain_id residue_seq_num")
        print('\thelp')
        print("\tquit")
    # if command is reslength
    elif command.lower().split()[0]=="reslength":
        if len(command.lower().split())!=4:
            sys.stderr.write("Error: Incorrent usage!,Correct usage:-reslength residue_name chain_id residue_seq_num\n")
        else:
            temp=command.split()
            residue_name=temp[1]
            chain_id=temp[2]
            residue_seq_num=int(temp[3])
            max_dis=diameter(atom_records,residue_name,chain_id,residue_seq_num)
#            GLU with sequence number 3 in chain A has length 42.00 angstroms.
            if max_dis is not None:
                print(residue_name," with sequence number ", residue_seq_num,' in chain ',chain_id,' has length %.2f'%max_dis," angstroms.",sep='')
    else:
        sys.stderr.write("Error: Unidentified command! Try Again\n")
