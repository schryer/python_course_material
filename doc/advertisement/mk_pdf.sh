#!/bin/bash
RST_F=$1".rst"
TEX_F=$1".tex"
PDF_F=$1".pdf"
LOG_F=$1".log"
AUX_F=$1".aux"
OUT_F=$1".out"

TILDE_F="*~"
HTML_F=$1".html"

CLEAN=$2

LATEX_PREAMBLE="\usepackage{geometry}
\geometry{a4paper,textwidth=400pt,textheight=650pt}
\usepackage{libertineotf}"

echo "Converting" $RST_F
rst2xetex --latex-preamble "$LATEX_PREAMBLE" $RST_F> $TEX_F && xelatex $TEX_F

echo "Executing: mv" $PDF_F Data_Analysis_for_Scientists_and_Engineers_June_2013.pdf
mv $PDF_F Data_Analysis_for_Scientists_and_Engineers_June_2013.pdf
#rst2html $RST_F>$HTML_F

if $CLEAN; then
echo "Cleaning up XeLaTeX files."
rm $TEX_F $LOG_F $AUX_F $OUT_F $TILDE_F 
fi
