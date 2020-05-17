mkdir data/
mkdir data/raw
mkdir data/parsed
mkdir data/index

cd data/raw


# wget http://download.wikipedia.com/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2

# bzip2 -d *.bz2

for i in *;
do 
    python ../../wikisearch/deps/wikiextractor/WikiExtractor.py -b32M --json $i
done

mv */ ../parsed/
