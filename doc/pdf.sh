rm book.pdf
rm -r book-pdf
md2review src/preface.md > preface.re
md2review src/chap01.md > chap01.re
review-pdfmaker config.yml
