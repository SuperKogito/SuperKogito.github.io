make clean
make html
python ../src/postprocessing.py

# open page
firefox build/html/index.html
