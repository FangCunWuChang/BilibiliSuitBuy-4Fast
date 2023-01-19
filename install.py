import shutil
import glob
import os

if __name__ == '__main__':
    shutil.move("./dist/main.exe", "./")
    print("./dist/main.exe move to ./")

    python_exe_list = glob.glob("./http/source/python/dist/*.exe")
    golang_exe_list = glob.glob("./http/source/golang/*.exe")
    for http_exe_path in python_exe_list + golang_exe_list:
        shutil.move(http_exe_path, "./http/exe")
        print("%s move to %s" % (http_exe_path, "./http/exe"))

    delete_folder_list = [
        "./dist", "./build",
        "./http/source/python/dist",
        "./http/source/python/build"
    ]

    for delete_folder in delete_folder_list:
        shutil.rmtree(delete_folder)
        print("delete folder %s" % (delete_folder,))

    http_spec_file_list = glob.glob("./http/source/python/*.spec")
    spec_file_list = glob.glob("./*.spec")
    for spec_file_path in http_spec_file_list + spec_file_list:
        os.remove(spec_file_path)
        print("delete file %s" % (spec_file_path,))
