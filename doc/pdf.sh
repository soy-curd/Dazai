rm book.pdf
rm preface.re
rm chap01.re
rm -r book-pdf
md2review src/preface.md > preface.re
md2review src/chap01.md > chap01.re
md2review src/chap02.md > chap02.re
md2review src/chap03.md > chap03.re


review-pdfmaker config.yml
open book.pdf
