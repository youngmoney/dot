if !filereadable(expand('~/.vim/bundle/vundle/README.md'))
  !git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
  !vim +BundleInstall +qall
  qa
endif
set nocompatible
filetype off
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()
Bundle 'gmarik/vundle'


"Navigation
Bundle 'kien/ctrlp.vim'
Bundle 'djoshea/vim-autoread'
Bundle 'tpope/vim-eunuch'
Bundle 'kshenoy/vim-signature'
Bundle 'Valloric/ListToggle'

Bundle 'epeli/slimux'
Bundle 'christoomey/vim-tmux-navigator'

"Completion
"Bundle 'Valloric/YouCompleteMe'
Bundle 'SirVer/ultisnips'
Bundle 'honza/vim-snippets'
"Bundle 'sheerun/vim-polyglot'

"Whitespace and Characters
Bundle 'ntpeters/vim-better-whitespace'
Bundle 'vim-scripts/yaifa.vim'
Bundle 'Raimondi/delimitMate'
Bundle 'tpope/vim-surround'
Bundle 'tomtom/tcomment_vim'

"Text
Bundle 'vim-pandoc/vim-pandoc-syntax'
"Bundle 'junegunn/goyo.vim'
"Bundle 'vim-scripts/DrawIt'
Bundle 'dhruvasagar/vim-table-mode'

"So Crucial
filetype on
filetype plugin indent on
syntax on
set shellcmdflag=-ic
silent !mkdir -p ~/.vim/backup ~/.vim/swap >/dev/null 2>&1
set backupdir=~/.vim/backup//
set directory=~/.vim/swap//
set backspace=2
set tags=.tags;/ 
let mapleader=","
set laststatus=2

set statusline=%<\ %f\ %m%r%y%=%-35.(line:\ %l\ of\ %L,\ col:\ %c%V\ (%P)%)

map <leader>r :source ~/.vimrc <Return>
map <leader>i :source ~/.vimrc <Return> :BundleInstall<Return>:q<Return>
map <leader>u :source ~/.vimrc <Return> :BundleClean<Return>:BundleInstall<Return>:q<Return>

let g:ctrlp_extensions = ['tag']
autocmd Filetype crontab set backupcopy=yes

map <leader>b :execute "!git blame -L".line('.').",+3 ".expand("%")<return>

let g:ycm_path_to_python_interpreter = '/usr/bin/python'
let g:clang_exec = '/usr/local/bin/clang'
let g:clang_library_path = '/usr/local/lib/libclang.dylib'
let g:clang_library_path = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'
let g:ycm_collect_identifiers_from_tags_files = 1
let ycm_global_ycm_extra_conf = '~/local/scripts/~ycm_extra_conf.py'
let g:ycm_key_invoke_completion = '<C-Space>'
let g:ycm_error_symbol = '!'
let g:ycm_warning_symbol = '?'
let g:ycm_extra_conf_globlist = ['~/local/*','!~/*']
let g:ycm_filepath_completion_use_working_dir = 1
"let g:ycm_filetype_blacklist = { "tagbar": 1, "qf": 1,  "unite": 1, "text": 1, "vimwiki": 1, "infolog": 1 }
let g:EclimCompletionMethod = 'omnifunc'

let g:UltiSnipsExpandTrigger="<c-j>"
let g:UltiSnipsJumpForwardTrigger = g:UltiSnipsExpandTrigger
let g:UltiSnipsJumpBackwardTrigger = "<c-n>"
let g:ulti_expand_or_jump_res = 0 "default value, just set once
function! Ulti_ExpandOrJump_and_getRes()
    call UltiSnips#ExpandSnippetOrJump()
    return g:ulti_expand_or_jump_res
endfunction
inoremap <c-a> <C-R>=(Ulti_ExpandOrJump_and_getRes() > 0)?"":"\n"<CR>
set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*.d,*.o,*.class,build/*,*.pdf


"Slime
let g:slimux_select_from_current_window = 1
map <Leader>. :SlimuxREPLSendLine<CR>
map <Leader>> :SlimuxREPLSendBuffer<CR>
vmap <Leader>. :SlimuxREPLSendSelection<CR>

"Shortcuts
inoremap kj <Esc>
noremap kj <Esc>
map π :set paste<Return>i
map ¬ :set nu!<Return>
map ø :Obsession<Return>
map Ø :Obsession!<Return>
autocmd InsertLeave * set nopaste
map <Bslash> :noh<Return>
map ˙ :e %:p:s,.h$,.X123X,:s,.c$,.h,:s,.X123X$,.c,<CR>
map Ó :sp %:p:s,.h$,.X123X,:s,.c$,.h,:s,.X123X$,.c,<CR>
set updatetime=5

let g:tagbar_autoclose = 1

"Colors
set vb "t_vb
colo slate
set cursorline
set hlsearch
autocmd Filetype text set ft=pandoc
autocmd Filetype pandoc set cursorline!
autocmd WinEnter * setlocal cursorline
autocmd WinLeave * setlocal nocursorline
set fillchars+=vert:\ 
set titlestring=%t%(\ %M%)%(\ (%{expand(\"%:p:h\")})%)%(\ %a%)\ -\ %{v:servername}
set title

"Tabs
set expandtab
set shiftwidth=4
set smartindent
set smarttab

"Markdown
let g:grammerOn = 0
function! ToggleGrammer()
  if g:grammerOn
    g:grammerOn = 0
    LanguageToolClear
  else
    g:grammerOn = 1
    LanguageToolCheck
  endif
endfunction
let g:languagetool_jar='/usr/local/Cellar/languagetool/2.8/libexec/languagetool-commandline.jar'

"autocmd Filetype mail exe "normal iThanks,Taylorkjgg"

autocmd Filetype markdown set updatetime=50
autocmd Filetype markdown map ß :set spell!<Return>
autocmd Filetype markdown map © call ToggleGrammer()
"autocmd Filetype markdown Goyo
map ƒ :Goyo<return>
let autoreadargs={'autoread':1}
autocmd Filetype markdown execute WatchForChanges("*",autoreadargs)
"autocmd Filetype markdown map Ó yypVr=
"autocmd Filetype markdown map ˙ yypVr-
autocmd Filetype markdown syntax match mdReminder "<!--+.*-->"
autocmd Filetype markdown highlight link mdReminder Todo
autocmd Filetype markdown syntax match mdTodo "<!---.*-->"
autocmd Filetype markdown highlight link mdTodo Todo
autocmd Filetype markdown syntax match mdAlert "<!--.*!.*-->"
autocmd Filetype markdown highlight link mdAlert Error
autocmd Filetype markdown syntax match mdMath "\$\_.\{-}\$"
autocmd Filetype markdown highlight link mdMath Structure
autocmd Filetype markdown set textwidth=80
autocmd Filetype markdown syntax match mdBudget "^\(in\|tx\|bg\|ex\) .*$"
autocmd Filetype markdown highlight link mdBudget Ignore
highlight nonascii guibg=Red ctermbg=1 term=standout
au BufReadPost * syntax match nonascii "[^\u0000-\u007F]"
map <leader>s ]s
map <leader>z 1z=

let g:table_mode_corner_corner='+'
let g:table_mode_corner='+'

"Building
function! ShowErrors()
  :cclose
  if len(getqflist()) > 0 && g:projectType == ""
    :copen
  endif
endfunction


map ∫ :make<Return>:call ShowErrors()<Return>
map ® :make run -s<Return>:call ShowErrors()<Return>
map ç :make check -s<Return>:call ShowErrors()<Return>
map <S-Left> :cprevious<Return>
map <S-Right> :cnext<Return>

let g:projectType = ""
if filereadable(".classpath")
  let g:projectType = "Java"
endif

if filereadable("AndroidManifest.xml")
  let g:projectType = "Android"
endif

if filereadable("Procfile")
  let g:projectType = "Heroku"
endif

if len(glob("*.xcworkspace")) || len(glob("*.xcodeproj"))
  let g:projectType = "xCode"
endif
autocmd BufRead,BufNewFile .cron set ft=crontab

autocmd Filetype java set errorformat=%A%f:%l:\ %m,%-Z%p^,%-C%.%#

if g:projectType == ""
  autocmd Filetype java set makeprg=javac\ %
  autocmd Filetype python map ∫ :w<Return>:!python %<Return>
  autocmd Filetype python map ® :w<Return>:!python %<Return>
  autocmd Filetype ruby map ∫ :w<Return>:!ruby %<Return>
  autocmd Filetype ruby map ® :w<Return>:!ruby %<Return>
  autocmd Filetype markdown map ® :w<Return>:execute "!build markdown -o %"<Return><Return>
  autocmd Filetype markdown map ∫ :w<Return>:execute "!build markdown -o %"<Return>
  autocmd Filetype rmd map ® :w<Return>:execute "!R -e \"rmarkdown::render('%','pdf_document')\""<Return><Return>
  autocmd Filetype rmd map ∫ :w<Return>:execute "!R -e \"rmarkdown::render('%')\""<Return><Return>
  autocmd Filetype r map ® :w<Return>:execute "!R -e \"library(knitr); knitr::stitch('%')\""<Return><Return>
  autocmd Filetype r map ∫ :w<Return>:execute "!R -e \"library(knitr); knitr::stitch('%')\""<Return><Return>
endif

if g:projectType == "xCode"
  map ∫ :w<Return>:!build xcode<Return>
  map ® :w<Return>:!build xcode<Return>

  let g:ycm_semantic_triggers = {
 \ 'objc' : ['re!\@"\.*"\s',
 \ 're!\@\w+\.*\w*\s',
 \ 're!\@\(\w+\.*\w*\)\s',
 \ 're!\@\(\s*',
 \ 're!\@\[.*\]\s',
 \ 're!\@\[\s*',
 \ 're!\@\{.*\}\s',
 \ 're!\@\{\s*',
 \ "re!\@\’.*\’\s",
 \ '#ifdef ',
 \ 're!:\s*',
 \ 're!=\s*',
 \ 're!,\s*', ],
 \ }
"let tlist_objc_settings    = 'objc;i:interface;c:class;m:method;p:property'
let g:ycm_filetype_specific_completion_to_disable = {
      \ 'objc': 1
      \}
endif

if g:projectType == "Android"
  map ∫ :w<Return>:!build droid debug $ACTIVITY<Return>
  map ® :w<Return>:!build droid log $ACTIVITY<Return>
endif

if g:projectType == "Java"
  map ∫ :w<Return>:Java<Return>
  map ® :w<Return>:Java<Return>
endif

if g:projectType == "Heroku"
"  map ∫ :w<Return>:!foreman start<Return>
  map ® :w<Return>:!foreman start<Return>
  let g:projectType = ""
endif

if g:projectType == "Fake For XVim"
  map ∫ :make
  map ® :run
endif
