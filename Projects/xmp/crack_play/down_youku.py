#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：下载优酷视频
            来源：http://zpz.name/2378/#comment-127916
            注意：使用python3实现的
'''

from sys import argv
from re import compile
from os import mkdir
from os.path import isfile, join, dirname, exists, basename
from urllib2 import quote
from urllib2 import urlopen
from json import loads
from base64 import b64decode, b64encode

_re_url_id = compile('id_(\w+)\.')

_magic_1 = b'becaf9be'
_magic_2 = b'bf7e5f01'
_info_url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/Pf/4/ctype/12/ev/1'
_m3u8_url = 'http://pl.youku.com/playlist/m3u8?ctype=12&ep=%s&ev=1&keyframe=1&oip=%s&sid=%s&token=%s&type=%s&vid=%s'

_save_base_dir = dirname(__file__)

_default_types = (
    'hd3',  # 1080P
    'dh2',  # 超清
    'mp4', '3gphd', 'flvhd',  # 高清
    'flv'  # 标清
)

def _encode(magic, s):
    f = 0
    r = []

    m = [i for i in range(256)]
    for i in range(256):
        f = (f + m[i] + magic[i % len(magic)]) % 256
        m[i], m[f] = m[f], m[i]

    f = i = 0
    for c in s:
        i = (i + 1) % 256
        f = (f + m[i]) % 256
        m[i], m[f] = m[f], m[i]
        r.append(c ^ m[(m[i] + m[f]) % 256])

    return bytes(r)


def get_youku_video(url_or_id, types=None):
    assert url_or_id, ValueError('require a you video url or id')
    if url_or_id.find('id_') > -1:
        m = _re_url_id.search(url_or_id)
        assert m, ValueError('No id contains in url')
        url_or_id = m.group(1)

    if isinstance(types, str):
        types = [types]
    elif not types:
        types = _default_types

    assert isinstance(types, (list, tuple)), \
        ValueError('prefers must be a str or list of str or None')

    print('> Get basic info of :', url_or_id)
    data = urlopen(_info_url % url_or_id).read()
    info = loads(data.decode('utf-8'))
    info = info['data'][0]
    video_name = info['title']

    print('> Video name :', video_name)
    print('> Video publisher :', info['username'])

    types = info['segs'].keys()
    video_type = None
    for t in types:
        if t in types:
            video_type = t
            break
    assert video_type, ValueError('Only "%s" formats are available.' % (', '.join(types)))

    print('> Choose video type "%s"' % video_type)

    sid, token = _encode(_magic_1, b64decode(info['ep'].encode())).split(b'_', 1)
    ep = quote(b64encode(_encode(_magic_2, sid + b'_' + url_or_id.encode() + b'_' + token))[:-1])
    token = token.decode()
    sid = sid.decode()

    print('> Retrieve file list')
    url_list = set()
    for line in urlopen(_m3u8_url % (ep, info['ip'], sid, token, video_type, url_or_id)).read().splitlines():
        line = line.strip()
        if line.startswith(b'#'):
            continue
        i = line.find(b'?')
        if i > -1:
            line = line[:i]
            url_list.add(line.decode())

    _save_dir = join(_save_base_dir, video_name.replace(' ', '__'))
    exists(_save_dir) or mkdir(_save_dir)

    print('> %s file(s) to retrieve' % len(url_list))

    for i, url in enumerate(url_list):
        filename = '%d.%s' % (i, url[url.rfind('.') + 1:])
        save_path = join(_save_dir, filename)
        print('---- ' + filename)
        if isfile(save_path):
            print('---- Fetched, Skip')
            continue

        data = urlopen(url).read()
        print('---- Size :', len(data))
        with open(save_path, 'wb') as f:
            f.write(data)
        del data

    print('> Done')


if __name__ == '__main__':
    if len(argv) < 2:
        print('''Usage:
                python3 %(s)s "youku video url or video id"
                python3 %(s)s XNjkwODQ4NTk2
                ''' % {'s': basename(argv[0])})
        exit()

    for v in argv[1:]:
        get_youku_video(v)
