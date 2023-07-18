#!/usr/bin/python3
import os
import sys
import time
import subprocess as sbpr

litcode_sty_content = r'''
\RequirePackage[T1]{fontenc}
\usepackage{amsmath}
\RequirePackage{textcomp}
%\RequirePackage{inconsolata}
\RequirePackage{calc}
\RequirePackage{caption}
\RequirePackage{hyperref}
\RequirePackage{cleveref}

\RequirePackage{fancyvrb}
\RequirePackage{listings}
\RequirePackage{xcolor}

\RequirePackage{xparse}
\RequirePackage{subcaption}
\def\litcode{{LitCode}}
\def\linewidth{\textwidth}

\def\xleftmargin{10pt}
\def\xrightmargin{0pt}

\def\litcodefont{\fontfamily{SourceCodePro-TLF}\small}
\def\codebg{yellow!15}
\def\vcodebg{green!20}

\hypersetup{
    colorlinks=true,
    linkcolor=red,
    urlcolor=red,
    citecolor=red
}

\urlstyle{same}
% Define code environment: Used when defining a chunk for the first time
\lstnewenvironment{code}[1][]{
    \lstset{
        caption={\protect\detokenize{#1}},
        label={#1},
        columns=fullflexible,
        basicstyle=\litcodefont,
        keepspaces=true,
        breaklines=true,
        upquote=true,
        backgroundcolor=\color{\codebg},
        escapeinside={@<}{@>}
    }
}{}

% Define oldcode environment: To be used when extending an already defined chunk
\lstnewenvironment{oldcode}[1][]{
    \lstset{
        columns=fullflexible,
        basicstyle=\litcodefont,
        keepspaces=true,
        breaklines=true,
        upquote=true,
        backgroundcolor=\color{\codebg},
        escapeinside={@<}{@>}
    }
}{}
% Verbatim code environment: Takes no captions, has no labels and won't get included in the listing. 
% Purely verbatim!!
\lstnewenvironment{vcode}[1][]{
    \lstset{
        columns=fullflexible,
        basicstyle=\litcodefont,
        keepspaces=true,
        breaklines=true,
        upquote=true,
        backgroundcolor=\color{\vcodebg},
    }
}{}
\DeclareCaptionFormat{codecaptionformat}
{
    \phantom{$\langle\textit{#3}\rangle\!\!\equiv$}
}

\captionsetup[lstlisting]{
    format=codecaptionformat,
    justification=raggedright,
    singlelinecheck=off,
    skip=-\baselineskip
}

\makeatletter
\renewcommand\l@lstlisting[2]{\@dottedtocline{1}{0em}{2.3em}{\textit{#1}}{#2}}
\makeatother

\newcommand{\coderef}[1]{$\langle$\textit{\nameref{#1}}$\rangle$}
%\newcommand{\coderef}[1]{$\langle$\textit{\nameref{#1}} \rm(p.~\pageref{#1})$\rangle$}
'''

def main():
    global litcode_sty_content
    if len(sys.argv) <= 1:
        print('Please supply a directory name')
        exit(1)
    directory = sys.argv[1]
    command = f'mkdir -p {directory}'
    os.system(command)
    full_path_to_sty = f'{directory}{os.sep}litcode.sty'
    with open(full_path_to_sty, 'w') as fp:
        fp.writelines(litcode_sty_content)

main()

