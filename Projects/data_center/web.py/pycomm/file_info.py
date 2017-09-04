#!/usr/bin/env python
# coding: utf-8

import os
import distutils.dir_util
import distutils.file_util
import md5
import sha

def rm(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        elif os.path.isdir(path):
            distutils.dir_util.remove_tree(path)
            return True
    except:
        return False
        
def relate(from_path, to_path):
    try:
        os.link(from_path, to_path)
        return True
    except:
        pass

    try:
        os.symlink(from_path, to_path)
        return True
    except:
        pass

    return bool(distutils.file_util.copy_file(from_path, to_path)[1])
    
def exists_path(path):
    return os.path.exists(path)

def get_dir(path):
    return os.path.split(path)[0]
    
def get_basename(path):
    return os.path.splitext(path)[0]
    
def get_filename(path):
    return os.path.split(path)[1]

def get_filesize(path):
    return os.path.getsize(path)

def get_suffix(path):
    return os.path.splitext(path)[1]
        
def get_prefix(path):
    return get_filename(get_basename(path))
        
def random_read_data(fd, position, length):
    fd.seek(position, 0)
    return fd.read(length)
        
def get_cid_hex(path):
    k_cid_block_size = 20 * 1024

    file_length = os.path.getsize(path)
    fd = open(path, "rb")
    cid = sha.new()

    if file_length < k_cid_block_size * 3:
        cid.update(random_read_data(fd, 0, file_length))
    else:
        cid.update(random_read_data(fd, 0, k_cid_block_size))
        cid.update(random_read_data(fd, file_length / 3, k_cid_block_size))
        cid.update(random_read_data(fd, file_length - k_cid_block_size, k_cid_block_size))

    fd.close()
    return cid.hexdigest()

def get_cid(path):
    k_cid_block_size = 20 * 1024

    file_length = os.path.getsize(path)
    fd = open(path, "rb")
    cid = sha.new()

    if file_length < k_cid_block_size * 3:
        cid.update(random_read_data(fd, 0, file_length))
    else:
        cid.update(random_read_data(fd, 0, k_cid_block_size))
        cid.update(random_read_data(fd, file_length / 3, k_cid_block_size))
        cid.update(random_read_data(fd, file_length - k_cid_block_size, k_cid_block_size))

    fd.close()
    return cid.digest()

def get_file_md5_hex(path):  
    fileinfo = os.stat(path)  
    if int(fileinfo.st_size)/(1024*1024)>1000:  
        return get_bigfile_md5_hex(path)  
    m = md5.new()  
    f = open(path,'rb')  
    m.update(f.read())  
    f.close()  
    return m.hexdigest()

def get_bigfile_md5_hex(path):  
    m = md5.new()  
    f = open(path,'rb')  
    maxbuf = 8192  

    while 1:  
        buf = f.read(maxbuf)  
        if not buf:  
            break  
        m.update(buf)  

    f.close()  
    return m.hexdigest()  

if __name__ == '__main__':
    file = '/home/root1/5868936b659c57a3ce56198f1b1dd3a8.mp4'
    print get_dir(file)
    print get_basename(file)
    print get_filename(file)
    print get_filesize(file)
    print get_suffix(file)
    print get_prefix(file)
    print get_cid_hex(file).upper()
    print get_cid(file)
    print get_file_md5_hex(file)