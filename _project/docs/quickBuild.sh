# delete old files and folders in root path
cd ../..
find . -type f -name '*.html' -delete
rm sitemap.xml objects.inv searchindex.js
rm -R about blog _images _sources _static

# make html
cd _project/docs/
make clean
make html
python ../src/postprocessing.py

# copy files to front folder
cp -r build/html/*  ../../


# open page
firefox ../../index.html
