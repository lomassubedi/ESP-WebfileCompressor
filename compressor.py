#!/usr/bin/python
import requests
import sys
import os
import shutil
import gzip

f_input = ""
f_output = "output"
output_file_c_header = "web_file.h"
output_file_var_list = "arduino_snippet.txt"

dict_output_sub_dir = {
    "minified": "minified",
    "compressed": "compressed",
    "source": "source"
}

URL_minify_js = 'https://javascript-minifier.com/raw'  # Website to minify javascript
URL_minify_html = 'https://html-minifier.com/raw'  # Website to minify html
URL_minify_css = 'https://cssminifier.com/raw'  # Website to minify css

file_list = []


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
                gzip.open(os.path.join(f_output, dict_output_sub_dir["compressed"], file["filename"] + ".gz"),
                          'wb') as dst:
            dst.writelines(src)
            src.close()
            dst.close()
    pass


def file2Hex(filename):
    output_str = ""
    x = 1
    myfile = open(filename, "rb")
    try:
        bin_len = os.path.getsize(filename)
        byte = myfile.read(1)
        for byte_num in range(0, bin_len):
            output_str += hex(ord(byte))
            if x != bin_len:
                output_str += ","
            x += 1
            # Next Byte
            byte = myfile.read(1)
    finally:
        myfile.close()
    return output_str


def create_source_files():
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "w") as c_src:
        c_src.write(
            "#ifndef " + output_file_c_header.split('.')[0].upper() + "_H_\n#define " + output_file_c_header.split('.')[
                0].upper() + "_H_")
        c_src.write("\n\n")
        c_src.write("#include<Arduino.h>")
        c_src.close()

    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_var_list), "w") as v_list:
        v_list.write("*" * 20)
        v_list.write("\nList of variables created in file : " + output_file_c_header + "\n")
        v_list.write("*" * 20)
        v_list.write("\n" * 2)
        v_list.close()


def terminate_source_file():
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "a+") as c_src:
        c_src.write("#endif " + " // End of " + output_file_c_header.split('.')[0].upper() + "_H_")
        c_src.close()


def write_to_file(filepath="", data=""):
    with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_c_header), "a+") as c_src:
        c_src.write("\n" * 2)
        file_name = os.path.basename(filepath)

        file_name_w_ext = os.path.splitext(file_name)[0]
        file_extension = os.path.splitext(file_name)[1]

        filepath = "/".join(filepath.strip("\\").split('\\')[1:])

        path_for_src = filepath.replace("\\", "/")
        file_name_w_ext = file_name_w_ext.translate({ord(c): "_" for c in "!@#$%^&*;:,.<>?|`~-=+"})

        file_extension = file_extension.replace(".", "")

        c_src.write(
            "const char* path_" + file_name_w_ext + "_" + file_extension + " PROGMEM = " + "\"/" + path_for_src + "\";\n")

        c_src.write("const char data_" + file_name_w_ext + "_" + file_extension + "[] PROGMEM = {\n\t\t")

        hex_len = len(data)
        if hex_len > 0:
            byte_counter = 0
            for byte in data:
                c_src.write(byte)
                if byte == ',':
                    c_src.write(" ")
                    byte_counter = byte_counter + 1
                    if (byte_counter % 16) == 0:
                        c_src.write("\n\t\t")
        else:
            print("invalid hex string")
        c_src.write("};\n")
        c_src.close()

        with open(os.path.join(f_output, dict_output_sub_dir["source"], output_file_var_list), "a+") as v_list:
            v_list.write("Webserver->on(path_" + file_name_w_ext + "_" + file_extension + ", HTTP_GET, " + "handler_" + \
                         file_name_w_ext + "_" + file_extension + ");\n")
            v_list.close()

def main():
    try:
        sys.argv[1]
    except:
        print("Error: Enter input directory to proceed.")
        return
    else:
        f_input = sys.argv[1]

    print("Input files will be taken from: " + f_input)
    print("Output files stored at: " + f_output)

    # Remove old directories and files
    try:
        shutil.rmtree(f_output)
    except OSError as e:
        print("Error: %s : %s" % (f_output, e.strerror))

    os.mkdir(f_output)

    for dirs in dict_output_sub_dir:
        path = os.path.join(f_output, dirs)
        os.mkdir(path)

    # list file directories and other details
    for root, dirs, files in os.walk(f_input, topdown=False):
        for filename in files:  # for files
            file_details_dict = {
                "filepath": None,
                "filename": None,
                "filetype": None
            }
            fullfilename = os.path.join(root, filename)
            # dirname = fullfilename.rsplit('/', 1)[0].strip(f_input + "/")  # Get Dirname
            file_details_dict["filepath"] = fullfilename
            file_details_dict["filename"] = filename
            file_details_dict["filetype"] = os.path.splitext(filename)[1]
            file_list.append(file_details_dict)
            del file_details_dict

    # Minify and compress files
    for file in file_list:
        if file["filepath"].endswith(".js"):
            print("Minifying and copying file: " + file["filepath"])
            minified = minify_js(file["filepath"])  # minify javascript
            f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "x", encoding="utf-8")
            f.write(minified)
            f.close()

        elif file["filepath"].endswith(".css"):
            print("Minifying and copying file: " + file["filepath"])
            minified = minify_css(file["filepath"])  # minify javascript
            if file["filename"] == "vendor.css":
                a = 0
            f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "w", encoding="utf-8")
            f.write(minified)
            f.close()

        elif file["filepath"].endswith(".html"):
            print("Minifying and copying file: " + file["filepath"])
            minified = minify_html(file["filepath"])  # minify javascript
            f = open(os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]), "w", encoding="utf-8")
            f.write(minified)
            f.close()

        else:
            print("Processing file: " + file["filepath"])
            shutil.copyfile(file["filepath"], os.path.join(f_output, dict_output_sub_dir["minified"], file["filename"]))

    print("Compressing files")
    compress_file()

    print("Converting compressed files to hex string")
    create_source_files()

    for file in file_list:
        print("Writing content of " + file["filepath"])
        write_to_file(file["filepath"],
                      file2Hex(os.path.join(f_output, dict_output_sub_dir["compressed"], file["filename"] + ".gz")))

    terminate_source_file()


if __name__ == "__main__":
    main()
