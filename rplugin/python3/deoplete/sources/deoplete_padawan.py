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

sys.path.insert(1, path.dirname(__file__) + '/deoplete_padawan')

import padawan_server  # noqa
import padawan_helper  # noqa


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.helper = padawan_helper.Helper()
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
        self.auto_update = self.vim.eval(
            'deoplete#sources#padawan#auto_update')

        self.server = padawan_server.Server(server_addr, server_command,
                                            log_file)

    def on_event(self, context):
        if (context['event'] == 'BufWritePost' and self.auto_update == 1):
            file_path = self.current.buffer.name
            current_path = self.helper.get_project_root(file_path)
            params = {
                'path': current_path
            }
            self.do_request('update', params)

    def get_complete_position(self, context):
        patterns = [r'[\'"][^\)]*$', r'[\w\\]*$']
        input = context['input']
        pos = self.get_patterns_position(context, patterns)
        if pos in range(len(input)) and input[pos] == '\\':
            pos = pos + 1
        return pos

    def get_padawan_column(self, context):
        patterns = [r'(?<=[\s\(\=])\w+$|^\w+$']
        pos = self.get_patterns_position(context, patterns)
        if pos == context['complete_position']:
            return pos + 2
        return context['complete_position'] + 1

    def get_patterns_position(self, context, patterns):
        result = -1
        result_end = -1
        pos = -1
        for pattern in patterns:
            m = re.search(pattern, context['input'])
            if m:
                pos = m.start()
                pos_end = m.end()
            # match new pattern only if previous one ended before this one
            if pos > result_end:
                result = pos
                result_end = pos_end

        return result

    def gather_candidates(self, context):
        file_path = self.current.buffer.name
        current_path = self.helper.get_project_root(file_path)

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
                         'info': self.get_candidate_info(item),
                         'dup': 1}
            candidates.append(candidate)

        return candidates

    def get_candidate_info(self, item):
        abbr = self.get_candidate_abbr(item)
        signature = self.get_candidate_signature(item)

        return abbr + signature

    def get_candidate_abbr(self, item):
        if 'menu' in item and item['menu']:
            abbr = item['menu']
        else:
            abbr = item['name']

        return abbr

    def get_candidate_word(self, item):
        signature = self.get_candidate_signature(item)
        name = self.get_candidate_abbr(item)
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
