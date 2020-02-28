# -*- coding: utf-8 -*-

import os
import os.path
import hashlib

import magic
import requests
from flask import current_app



def get_path(url, extension=None):
    if not hasattr(get_path, 'cache'):
        setattr(get_path, 'cache', {})

    if url in get_path.cache:
        return get_path.cache[url]

    cache_dir = current_app.config['CACHE_EXTERNAL_ASSETS_DIR']
    filename_hash = hashlib.new('md5')
    filename_hash.update(url)

    if not extension:
        extension = ''

    filename = '{}/{}{}'.format(
        cache_dir,
        filename_hash.hexdigest(),
        extension,
    )

    get_path.cache[url] = filename
    return get_path.cache[url]


def get_filepath(url):
    return os.path.join(
        current_app.config['CACHE_EXTERNAL_ASSETS_ROOT'],
        get_path(url),
    )


def get_cached_file_with_extension(url):
    prefix = '/'

    filepath = get_filepath(url)
    path = get_path(url)

    for ext in ('.jpg', '.png', ''):
        if os.path.exists(filepath + ext) and \
           os.stat(filepath + ext).st_size > 0:
            return prefix + path + ext
    return False


def rename_with_magic(filepath):
    if os.path.exists(filepath):
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(filepath)
        if mime_type == 'image/jpeg':
            os.rename(filepath, filepath + '.jpg')
        elif mime_type == 'image/png':
            os.rename(filepath, filepath + '.png')


def cache_external_assets(url):
    # if not external, return direct file
    if not url.startswith('http'):
        return url

    filepath = get_filepath(url)

    # Try to rename already existing file
    rename_with_magic(filepath)

    ret = get_cached_file_with_extension(url)
    if ret:
        return ret

    try:
        os.makedirs(os.path.dirname(filepath))
    except:  # FIXME: handle exceptions
        pass

    with open(filepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            # Something went wrong
            raise RuntimeError('Cannot request image')

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    # Try to rename, just downloaded file
    rename_with_magic(filepath)

    return get_cached_file_with_extension(filepath)


class CacheExternalAssets(object):
    """ Adds a jinja filter for caching external assets. """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if 'CACHE_EXTERNAL_ASSETS_ROOT' not in app.config:
            raise RuntimeError('You must specify CACHE_EXTERNAL_ASSETS_ROOT')
        app.config.setdefault('CACHE_EXTERNAL_ASSETS_DIR', 'external')
        app.jinja_env.filters['cache_external_assets'] = cache_external_assets

    def teardown(self, exception):
        pass
