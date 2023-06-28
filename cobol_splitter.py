import os

def split_cobol_code(code_file, output_directory):
    with open(code_file, 'r') as file:
        lines = file.readlines()

    # Identify logical breakpoints (Divisions) and their corresponding labels
    breakpoints = []
    for i, line in enumerate(lines):
        if line.startswith('IDENTIFICATION DIVISION') or \
           line.startswith('ENVIRONMENT DIVISION') or \
           line.startswith('DATA DIVISION') or \
           line.startswith('PROCEDURE DIVISION'):
            breakpoint_label = line.strip()
            breakpoints.append((breakpoint_label, i))

    # Split the code into separate files based on breakpoints
    for i in range(len(breakpoints)):
        breakpoint_label, start_line = breakpoints[i]
        end_line = breakpoints[i+1][1] if i < len(breakpoints)-1 else len(lines)
        code_segment = lines[start_line:end_line]

        # Create a separate file for each code segment
        segment_file = os.path.join(output_directory, f'code_segment_{i+1}.cob')
        with open(segment_file, 'w') as segment:
            segment.write('\n'.join(code_segment))

        # Include relevant context as comments in each segment file
        with open(segment_file, 'a') as segment:
            segment.write(f'\n\n* Context: {breakpoint_label}\n')

    print(f'COBOL code split into {len(breakpoints)} segments.')

def process_directory(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each COBOL code file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.cob'):
            cobol_code_file = os.path.join(input_directory, filename)
            split_cobol_code(cobol_code_file, output_directory)

# Usage example
input_directory = 'input_cobol_files'  # Replace with the directory containing your COBOL code files
output_directory = 'code_segments'  # Replace with the desired output directory

process_directory(input_directory, output_directory)
