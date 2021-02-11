#!/usr/bin/python
import requests
import sys
import os
import json
import pprint
import shutil
import gzip

input_dir = "new_mew"  # Sub folder of webfiles
output_dir = "HTML_minified"

# try:
#     sys.argv[1]
# except NameError:
#     f_output = 'output_dir'
# else:
#     f_output = sys.argv[1]

f_output = "output"
f_output_minified = f_output + "/minified"
f_output_compressed = f_output + "/compressed"
f_output_c_source = f_output + "/c_source"

dict_output_sub_dir = {
    "minified":"minified",
    "compressed":"compressed",
    "c_source":"c_source"
}
# print("Output stored at : " + f_output)

# f_output = open(f_output, "w")
# f_output = open("output_dir", "w")
URL_minify_js = 'https://javascript-minifier.com/raw'  # Website to minify javascript
URL_minify_html = 'https://html-minifier.com/raw'  # Website to minify html
URL_minify_css = 'https://cssminifier.com/raw'  # Website to minify css


def minify_js(input_file):
    url = URL_minify_js
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def minify_html(input_file):
    url = URL_minify_html
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def minify_css(input_file):
    url = URL_minify_css
    data = {'input': open(input_file, 'rb').read()}
    response = requests.post(url, data=data)
    return response.text

def compress_file():
    for file in file_list:
        with open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), 'rb') as src, \
                gzip.open(os.path.join(f_output, dict_output_sub_dir["compressed"], file["filename"] + ".gz"), 'wb') as dst:
            dst.writelines(src)
            src.close()
            dst.close()
    pass

def file2Hex(filename):
    output_str = ""
    x = 1
    myfile = open(filename, "rb")
    try:
        binLen = os.path.getsize(filename)
        byte = myfile.read(1)
        for byte_num in range(0, binLen):
        # while byte != "":
        #     try:
            output_str += hex(ord(byte))
            # except:
            #     print("got an error");
            if (x != binLen):
                output_str += ","
            x += 1
            # Next Byte
            byte = myfile.read(1)
    finally:
        myfile.close()
    return output_str

file_list = []

try:
    shutil.rmtree(f_output)
except OSError as e:
    print("Error: %s : %s" % (f_output, e.strerror))

os.mkdir(f_output)

for dirs in dict_output_sub_dir:
    path = os.path.join(f_output, dirs)
    os.mkdir(path)


for root, dirs, files in os.walk(input_dir, topdown=False):
    # Process Files
    for filename in files:  # for files
        file_details_dict = {
            "filepath": None,
            "filename": None,
            "filetype": None
        }
        fullfilename = os.path.join(root, filename)
        # print("fullfilename: " + fullfilename)
        # print("filename: " + filename)
        dirname = fullfilename.rsplit('/', 1)[0].strip(input_dir + "/")  # Get Dirname
        # print("dirname: " + dirname)
        # process_file(dirname, filename, fullfilename)
        file_details_dict["filepath"] = fullfilename
        file_details_dict["filename"] = filename
        file_details_dict["filetype"] = os.path.splitext(filename)[1]
        file_list.append(file_details_dict)
        del file_details_dict

for file in file_list:
    if file["filepath"].endswith(".js"):
        print("Output JAVASRIPT: " + file["filepath"])
        minified = minify_js(file["filepath"])  # minify javascript
        f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "x", encoding="utf-8")
        f.write(minified)
        f.close()

    elif file["filepath"].endswith(".css"):
        print("Output CSS: " + file["filepath"])
        minified = minify_css(file["filepath"])  # minify javascript
        if(file["filename"] == "vendor.css"):
            a = 0
        f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "w", encoding="utf-8")
        f.write(minified)
        f.close()

    elif file["filepath"].endswith(".html"):
        print("Output HTML: " + file["filepath"])
        minified = minify_html(file["filepath"])  # minify javascript
        f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "w", encoding="utf-8")
        f.write(minified)
        f.close()

    else:
        shutil.copyfile(file["filepath"], os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]))

compress_file()

# for file in file_list:
with open(os.path.join(f_output, "test.txt"), "x") as flo:
    flo.write(file2Hex(os.path.join(f_output, dict_output_sub_dir["compressed"], "index.html.gz")))
    flo.close()

