# deoplete-padawan

[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.org/padawan-php/deoplete-padawan.svg?branch=master)](https://travis-ci.org/padawan-php/deoplete-padawan)

[deoplete.nvim](https://github.com/Shougo/deoplete.nvim) source for
[padawan.php](https://github.com/mkusher/padawan.php).

Deoplete-padawan offers asynchronous completion of code written in PHP using
[padawan.php](https://github.com/mkusher/padawan.php) and
[deoplete.nvim](https://github.com/Shougo/deoplete.nvim).

It requires [neovim](https://github.com/neovim/neovim) as deoplete requires it.

## Demo

![demo](https://raw.githubusercontent.com/padawan-php/deoplete-padawan/master/demo.gif)
![demo2](https://raw.githubusercontent.com/padawan-php/deoplete-padawan/master/demo2.gif)

## Installation

You need to install [padawan.php](https://github.com/mkusher/padawan.php) and
index your project. The plugin requires padawan.php server running to work.

To install server within the plugin directory you can run
```
`:call deoplete#sources#padawan#InstallServer()`
```
It will install the padawan.php server in the plugin directory.
To update server run
```
`:call deoplete#sources#padawan#UpdateServer()`
```
Composer needs to be in your system path in order to install or update server.


Using [vim-plug](https://github.com/junegunn/vim-plug):
```vim
Plug 'Shougo/deoplete.nvim'

Plug 'padawan-php/deoplete-padawan', { 'do': 'composer install' }
```

Using [Vundle](https://github.com/VundleVim/Vundle.vim):
```vim
Plugin 'Shougo/deoplete.nvim'

Plugin 'padawan-php/deoplete-padawan'
```

## Configuration

The plugin requires no configuration. However, it is possible to change some
options.

### Available settings

| Variable                                      | Default                   |
|:----------------------------------------------|:--------------------------|
| `g:deoplete#sources#padawan#server_addr`      | `http://127.0.0.1:15155`  |
| `g:deoplete#sources#padawan#server_command`   | `padawan-server`          |
| `g:deoplete#sources#padawan#composer_command` | `composer`                |
| `g:deoplete#sources#padawan#log_file`         | `/tmp/padawan-server.log` |
| `g:deoplete#sources#padawan#server_autostart` | `1`                       |
| `g:deoplete#sources#padawan#add_parentheses`  | `0`                       |
| `g:deoplete#sources#padawan#auto_update`      | `0`                       |

- `g:deoplete#sources#padawan#server_addr`

Address to padawan.php server. By default, it is `http://127.0.0.1:15155`

- `g:deoplete#sources#padawan#server_command`

If your padawan-server bin is not in $PATH then you can set up this
to point it directly, ie: `/path/to/padawan/bin/padawan-server`.

- `g:deoplete#sources#padawan#composer_command`

Composer is used to install and update the padawan.php server in the plugin
directory.  If `composer` is not in your system path you can set full command
directly, ie: `php ~/bin/composer.phar`.

- `g:deoplete#sources#padawan#log_file`

Padawan.php log file path, if empty log won't be stored anywhere. By default, it goes
to `/tmp/padawan-server.log` unless you have no `/tmp` directory, in that case
log won't be saved.

- `g:deoplete#sources#padawan#server_autostart`

The plugin will try to start padawan.php server automatically when completion is triggered.
Any value but `1` will make this option disabled.

- `g:deoplete#sources#padawan#add_parentheses`

If set to `1` parentheses will be added to function (method) completion. If function
accepts parameters, only opening parenthesis will be added.

- `g:deoplete#sources#padawan#auto_update`
If set to `1` send `update` command to server automatically when `BufWritePost` event is triggered.

## Additional commands

By default, the plugin is not creating any vim commands. However, there are some
functions available to manage the padawan.php server.

- `call deoplete#sources#padawan#StartServer()`

Will start padawan-server.

- `call deoplete#sources#padawan#StopServer()`

Will kill padawan-server.

- `call deoplete#sources#padawan#RestartServer()`

Will kill padawan-server and start it again.

- `call deoplete#sources#padawan#InstallServer()`

Will install padawan.php server.

- `call deoplete#sources#padawan#UpdateServer()`

Will update padawan.php server.

- `call deoplete#sources#padawan#Generate()`

Will generate index file for current project. Command will run as neovim job,
if you would like to see the output you can pass 1 as an argument to this
function.

### Custom commands

If you would like to have simpler commands, you can add them to your
`vimrc` file. Snippet below shows how to add commands.

```vim
command! PadawanStart call deoplete#sources#padawan#StartServer()
command! PadawanStop call deoplete#sources#padawan#StopServer()
command! PadawanRestart call deoplete#sources#padawan#RestartServer()
command! PadawanInstall call deoplete#sources#padawan#InstallServer()
command! PadawanUpdate call deoplete#sources#padawan#UpdatePadawan()
command! -bang PadawanGenerate call deoplete#sources#padawan#Generate(<bang>0)
```

## Compatibility with other plugins

### echodoc.vim

This plugin is compatible with [echodoc.vim](https://github.com/Shougo/echodoc.vim).

**Note**: If you change `g:deoplete#sources#padawan#add_parentheses` from default `0` to `1`, you have to add `$` to deoplete's `skip_chars`.
Otherwise the popup menu which is triggered after you type `$` will disable echodoc's functionality.

Examples of working setups:

```vim
let g:deoplete#sources#padawan#add_parentheses = 0
```

or

```vim
let g:deoplete#sources#padawan#add_parentheses = 1
let g:deoplete#skip_chars = ['$']
```

## Todo
- [x] Update configuration section
- [x] Provide actions to start and stop padawan.php server
- [ ] Add Vim help file

## Contribution

Always welcome.

## Credits

Plugin is based on [padawan.vim](https://github.com/mkusher/padawan.vim),
[deoplete-jedi](https://github.com/zchee/deoplete-jedi) and
[deoplete-go](https://github.com/zchee/deoplete-go).

## License

MIT License;
The software is provided "as is", without warranty of any kind.
