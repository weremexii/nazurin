import os
import re
import shutil
import requests
from config import *
from pybooru import Danbooru as danbooru

class Danbooru(object):
    api = danbooru('danbooru')

    def view(self, id):
        post = self.api.post_show(id)
        url = post['file_url']
        artists = post['tag_string_artist']
        tags = post['tag_string'].split(' ')
        title, filename = self._getNames(post)
        imgs = list()
        imgs.append({'url': url, 'name': filename})
        tag_string = str()
        for character in tags:
            tag_string += '#' + character + ' '
        details = {'Title': title, 'Artist': artists, 'Tags': tag_string, 'Url': 'https://danbooru.donmai.us/posts/' + str(id)}
        if post['children_ids']:
            details.setdefault('Children', post['children_ids'])
        return imgs, details

    def download(self, id):
        imgs, _ = self.view(id)
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        for img in imgs:
            if not os.path.exists(DOWNLOAD_DIR + img['name']):
                response = requests.get(img['url'], stream=True).raw
                with open(DOWNLOAD_DIR + img['name'], 'wb') as f:
                    shutil.copyfileobj(response, f)
        return imgs

    def _getNames(self, post):
        characters = post['tag_string_character']
        copyrights = post['tag_string_copyright']
        artists = post['tag_string_artist']
        filename = str()
        if characters:
            filename += self._formatCharacters(characters) + ' '
        if copyrights:
            copyrights = self._formatCopyrights(copyrights)
            if characters:
                filename += '(' + copyrights + ')'
            else:
                filename += copyrights
        title = filename
        if artists:
            filename += ' drawn by ' + self._normalize(self._sentence(artists.split(' ')))
        if filename: # characters or copyrights present
            filename += ' - '
        filename += os.path.basename(post['file_url'])
        return title, filename

    def _formatCharacters(self, characters):
        characters = characters.split(' ')
        characters = list(map(self._normalize, characters))
        size = len(characters)
        if size <= 5:
            result = self._sentence(characters)
        else:
            characters = characters[:5]
            result = self._sentence(characters) + ' and ' + str(size - 1) + ' more'
        return result

    def _formatCopyrights(self, copyrights):
        copyrights = copyrights.split(' ')
        copyrights = list(map(self._normalize, copyrights))
        size = len(copyrights)
        if size == 1:
            result = copyrights[0]
        else:
            result = copyrights[0] + ' and ' + str(size - 1) + ' more'
        return result

    def _sentence(self, names):
        if len(names) == 1:
            return names[0]
        else:
            sentence = ' '.join(names[:-1])
            sentence += ' and ' + names[-1]
            return sentence

    def _normalize(self, name):
        name = re.sub('_\(.*\)', '', name) # replace _(...)
        name = name.replace('_', ' ')
        name = re.sub('[\\\/]', ' ', name) # replace / and \
        return name