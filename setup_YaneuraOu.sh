#!/bin/bash
set -eu

git clone https://github.com/yaneurao/YaneuraOu.git
cd YaneuraOu/source
make -j

wget https://github.com/Tama4649/Kristallweizen/raw/master/Kristallweizen_kaiV0.4.zip
unzip Kristallweizen_kaiV0.4.zip

mkdir -p book
cd $_
wget https://github.com/yaneurao/YaneuraOu/releases/download/BOOK-700T-Shock/700T-shock-book.zip
unzip 700T-shock-book.zip
wget https://github.com/yaneurao/YaneuraOu/releases/download/v4.73_book/standard_book.zip
unzip standard_book.zip
wget https://github.com/yaneurao/YaneuraOu/releases/download/v4.73_book/yaneura_book1_V101.zip
unzip yaneura_book1_V101.zip
wget https://github.com/yaneurao/YaneuraOu/releases/download/v4.73_book/yaneura_book3.zip
unzip yaneura_book3.zip
