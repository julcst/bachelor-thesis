# Computer Graphics Thesis Template

Version 2.0.1

Patrick Stotko (stotko@cs.uni-bonn.de)

## Requirements

Installed LaTeX distribution, e.g.:

- Linux : TeXLive
- Windows : MikTeX, TeXLive
- macOS : MacTeX

We use *pdflatex* and *biber* as the compilers for .tex and .bib files. Make sure that both are installed.

THERE IS NO GUARANTEE THAT THIS TEMPLATE ALSO WORKS WITH OTHER COMPILERS (BIBTEX WILL NOT WORK!).

## Structure

The template is divided into several modules:

- thesis.tex : The root file. It manages the overall structure of the thesis. Add packages or chapters, set the author, title, etc. BUT DO NOT REMOVE ANYTHING OR CHANGE THE OVERALL STRUCTURE OR PAGE ORDER

- figures : The directory into which all figures should be put in

- tex : The directory containing the remaining TeX files

    - chapter : Contains all your chapters
    
        - chapter{n}  : The n-th chapter of your Thesis. A new chapter can be added in thesis.tex through the \include function
        
    - abstract.tex : Contains the abstract
    
    - acknowledgement.tex : Contains the acknowledgements
    
    - literature.bib : Put all citations in here
    
    - macros.tex : Several predefined (mathematical) macros. DO NOT EDIT ANY MACROS. In case, you need to define additional ones, you are allowed to add them here
    
    - statutoryDeclaration : The statutory declaration that must be binded together with the Thesis. DO NOT EDIT THIS
    
    - style.tex : The configuration of the style. DO NOT EDIT ANY CONFIGURATION. However, you are allowed to add configurations for additional packages you need that DO NOT CONFLICT WITH THE EXISTING ONES
    
    - titlepage.tex : The title page. DO NOT EDIT THIS

## Building

You can compile this template using one of the following methods:

- Commandline:

    ```
    pdflatex thesis  
    biber thesis  
    pdflatex thesis  
    pdflatex thesis  
    ```

- TeXStudio (recommended)

    - Set pdflatex as the default TeX and biber as the default bibliography compiler in the settings
    - Compile thesis.tex (TexStudio will care about executing pdflatex and biber, SOMETIMES BUGGY AND MUST BE CALLED MANUALLY)

Any other TeX IDE will also work. Make sure it executes pdflatex and biber.

## Troubleshooting

In cases you have trouble using this template, check the following common problems:

- pdflatex complains about unknown option giveninits when loading biblatex --> Upgrade your biblatex package

If this does not solve your problem or you have questions, please contact the authors of this template.
