import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = 'pwrmux-AKraft33',       
  version = '1.0',      
  license = 'GPL V3.0',        
  description = 'Allows batch muxing of files from multiple directories using an options file created by MKVToolNixGUI.',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'Adam Kraft',                  
  author_email = 'kraftadam47@gmail.com',      
  url = 'https://github.com/AKraft33/pwrmux',   
  keywords = ['Mux', 'Video', 'Media'],   
  install_requires = [            #other pip projects that this project depends on
          'halo',
          'anitopy',
      ],
  classifiers = [
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: End Users/Desktop',
    'Topic :: Multimedia :: Video',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
    'Programming Language :: Python :: 3',     
  ],
  package_dir = {"": "src"},
  packages = setuptools.find_packages(where="src"),
  python_requires = ">=3"
)