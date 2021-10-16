try:
    import os
    import sys
    import ntpath
    import pathlib
    import anitopy
    import functools
    from subprocess import DEVNULL, Popen
    import json
    import subprocess
    from time import sleep
    from halo import Halo
    from pprint import pprint
except Exception as e:
    from traceback import format_exception
    exc_str = format_exception(etype=type(e), value=e, tb=e.__traceback__)
    print("{} Some modules are missing {}.\n Traceback: \n {} \n".format(__file__, e, exc_str))   

#TODO create an option for single threaded mode - IE limit number of processes to 1
#TODO give better error message when input files don't match IE given 11 files in one input directory and only 10 files in another input directory
#TODO when anitopy fails - use the len of the list to match files for muxing - get user confirmation
#TODO when given an options file - save the name of the track and look for that name in the other files being muxed - use mkvextract similar to pwrsub

def update_options_file(options_file_path, new_options_file_path, output_file_path, input_files_to_mux):
    options_file_contents = None
    with open(options_file_path, 'r') as options_file_reader:
        options_file_contents = options_file_reader.readlines()

    # the title is metadata in the file such as "Cool Show S01E01" this often gets displayed in video players
    file_title = None
    output_file_name = ntpath.basename(output_file_path)
    for input_file_path in input_files_to_mux:
        if output_file_name in input_file_path:
            mkvextract_json = json.loads(subprocess.check_output(['mkvmerge', '-J', input_file_path]).decode())

            try: 
                file_title = mkvextract_json['container']['properties']['title']
            except KeyError as e:
                print("Could not get a title from the file:", ntpath.basename(input_file_path),"\nThis means the mkv meta data didn't have a title.")
                file_title = ntpath.basename(input_file_path)

    if options_file_contents != None:
        matches_found = 0
        for index, line in enumerate(options_file_contents):
            if line == '  "(",\n':
                options_file_contents[index + 1] = '  "{}",\n'.format(input_files_to_mux[matches_found])
                matches_found += 1
            elif line == '  "--output",\n':
                options_file_contents[index + 1] = '  "{}",\n'.format(output_file_path)  
            elif line == '  "--title",\n' and file_title != None:
                options_file_contents[index + 1] = '  "{}",\n'.format(file_title)
        if matches_found != 0:   
            new_options_file_dir = os.path.dirname(new_options_file_path)
            if not os.path.isdir(new_options_file_dir):
                os.makedirs(new_options_file_dir)     
            with open(new_options_file_path, 'w') as options_file_writer:
                options_file_writer.writelines(options_file_contents)   
            return options_file_contents
    return None                

#called only ONCE to get the directories that contain both input files, and the output directory
#this is called before we start editing the options file for further files
def get_paths_from_options_file(options_file_path):
    options_file_contents = None
    with open(options_file_path, 'r') as options_file_reader:
        options_file_contents = options_file_reader.readlines()
    if options_file_contents != None:
        input_files = []
        output_dir = None
        for index, line in enumerate(options_file_contents):

            #the first and last quotation mark contain the string we want, remove everything else
            if line == '  "(",\n':
                file_name = options_file_contents[index + 1][3:]
                file_name = file_name[:(len(file_name) - 3)] 
                input_files.append(file_name)

            elif line == '  "--output",\n':
                output_dir = options_file_contents[index + 1][3:]
                output_dir = output_dir[:(len(output_dir) - 3)]                
                output_dir = os.path.dirname(output_dir)
              
        return input_files, output_dir
    return None            

#returns all files in given directories that have the same extension as the input file
def get_files_to_mux(input_files_from_options_file):
    #files may not be in same directory
    files_to_mux = {}   
    input_files_found = {} 

    for input_file_path in input_files_from_options_file:
        #the extension of the input file
        input_file_extension = pathlib.Path(input_file_path).suffix
        files_added = 1
        input_files_found[input_file_path] = 0
        for entry in os.scandir(r'{0}'.format(os.path.dirname(input_file_path))):
            input_files_found[input_file_path] += 1
            #used when anitopy can't get episode number from file            
            if not entry.is_dir():
                #they should be the same extension as the original input_file_path in input_files_from_options_file
                if pathlib.Path(entry.path).suffix == input_file_extension:
                    parsed_file = anitopy.parse(entry.name)
                    
                    #find out where to insert the file
                    insertion_index = files_added                   
                    if 'episode_number' in parsed_file:
                        insertion_index = parsed_file['episode_number']
                        #TODO test anitopy names that return a list for episode number 
                        #ask user to manually input episode number? input can be for every episode or it can be for a rule to select the first, second, ... n element in the episdoe number list                                               
                        if isinstance(insertion_index, list):
                            print("Anitopy detected this file's episode number as a list. This may affect the accuracy of the mux.")
                            insertion_index = insertion_index[0]

                    if insertion_index in files_to_mux:
                        files_to_mux[insertion_index].append(entry.path)    
                    else:
                        files_to_mux[insertion_index] = [entry.path]   

                    files_added += 1     

    file_count = None
    for input_file_path, input_file_count in input_files_found.items():
        if file_count:
            if input_file_count != file_count:
                print(f"The directory {os.path.dirname(input_file_path)} has more files than your other input directories.")
                print("Files found in your input directories:")
                pprint(input_files_found)

    #confirm that each mux_file_group is the same length. If not then one input directory has more files than the other                
    for mux_file_group in files_to_mux.values():
        if len(mux_file_group) != len(input_files_from_options_file):
            print("Files could not be mapped properly!")  
            print("This is how episodes were mapped. Episode numbers are mapped to file names.") 
            pprint(files_to_mux) 
            return None         
    
    return files_to_mux  

def get_user_name_scheme_choice(name_choices): 
    #if there is only one .mkv given in the inputs, then automatically choose that as the name scheme choice since you can only mux to .mkv files
    mkv_file_count = 0
    mkv_file_index = None
    for index, choice in enumerate(name_choices):
        if '.mkv' in choice:
            mkv_file_count += 1
            mkv_file_index = index

    if mkv_file_count == 1:
        return mkv_file_index

    if len(name_choices) != 1:    
        while True:
            print("\nEnter the number assosciated with your Name Scheme Choice | Name schemes refect your input file names")
            for index, name_choice in enumerate(name_choices):
                print("\t{}: {}".format(index + 1, ntpath.basename(name_choice)))
            print("\nYOUR CHOICE WILL BE USED FOR EVERY FILE BEING MUXED.\n")
            try:
                user_response = int(input("Your response: "))
                if user_response < 1 or user_response > len(name_choices):
                    continue
            except Exception:
                continue    
            return user_response - 1  

    print("\nDETECTED ONLY ONE INPUT FILE PER MUX\n\tDefault Name Scheme: {}\n".format(ntpath.basename(name_choices[0])))
    return 0

def get_cmd_info_str(current_cmd_num, num_cmds, partner_files, output_file_name):
    cmd_info_print = f"[{current_cmd_num}/{num_cmds}] Started mux for:"
    for index, partner_file in enumerate(partner_files):
        cmd_info_print += f"\n\t{index + 1}: {ntpath.basename(partner_file)}"
    cmd_info_print += f"\n\tOUTPUT FILE: {output_file_name}\n"
    return cmd_info_print    

def get_mkv_cmd_list(options_file_path, file_name_scheme_choice, output_dir_path, files_to_mux):
    cmds = []
    cmds_added = 1

    #partner files are the two files that are meant to be muxed together
    for _, partner_files in files_to_mux.items():
        try:
            output_file_name = ntpath.basename(partner_files[file_name_scheme_choice])
        except Exception as e:
            print("ERROR: This exception probably means that anitopy did not find consistent episode numbers for your input file names. IE there was an episode 2 in one input directory, but not the other.")    
            print("ERROR: Check your file names.")
            raise(e)
        output_file_path = "{}/{}".format(output_dir_path, output_file_name)

        new_options_file_path = os.path.dirname(options_file_path) + "/pwrmux_json/options_{}.json".format(cmds_added)

        update_options_call = functools.partial(update_options_file, options_file_path, new_options_file_path, output_file_path, partner_files)
        cmd = "mkvmerge @{}".format(new_options_file_path)

        cmd_info_print = get_cmd_info_str(cmds_added, len(files_to_mux), partner_files, output_file_name)

        cmds.append( [update_options_call, cmd_info_print, cmd, new_options_file_path] )
        cmds_added += 1

    return cmds

#wait until the stored processes are done, when they are done remove the assosciated options file 
def mkvmerge_process_wait(conditional, mkvmerge_processes, total_processes_expected):
    spinner = Halo(spinner='dots')

    while(conditional(len(mkvmerge_processes))):
        spinner.start(text='[{}/{} Muxes Finished] Muxing remaining files...'.format(mkvmerge_process_wait.completed_processes, total_processes_expected))
        sleep(0.5)
        #check if any of the processes are finished, instead of waiting for an arbitrary one to finish
        for index, process_and_options_file in enumerate(mkvmerge_processes):
            process = process_and_options_file[0]
            process_options_file_path = process_and_options_file[1]

            if process.poll() != None:
                #remove the options file assosciated with the mkvmerge process
                os.remove(process_options_file_path)
                new_options_file_dir = os.path.dirname(process_options_file_path)
                if len(os.listdir(new_options_file_dir)) == 0:
                    os.removedirs(new_options_file_dir)

                mkvmerge_processes.pop(index)                    
                mkvmerge_process_wait.completed_processes += 1  
                spinner.stop() 

def run_mux_cmds(cmds, log_file_path):
    log_to_write = []
    detailed_log_to_write = []
    mkvmerge_processes = []
    num_cores = os.cpu_count()

    mkvmerge_process_wait.completed_processes = 0
                                                   
    #run the cmds
    for cmd in cmds:
        mkvmerge_process_wait(lambda x: x >= num_cores, mkvmerge_processes, len(cmds))
        
        updated_options_file_contents = cmd[0]()        
        print(cmd[1])
        log_to_write.append(cmd[1])
        detailed_log_to_write.append(cmd[1])
        detailed_log_to_write.extend(updated_options_file_contents)

        mkvmerge_processes.append([Popen(cmd[2], shell=True, stdin=None, stdout=DEVNULL, stderr=None,close_fds=True), cmd[3]])

    #write the log, appending a list of all of the options used for muxing at the end
    log_to_write.append("\n\nDETAILED LOG WITH OPTIONS.JSON CONTENTS FOR EACH MUX:\n")
    log_to_write.extend(detailed_log_to_write)  
    with open(log_file_path, "w") as log_writer:
        log_writer.writelines(log_to_write) 
        
    #wait for any remaining processes before returning  
    mkvmerge_process_wait(lambda x: x > 0, mkvmerge_processes, len(cmds))

#input_file_name would come from the command line
#if input_file_name is None then we check if the default options.json is in the current working directory
def confirm_options_file_path(input_file_name = None):
    options_file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/" + 'options.json'    

    if input_file_name != None:
        options_file_path = input_file_name
        print("Options File (INPUT): {}".format(options_file_path))
    else:
        print("Options File (DEFAULT): {}".format(options_file_path))  

    #make sure the options file exists
    if not os.path.exists(options_file_path):
        print("That options file does not exist!")
        print("You can enter the path manually if needed: $ python pwrmux.py example/path/options.json")
        return None

    return options_file_path 

#take the original file we are muxing from 
#if only one mkv, take from the mkv
#if more than one mkv, take from the mkv that we are getting the file name from (name scheme)
#copy the title into option file contents 

def main(options_file_path):  
    original_options_file_contents = None

    with open(options_file_path, 'r') as original_options_file_reader:
        original_options_file_contents = original_options_file_reader.readlines()

    if original_options_file_contents != None:
        if len(original_options_file_contents) != 0:
            try:
                input_files_from_options_file, output_dir_path = get_paths_from_options_file(options_file_path)

                for input_file in input_files_from_options_file:
                    if os.path.dirname(input_file) == output_dir_path:
                        print("One of your input directories is the same as the output directory")
                        print("\tINPUT:", os.path.dirname(input_file))
                        print("\tOUTPUT:", output_dir_path)
                        return
                                               
                print("Input Directories:")
                for index, input_file in enumerate(input_files_from_options_file):
                    print(f"\t{index + 1}: {os.path.dirname(input_file)}/")
                print(f"Output Directory: \n\t{output_dir_path}/")

                file_name_scheme_choice = get_user_name_scheme_choice(input_files_from_options_file)
                
                #files_to_mux is a dict where each element is a list containing two files that are to be muxed
                files_to_mux = get_files_to_mux(input_files_from_options_file)                                

                cmds = get_mkv_cmd_list(options_file_path, file_name_scheme_choice, output_dir_path, files_to_mux)

                log_file_path = output_dir_path + '/muxlog.txt'
                run_mux_cmds(cmds, log_file_path)  

                print(f'Muxing finished!\n\tAll files muxed to :{output_dir_path}\n\tLog file written to :{log_file_path}')
            except Exception as e:
                #restore the original options file if something goes south
                #in normal operation the original options file is only read from not written to
                with open(options_file_path, 'w') as original_options_file_writer:
                    original_options_file_writer.writelines(original_options_file_contents)  
                raise(e)    
        else:
            print("Options file empty - {}.".format(options_file_path))              
    else:
        print("Could not open options file - {}.".format(options_file_path))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        options_file_path = confirm_options_file_path(sys.argv[1])    
    else:
        options_file_path = confirm_options_file_path()    

    if options_file_path != None:
        main(options_file_path)
    else:
        print("Could not find your options file path")
