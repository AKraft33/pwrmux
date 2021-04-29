from distutils.core import setup
setup(
  name = 'pwrmux',         # How you named your package folder (MyLib)
  packages = ['pwrmux'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='GPL V3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Allows batch muxing of files from multiple directories using an options file created by MKVToolNixGUI.'
  author = 'Adam Kraft',                  
  author_email = 'kraftadam47@gmail.com',      
  url = 'https://github.com/AKraft33/pwrmux',   
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Mux', 'Video', 'Media'],   # Keywords that define your package best
  install_requires=[            
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