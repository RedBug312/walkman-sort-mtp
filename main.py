#! /usr/bin/python3
import os
import eyed3
import mtpy

srcdir = os.path.expanduser('/home/redbug312/桌面/Touhou BGM')
dstdir = 'mtp:/Touhou BGM'[4:]
tag_order = 'aAn'

tag_getter = {
    'a': lambda audio: audio['tags'].artist or '',
    'A': lambda audio: audio['tags'].album or '',
    'n': lambda audio: audio['tags'].track_num[0] or 0
}

audiopaths = [os.path.join(root, f) for root, dirs, files in os.walk(srcdir)
                                    for f in files
                                    if os.path.splitext(f)[1] in ('.mp3', '.MP3')]

audiolist = [{'path': os.path.relpath(path, srcdir),
              'tags': eyed3.load(path).tag }
            for path in audiopaths]

reverse = False
for tag in tag_order[::-1]:
    if tag == '-':
        reverse = True
    else:
        audiolist.sort(reverse=reverse, key=tag_getter[tag])
        reverse = False


raw_devs = mtpy.get_raw_devices()
for index, raw_dev in enumerate(raw_devs):
    print('{}: {}'.format(index, repr(raw_dev)))

choose = -1
while not 0 <= choose < len(raw_devs):
    choose = int(input('Target device: '))

dev = raw_devs[choose].open()

for audio in audiolist:
    srcpath = os.path.join(srcdir, audio['path'])
    dstpath = os.path.join(dstdir, audio['path'])
    print('Upload: {}'.format(srcpath))
    print('      ⇒ {}'.format(dstpath))

    if dev.get_descendant_by_path(dstpath) is not None:
        continue

    curr = dev
    for segment in dstpath.split('/')[1:-1]:
        curr._ensure_got_children()
        if segment in curr.children_by_name:
            curr = curr.children_by_name[segment]
        else:
            curr = curr.create_folder(segment)
    curr.send_file(srcpath)

dev.close()

# eyed3.utils.log.setLevel(5)
# getLogger(MAIN_LOGGER)
# print(audiolist)

