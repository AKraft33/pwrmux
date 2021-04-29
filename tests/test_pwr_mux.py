try:
    import pytest
    import filecmp
    from src.pwrmux.pwrmux import *
except Exception as e:
    from traceback import format_exception
    exc_str = format_exception(etype=type(e), value=e, tb=e.__traceback__)
    print("{} Some modules are missing {}.\n Traceback: \n {} \n".format(__file__, e, exc_str))   

#none of these muxes will actually be ran
#organization: 
# {
# name_of_example : [example_json_file_contents],
# name_of_example : [example_json_file_contents],  
# }
example_options_files = {    
    'one_file_mux' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/Media/Cool Title/Cool Show.mkv",
        "--audio-tracks",
        "1",
        "--subtitle-tracks",
        "3",
        "--language",
        "0:und",
        "--track-name",
        "0:Presented By EMBER",
        "--default-track",
        "0:yes",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "1:jpn",
        "--sub-charset",
        "3:UTF-8",
        "--language",
        "3:eng",
        "--track-name",
        "3:Dialogue@Asakura",
        "--default-track",
        "3:yes",
        "--forced-track",
        "3:yes",
        "(",
        "/media/Media/Cool Title/Cool Show.mkv",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "0:0,0:1,0:3", 
    ],  
    'two_file_mux' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/Media/Cool Title/Cool Show.mkv",
        "--no-audio",
        "--no-video",
        "--sub-charset",
        "2:UTF-8",
        "--language",
        "2:eng",
        "--track-name",
        "2:Bakaiser",
        "--default-track",
        "2:yes",
        "(",
        "/media/Media/Cool Title/Cool Show.mkv",
        ")",
        "--audio-tracks",
        "2",
        "--no-subtitles",
        "--no-chapters",
        "--language",
        "0:und",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "2:jpn",
        "(",
        "/media/Media/Somewhat Nice Title/Nice Show.mkv",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "0:2,1:0,1:2"
    ],
    'three_file_mux' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/Media/Cool Title/Cool Show.mkv",
        "--no-audio",
        "--no-video",
        "--no-subtitles",
        "(",
        "/media/Media/Cool Title/Cool Show.mkv",
        ")",
        "--audio-tracks",
        "2",
        "--no-subtitles",
        "--no-chapters",
        "--language",
        "0:und",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "2:jpn",
        "(",
        "/media/Media/Somewhat Nice Title/Nice Show.mkv",
        ")",
        "--language",
        "0:und",
        "(",
        "/media/Media/Very Nice Title/Very Nice Show Subtitles.ass",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "1:0,1:2,2:0"
    ],
    'one_file_mux_updated' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/test output/output.mkv",
        "--audio-tracks",
        "1",
        "--subtitle-tracks",
        "3",
        "--language",
        "0:und",
        "--track-name",
        "0:Presented By EMBER",
        "--default-track",
        "0:yes",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "1:jpn",
        "--sub-charset",
        "3:UTF-8",
        "--language",
        "3:eng",
        "--track-name",
        "3:Dialogue@Asakura",
        "--default-track",
        "3:yes",
        "--forced-track",
        "3:yes",
        "(",
        "/media/test/Cool Show 2.mkv",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "0:0,0:1,0:3", 
    ],  
    'two_file_mux_updated' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/test output/output.mkv",
        "--no-audio",
        "--no-video",
        "--sub-charset",
        "2:UTF-8",
        "--language",
        "2:eng",
        "--track-name",
        "2:Bakaiser",
        "--default-track",
        "2:yes",
        "(",
        "/media/test/Cool Show 2.mkv",
        ")",
        "--audio-tracks",
        "2",
        "--no-subtitles",
        "--no-chapters",
        "--language",
        "0:und",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "2:jpn",
        "(",
        "/media/test2/Cool Show 2.mkv",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "0:2,1:0,1:2"
    ],
    'three_file_mux_updated' : [
        "--ui-language",
        "en_US",
        "--output",
        "/media/test output/output.mkv",
        "--no-audio",
        "--no-video",
        "--no-subtitles",
        "(",
        "/media/test/Cool Show 2.mkv",
        ")",
        "--audio-tracks",
        "2",
        "--no-subtitles",
        "--no-chapters",
        "--language",
        "0:und",
        "--display-dimensions",
        "0:1920x1080",
        "--language",
        "2:jpn",
        "(",
        "/media/test2/Cool Show 2.mkv",
        ")",
        "--language",
        "0:und",
        "(",
        "/media/test/Even Nicer Show Subtitles.ass",
        ")",
        "--title",
        "Test 01",
        "--track-order",
        "1:0,1:2,2:0"
    ],
}

class Temp_Path(object):
    def __init__(self, file_path, file_contents = None, delete_at_end = True):        
        self._dir_path = os.path.dirname(file_path) 
        self._file_path = file_path
        self._delete_at_end = delete_at_end

        if not os.path.exists(self._dir_path) or not os.path.isdir(self._dir_path):
            os.makedirs(self._dir_path)
            
        if file_contents == None:
            #create empty file, used for testing if a function can recognize that a file exists
            if not os.path.exists(file_path):                    
                os.mknod(file_path)  
        else:
            with open(file_path, 'w') as test_file_writer:
                test_file_writer.write('[\n')
                for line in file_contents[:-1]:
                    test_file_writer.write('  "' + line + '",\n')  
                test_file_writer.write('  "' + file_contents[-1] + '"\n')     
                test_file_writer.write(']')    
                          
    def __del__(self):      
        if self._delete_at_end:  
            os.remove(self._file_path)
            if len(os.listdir(self._dir_path)) == 0:
                os.removedirs(self._dir_path)


@pytest.mark.parametrize(
    "options_file_path, options_file_exists", [
        (os.getcwd() + "/tests/pytest_options.json", True),
        (None, False),
        (None, True),
    ],
)
def test_confirm_options_file_path(options_file_path, options_file_exists):                
    existing_options_file_contents = None
    #options.json is a special case - it is the default file checked for even when options_file_path is None
    existing_options_file_path = os.getcwd() + '/options.json' 
    print("Looking for: ", existing_options_file_path)

    #if there is already an options.json in the cwd()               
    if os.path.isfile(existing_options_file_path):            
        with open(existing_options_file_path, 'r') as existing_options_file_reader:
            existing_options_file_contents = existing_options_file_reader.readlines()

    if options_file_exists:
        if options_file_path == None:
            if existing_options_file_contents == None:
                _ = Temp_Path(os.getcwd() + '/options.json')
        else:    
            _ = Temp_Path(options_file_path)
    else:
        if os.path.isfile(existing_options_file_path):  
            os.remove(existing_options_file_path)    
    
    options_file = confirm_options_file_path(options_file_path)  

    if options_file_exists:
        assert(options_file != None)
    else:        
        assert(options_file == None)

    if existing_options_file_contents != None:
        print("Writing to options file")
        with open(existing_options_file_path, 'w') as existing_options_file_writer:
            existing_options_file_writer.writelines(existing_options_file_contents)         

@pytest.mark.parametrize(
    "options_file_path, options_file_contents, expected_file_extensions, expected_input_files_from_options_file, expected_output_dir", [
        (os.getcwd() + "/tests/pytest_options.json", example_options_files['one_file_mux'], ['.mkv'], ['/media/Media/Cool Title/Cool Show.mkv'], '/media/Media/Cool Title'),
        (os.getcwd() + "/tests/pytest_options.json", example_options_files['two_file_mux'], ['.mkv', '.mkv'], ['/media/Media/Cool Title/Cool Show.mkv', '/media/Media/Somewhat Nice Title/Nice Show.mkv'], '/media/Media/Cool Title'),
        (os.getcwd() + "/tests/pytest_options.json", example_options_files['three_file_mux'], ['.mkv', '.mkv', '.ass'], ['/media/Media/Cool Title/Cool Show.mkv', '/media/Media/Somewhat Nice Title/Nice Show.mkv', '/media/Media/Very Nice Title/Very Nice Show Subtitles.ass'], '/media/Media/Cool Title'),        
    ],
)
def test_get_paths_from_options_file(options_file_path, options_file_contents, expected_file_extensions, expected_input_files_from_options_file, expected_output_dir):   
    _ = Temp_Path(options_file_path, options_file_contents) 

    directories = get_paths_from_options_file(options_file_path)

    assert(directories[0] == expected_input_files_from_options_file)
    assert(directories[1] == expected_output_dir)

@pytest.mark.parametrize(
    "input_files_from_options_file, files_to_create, expected_files_found", [
         #one input directory, 2 files in directory, no anitopy
        (["/tests_1/test.txt"], ['/tests_1/test2.txt'], {1 : ["/tests_1/test.txt"], 2 : ['/tests_1/test2.txt']} ), 
        #one input directory, 2 files in directory, with anitopy
        (["/tests_1/test E03.txt"], ['/tests_1/test2 E04.txt'], {'03' : ["/tests_1/test E03.txt"], '04' : ['/tests_1/test2 E04.txt']} ),
        #one input directory, 4 files in directory - ignore json file, no anitopy
        (["/tests_1/test.txt"], ['/tests_1/test2.txt', '/tests_1/test3.txt', "/tests_1/test4.json"], {1 : ["/tests_1/test.txt"], 2 : ['/tests_1/test2.txt'], 3 : ['/tests_1/test3.txt']} ), 
        #one input directory, 4 files in directory - ignore json file, with anitopy
        (["/tests_1/test E03.txt"], ['/tests_1/test E04.txt', '/tests_1/test E05.txt', "/tests_1/test E06.json"], {'03' : ["/tests_1/test E03.txt"], '04' : ['/tests_1/test E04.txt'], '05' : ['/tests_1/test E05.txt']} ),        
        #two input directories, 2 files in each directory, no anitopy
        (["/tests_1/test.txt", "/tests_2/test.txt"], ['/tests_1/test2.txt', '/tests_2/test2.txt'], {1 : ["/tests_1/test.txt", '/tests_2/test.txt'], 2 : ['/tests_1/test2.txt', '/tests_2/test2.txt']} ),
        #two input directories, 2 files in each directory, with anitopy
        (["/tests_1/test E03.txt", "/tests_2/test E03.txt"], ['/tests_1/test E12.txt', '/tests_2/test E12.txt'], {'03' : ["/tests_1/test E03.txt", '/tests_2/test E03.txt'], '12' : ['/tests_1/test E12.txt', '/tests_2/test E12.txt']} ),
        #three input directories, 2 files in each directory - one json file to be ignored, no anitopy
        (["/tests_1/test.txt", "/tests_2/test.txt", "/tests_3/test.txt"], ['/tests_1/test2.txt', '/tests_2/test2.txt', "/tests_3/test2.txt", "/tests_3/test2.json"], {1 : ["/tests_1/test.txt", '/tests_2/test.txt', "/tests_3/test.txt"], 2 : ['/tests_1/test2.txt', '/tests_2/test2.txt', "/tests_3/test2.txt"]} ),
        #three input directories, 2 files in each directory, with anitopy
        (["/tests_1/test E07.txt", "/tests_2/test E07.txt", "/tests_3/test E07.txt"], ['/tests_1/test E04.txt', '/tests_2/test E04.txt', '/tests_3/test E04.txt'], {'07' : ["/tests_1/test E07.txt", '/tests_2/test E07.txt', '/tests_3/test E07.txt'], '04' : ['/tests_1/test E04.txt', '/tests_2/test E04.txt', '/tests_3/test E04.txt']} ),
    ],
)
def test_get_files_to_mux(input_files_from_options_file, files_to_create, expected_files_found):
    files_created = []
    for index, input_file_path in enumerate(input_files_from_options_file):
        updated_input_file_path = os.getcwd() + input_file_path 
        input_files_from_options_file[index] = updated_input_file_path       
        files_created.append(Temp_Path(updated_input_file_path))

    for file_to_create in files_to_create:
        files_created.append(Temp_Path(os.getcwd() + file_to_create))

    for key, files_to_mux in expected_files_found.items():
        updated_list_of_expcted_files_to_mux = []
        for file_to_mux in files_to_mux:
            updated_list_of_expcted_files_to_mux.append(os.getcwd() + file_to_mux)
        expected_files_found[key] = updated_list_of_expcted_files_to_mux     

    found_files = get_files_to_mux(input_files_from_options_file)    
    assert(found_files == expected_files_found)

@pytest.mark.parametrize(
    "options_file_path, options_file_contents, new_options_file_path, output_file_path, input_files_to_mux, expected_options_file_contents", [
        (os.getcwd() + "/tests/test_options.json", example_options_files['one_file_mux'], os.getcwd() + "/tests4/new_tests_options.json", "/media/test output/output.mkv", ["/media/test/Cool Show 2.mkv"], example_options_files['one_file_mux_updated']),
        (os.getcwd() + "/tests2/test_options.json", example_options_files['two_file_mux'], os.getcwd() + "/tests5/new_tests_options.json", "/media/test output/output.mkv", ["/media/test/Cool Show 2.mkv", "/media/test2/Cool Show 2.mkv"], example_options_files['two_file_mux_updated']),
        (os.getcwd() + "/tests3/test_options.json", example_options_files['three_file_mux'], os.getcwd() + "/tests6/new_tests_options.json", "/media/test output/output.mkv", ["/media/test/Cool Show 2.mkv", "/media/test2/Cool Show 2.mkv", "/media/test/Even Nicer Show Subtitles.ass"], example_options_files['three_file_mux_updated'])
    ],
)
def test_update_options_file(options_file_path, options_file_contents, new_options_file_path, output_file_path, input_files_to_mux, expected_options_file_contents):
    _ = Temp_Path(options_file_path, options_file_contents) 

    expected_options_file_path = os.getcwd() + "/tests/expected_options_file.json"
    expected_option_file = Temp_Path(expected_options_file_path, expected_options_file_contents)

    update_options_file(options_file_path, new_options_file_path, output_file_path, input_files_to_mux)

    assert(filecmp.cmp(new_options_file_path ,expected_options_file_path, shallow=False))
    
    os.remove(new_options_file_path)
    new_options_file_dir = os.path.dirname(new_options_file_path)
    if len(os.listdir(new_options_file_dir)) == 0:
        os.removedirs(new_options_file_dir)

@pytest.mark.parametrize(
    "name_scheme_choice, name_scheme_contents", [
        (1, [" "]), 
        (2, [" ", " "]),
        (5, [" ", " ", " ", " ", " ", " ", " ", " "])
    ],
)
def test_get_user_name_scheme_choice(monkeypatch, name_scheme_choice, name_scheme_contents):
    monkeypatch.setattr('builtins.input', lambda _: name_scheme_choice)

    result = get_user_name_scheme_choice(name_scheme_contents)    
    assert(result == name_scheme_choice - 1)

@pytest.mark.parametrize(
    "current_cmd_num, num_cmds, partner_files, output_file_path, expected_str", [
        (1, 1, ['test1.mkv'], 'out/test1.mkv', '[1/1] Performing mux for:\n\t1: test1.mkv\n\tOUTPUT FILE: out/test1.mkv\n'),
        (1, 1, ['test1.mkv', 'test2.mkv'], 'out/test1.mkv', '[1/1] Performing mux for:\n\t1: test1.mkv\n\t2: test2.mkv\n\tOUTPUT FILE: out/test1.mkv\n'),
        (2, 16, ['test1.mkv', 'test2.mkv','test3.mkv'], 'out/test1.mkv', '[2/16] Performing mux for:\n\t1: test1.mkv\n\t2: test2.mkv\n\t3: test3.mkv\n\tOUTPUT FILE: out/test1.mkv\n'),
    ]
)
def test_get_cmd_info_str(current_cmd_num, num_cmds, partner_files, output_file_path, expected_str):
    output_str = get_cmd_info_str(current_cmd_num, num_cmds, partner_files, output_file_path)
    assert(output_str == expected_str)

@pytest.mark.parametrize(
    "options_file_path, file_name_scheme_choice, output_dir_path, files_to_mux, expected_cmds", [
        (os.getcwd() + '/test_options.json', 1, os.getcwd() + '/out', {1 : [os.getcwd() + '/test1.mkv', os.getcwd() + '/test2.mkv']}, ['mkvmerge @{}'.format(os.getcwd() + '/pwrmux_json/options_1.json')]),
        (os.getcwd() + '/test_options.json', 1, os.getcwd() + '/test_out', {1 : [os.getcwd() + '/test1.mkv', os.getcwd() + '/test2.mkv'], 2 : [os.getcwd() + '/test3.mkv', os.getcwd() + '/test4.mkv']}, ['mkvmerge @{}'.format(os.getcwd() + '/pwrmux_json/options_1.json'), 'mkvmerge @{}'.format(os.getcwd() + '/pwrmux_json/options_2.json')]),
    ],
)
def test_get_mkv_cmd_list(options_file_path, file_name_scheme_choice, output_dir_path, files_to_mux, expected_cmds):
    cmd_list = get_mkv_cmd_list(options_file_path, file_name_scheme_choice, output_dir_path, files_to_mux)
    
    for index, cmd in enumerate(cmd_list):
        #cmd[0] is just a stored function call to update options
        expected_cmd_info_string = get_cmd_info_str(index + 1, len(expected_cmds), files_to_mux[index + 1], ntpath.basename(files_to_mux[index + 1][file_name_scheme_choice]))
        assert(cmd[1] == expected_cmd_info_string)
        assert(cmd[2] == expected_cmds[index])