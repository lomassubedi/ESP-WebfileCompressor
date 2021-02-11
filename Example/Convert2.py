#!/usr/bin/python
import requests
import sys
import os
import json
import pprint
import shutil
import gzip

input_dir = "spa_new"  # Sub folder of webfiles
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
output_file_c_header = "web_file.h"
output_file_var_list = "var_list.txt"

dict_output_sub_dir = {
    "minified":"minified",
    "compressed":"compressed",
    "source":"source"
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
    print("Files getting compressed ")
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
            output_str += hex(ord(byte))
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


def create_source_files():
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "w") as c_src:
        c_src.write("#ifndef " + output_file_c_header.split('.')[0].upper() + "_H_\n#define " + output_file_c_header.split('.')[0].upper() + "_H_")
        c_src.write("\n\n")
        c_src.write("#include<Arduino.h>")
        c_src.write("\n" * 2)
        c_src.close()

    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_var_list), "w") as v_list:
        v_list.write("\n" * 2)
        v_list.write("List of variables created in file : " + output_file_c_header)
        v_list.write("\n" * 2)
        v_list.close()

def terminate_source_file():
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "a+") as c_src:
        c_src.write("#endif " + " // End of " + output_file_c_header.split('.')[0].upper() + "_H_")
        c_src.close()

def write_to_file(filepath = "", data=""):
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "a+") as c_src:
        c_src.write("\n" * 2)
        # filepath = css/main.css
        if "BarlowCondensed" in filepath:
            print("Hey ! Stop man.")

        filename = os.path.basename(filepath)

        file_name_w_ext = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]

        filepath = "/".join(filepath.strip("\\").split('\\')[1:])

        path_for_src = filepath.replace("\\", "/")
        file_name_w_ext = file_name_w_ext.replace("-", "_")
        file_name_w_ext = file_name_w_ext.replace(".", "_")
        file_name_w_ext = file_name_w_ext.replace("x", "_")

        file_extension = file_extension.replace(".", "")

        c_src.write("const char* path_" + file_name_w_ext + "_" + file_extension + " PROGMEM = " + "\"" + path_for_src + "\";\n\n")

        c_src.write("const char data_" + file_name_w_ext + "_" + file_extension + "[] PROGMEM = { " )

        hex_len = len(data)
        if hex_len > 0:
            byte_counter = 0
            for byte in data:
                c_src.write(byte)
                if(byte == ','):
                    c_src.write(" ")
                    byte_counter = byte_counter + 1
                    if((byte_counter % 16) == 0):
                        c_src.write("\n\t\t\t\t")
        else:
            print("invalid hex string")
        c_src.write(" };\n")
        c_src.close()

        with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_var_list), "a+") as v_list:
            # v_list.write("path_" + file_name_w_ext + "_" + file_extension + "\n")
            # v_list.write("data_" + file_name_w_ext + "_" + file_extension + "\n")
            # v_list.write("handler_" + file_name_w_ext + "_" + file_extension + "\n")
            v_list.write("Webserver->on(path_" + file_name_w_ext + "_" + file_extension + ", HTTP_GET, " + "handler_" + \
                         file_name_w_ext + "_" + file_extension + ");\n")
            # v_list.write("\n")
            v_list.close()


for root, dirs, files in os.walk(input_dir, topdown=False):
    # Process Files
    for filename in files:  # for files
        file_details_dict = {
            "filepath": None,
            "filename": None,
            "relpath": None,
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
        file_details_dict["relpath"] = dirname
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


print("file will be converted to HEX")
# with open(os.path.join(f_output, "test.txt"), "x") as flo:
create_source_files()
for file in file_list:
    print("Writing content of " + file["filepath"])
    # a = file2Hex(os.path.join(dict_output_sub_dir["compressed"], file["filename"] + ".gz"))
    # print(a)
    write_to_file(file["filepath"], file2Hex(os.path.join(f_output, dict_output_sub_dir["compressed"], file["filename"] + ".gz")))

terminate_source_file()


