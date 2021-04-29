from distutils.core import setup
setup(
  name = 'pwrmux',         
  packages = ['pwrmux'],   
  version = '1.0',      
  license='GPL V3.0',        
  description = 'Allows batch muxing of files from multiple directories using an options file created by MKVToolNixGUI.'
  author = 'Adam Kraft',                  
  author_email = 'kraftadam47@gmail.com',      
  url = 'https://github.com/AKraft33/pwrmux',   
  download_url = 'https://github.com/AKraft33/pwrmux/archive/refs/tags/1.0.tar.gz',
  keywords = ['Mux', 'Video', 'Media'],   
  install_requires=[            #other pip projects that this project depends on
          'halo',
          'anitopy',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Media Creators',
    'Topic :: Video :: Media Productio',
    'License :: GNU Public License V3.0',  
    'Programming Language :: Python :: 3',     
  ],
)