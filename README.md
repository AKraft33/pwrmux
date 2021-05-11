<h1 align="center">PWRmux</h1>
<h4 align="center">Batch Muxing Made Simple</h4>    

---

<h4 align="center"> GPL 3.0 </h4>

---

<h2 align="left"> Getting Started </h2>

Firstly, you must create an options file using MKVToolNixGUI after selecting the settings for the mux that you want performed.

![image](https://user-images.githubusercontent.com/33562543/116497625-d437d180-a875-11eb-9044-00271d0309e6.png)

These settings will be copied to every file inside your input directories, ignoring any file that does not have the same extension as your original input file. 

Example Mux:
<ul> 
    <li>Muxing subtitles from /subtitles/Cool Show E01.srt </li>
    <li>Muxing video and audio from /video/Cool Show E01.mkv </li>
    <li>Saving video as /finished_mux/Cool Show E01.mkv </li>
    <li>
    This software will take the above settings (as an options file) to mux "Cool Show E01.srt" and "Cool Show E01.mkv"; then, pwrmux will apply those options to every file in the "subtitles" and "video" directories that those two original input files are stored in. The muxes will be mapped such that "Cool Show E02.srt" will be mapped to "Cool Show E02.mkv" and so on for each file in the directories that contained the two original files. 
    </li>
</ul>

Once you have your options file created, use the command python pwrmux.py [path to your options file] to run OR save your options file as options.json in the same directory where you saved pwrmux.py and use the command python pwrmux.py.

---

<h2 align="left"> Dependencies </h2>

<a href="https://mkvtoolnix.download/downloads.html"> MKVToolNixGUI</a> is used to create the options files needed for this program to run

<ul> <li> Installing MKVToolNixGUI will also install several other programs including <a href="https://mkvtoolnix.download/doc/mkvmerge.html"> MKVMerge </a> which is needed to do the file muxing</li> </ul>


<A href="https://pypi.org/project/halo/"> Halo </a> is used for the in progress indicator

<A href="https://pypi.org/project/anitopy/"> Anitopy </a> is used to parse file names in order to group the correct files together for muxing 

---

