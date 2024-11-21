import xml.etree.ElementTree as ET
import os
import shutil

def process_xml_file(input_file, output_file, tag_to_remove, contentDiscriminator, surroundingtag):
    """Process an XML file to remove the last matching TextObject and save to output file."""
    # Load the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Find the PageFooterBand element
    page_footer = root.find(".//{surroundingtag}")
    
    if page_footer is not None:
        # Collect all TextObjects in PageFooterBand that have Text="................."
        text_objects = [
            obj for obj in page_footer.findall("{tag_to_remove}") 
            if obj.get("{contentDiscriminator}") == "................."
        ]
        
        # If there are any matching TextObjects, remove the last one
        if text_objects:
            page_footer.remove(text_objects[-1])
    
    # Save the modified XML to the output path
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def process_all_files(input_dir, output_dir, tag_to_remove, contentDiscriminator, surroundingtag):
    """Process all XML files in the input directory and its subdirectories."""
    # Walk through all files in the input directory
    for root_dir, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".frx"):  # Only process XML files
                # Full path of the input file
                input_file_path = os.path.join(root_dir, file)
                
                # Create the corresponding output directory structure
                relative_path = os.path.relpath(root_dir, input_dir)
                output_file_dir = os.path.join(output_dir, relative_path)
                os.makedirs(output_file_dir, exist_ok=True)
                
                # Full path for the output file
                output_file_path = os.path.join(output_file_dir, file)
                
                # Process and save the XML file
                process_xml_file(input_file_path, output_file_path, tag_to_remove, contentDiscriminator, surroundingtag)
                print(f"Processed and saved: {output_file_path}")

# Specify input and output directories
input_directory = "input"
output_directory = "output"

# Clear the output directory if it already exists

print('Make sure that the .frx files are placed inside input/dirname/file.frx')
print('This will remove stuff from the .frx file')


#-----------------------------------------------------------
tagtoremove = "TextObject"
contentDiscriminator = "................."
surroundingtag = "PageFooterBand"
#-----------------------------------------------------------


# Process all files
process_all_files(input_directory, output_directory, tagtoremove, contentDiscriminator, surroundingtag)
