# =============================================================================
# FILE: deoplete_padawan.py
# AUTHOR: Pawel Bogut
# Based on:
#   https://github.com/mkusher/padawan.vim
#   https://github.com/zchee/deoplete-jedi
# =============================================================================

from .base import Base
from os import path
from urllib.error import URLError
from socket import timeout
import sys
import re
import logging as logger

sys.path.insert(1, path.dirname(__file__) + '/deoplete_padawan')

import padawan_server  # noqa

logger.basicConfig(level=logger.INFO)

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'padawan'
        self.mark = '[padawan]'
        self.filetypes = ['php']
        self.rank = 500
        self.input_pattern = r'\w+|[^. \t]->\w*|\w+::\w*|' \
                             r'\w\([\'"][^\)]*|\w\(\w*|\\\w*|\$\w*'
        self.current = vim.current
        self.vim = vim

    def on_init(self, context):
        server_addr = self.vim.eval(
            'deoplete#sources#padawan#server_addr')
        server_command = self.vim.eval(
            'deoplete#sources#padawan#server_command')
        log_file = self.vim.eval(
            'deoplete#sources#padawan#log_file')
        self.add_parentheses = self.vim.eval(
            'deoplete#sources#padawan#add_parentheses')

        self.server = padawan_server.Server(server_addr, server_command,
                                            log_file)

    def get_cursor_column(self, context):
        if self.current.window.cursor is tuple:
            return self.current.window.cursor[1]
        return len(context['input'])

    def get_complete_position(self, context):
        cursor_col = self.get_cursor_column(context)
        input = context['input']
        if cursor_col < len(input):
            logger.debug('using cursor column')
            # not at the end of line
            return cursor_col
        patterns = [
            r'(?:.*)::$|::(?=[_a-zA-Z][_\w]*$)', # static method/prop
            r'(?:.*)->$|->(?=[_a-zA-Z][_\w]*$)', # instance method/prop
            r'(?:.*)\\$|\\(?=[_a-zA-Z][_\w]*$)', # namespace
            r'(?:.*)\$$|\$(?=[_a-zA-Z][_\w]*$)', # variable
            r'(?:.*)[_\w]+\s*?\((?=.*?)',      # method/function call
        ]
        pos = self.get_patterns_position(context, patterns)
        if pos < 0:
            logger.debug('No match')
            return len(input)
        if pos in range(len(input)):
            if input[pos] == '\\':
                pos += 1
            elif input[pos] == '(':
                pos -= 1
        return pos

    def get_padawan_column(self, context):
        return self.get_complete_position(context) + 1

    def get_patterns_position(self, context, patterns):
        result = -1
        logger.debug('Matching in %s', context['input'])
        for pattern in patterns:
            logger.debug('Using pattern %s', pattern)
            m = re.search(pattern, context['input'])
            if m and m.end() > result:
                result = m.end()
        return result

    def gather_candidates(self, context):
        file_path = self.current.buffer.name
        current_path = self.get_project_root(file_path)

        [line_num, _] = self.current.window.cursor
        column_num = self.get_padawan_column(context)

        contents = "\n".join(self.current.buffer)

        params = {
            'filepath': file_path.replace(current_path, ""),
            'line': line_num,
            'column': column_num,
            'path': current_path
        }
        result = self.do_request('complete', params, contents)

        candidates = []

        if not result or 'completion' not in result:
            return candidates

        for item in result['completion']:
            candidate = {'word': self.get_candidate_word(item),
                         'abbr': self.get_candidate_abbr(item),
                         'kind': self.get_candidate_signature(item),
                         'info': item['description'],
                         'dup': 1}
            candidates.append(candidate)

        return candidates

    def get_candidate_abbr(self, item):
        if 'menu' in item and item['menu']:
            abbr = item['menu']
        else:
            abbr = item['name']

        return abbr

    def get_candidate_word(self, item):
        signature = self.get_candidate_signature(item)
        name = item['name']
        if self.add_parentheses != 1:
            return name
        if signature.find('()') == 0:
            return name + '()'
        if signature.find('(') == 0:
            return name + '('

        return name

    def get_candidate_signature(self, item):
        signature = item['signature']
        if not signature:
            signature = ''

        return signature

    def do_request(self, command, params, data=''):
        try:
            return self.server.sendRequest(command, params, data)
        except URLError:
            if self.vim.eval('deoplete#sources#padawan#server_autostart') == 1:
                self.server.start()
                self.vim.command(
                    "echom 'Padawan.php server started automatically'")
            else:
                self.vim.command("echom 'Padawan.php is not running'")
        except timeout:
            self.vim.command("echom 'Connection to padawan.php timed out'")
        except ValueError as error:
            self.vim.command("echom 'Padawan.php error: {}'".format(error))
        # any other error can bouble to deoplete
        return False

    def get_project_root(self, file_path):
        current_path = path.dirname(file_path)
        while current_path != '/' and not path.exists(
                path.join(current_path, 'composer.json')
        ):
            current_path = path.dirname(current_path)

        if current_path == '/':
            current_path = path.dirname(file_path)

        return current_path
