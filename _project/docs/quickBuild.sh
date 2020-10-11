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

# rm extra css files 
rm -f ../../_static/css/code_style.css ../../_static/css/custom_pygments.css ../../_static/css/ls.css ../../_static/css/scustom_style.css ../../_static/css/tree_graph.css ../../_static/css/new.css ../../_static/css/custom.css

# delete extra fonts
cd ../../_static/fonts
ls | grep -v "ubuntu" | xargs rm -R

cd ../../_project/docs

# open page
firefox ../../index.html
