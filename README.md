# Python-Interactive-PDB-Analysis-Tool

# README for PDB Tool Project

## Project Overview
The **PDB Tool Project** is a Python-based command-line utility designed for processing and analyzing Protein Data Bank (PDB) files. The tool offers users the ability to:
1. Retrieve the frequency of different atom types in a PDB file.
2. Calculate the frequency of residues.
3. Determine the maximum distance between atoms within a specific residue.
4. Interact with a simple user-friendly command prompt.

## Features
- **Atom Frequency Analysis**: Computes and lists the occurrences of each atom type in the PDB file.
- **Residue Frequency Analysis**: Displays the frequency of each residue in the file.
- **Residue Length Calculation**: Calculates the maximum distance between any two atoms within a specified residue.
- **Error Handling**: Robust checks to ensure the program doesn't crash due to invalid input files or commands.
- **Interactive Mode**: Users can interact with the program via a command-line interface.

## Usage Instructions
### Prerequisites
- Python 3.x installed on your system.
- A valid PDB file for analysis.

### Running the Program
To run the program, execute the following command:
```bash
python pdb_tool.py <PDB_FILE>
```
Replace `<PDB_FILE>` with the path to your PDB file.

### Interactive Commands
Once the program starts, use the following commands:
1. **`atomfreq`**: Displays the frequency of each atom type in the file.
   - Example:
     ```
     C: 3201
     N: 918
     O: 1101
     ```
2. **`resfreq`**: Displays the frequency of each residue.
   - Example:
     ```
     ALA: 32
     GLU: 91
     MET: 42
     ```
3. **`reslength <residue_name> <chain_id> <res_seq_num>`**: Calculates the maximum distance in angstroms between atoms in the specified residue.
   - Example:
     ```
     reslength GLU A 3
     GLU with sequence number 3 in chain A has length 42.00 angstroms.
     ```
4. **`quit`**: Exits the program.

### Error Messages
- **Missing File Argument**: Ensure you provide a file as an argument.
- **File Not Found**: Verify the path to the PDB file is correct.
- **Invalid Command**: Enter a valid command as listed above.

## Program Design
The program is structured for readability and maintainability:
- **Data Parsing**: Extracts relevant data from PDB files based on column specifications.
- **Data Storage**: Utilizes dictionaries and lists to manage atom and residue data.
- **Functions**:
  - `atom_frequencies`: Calculates and returns atom frequencies.
  - `residue_frequencies`: Calculates and returns residue frequencies.
  - `diameter`: Computes the maximum distance between atoms in a residue.

## Testing
- Test with small PDB files to validate output.
- Ensure the program handles invalid input gracefully.
- Verify all commands generate the expected results.

## Documentation
- For user assistance, type `help` in the interactive mode to see a list of available commands.
- Refer to the detailed in-line comments in the source code for more information on implementation details.
