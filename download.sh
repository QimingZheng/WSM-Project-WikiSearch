mkdir data/
mkdir data/raw
mkdir data/parsed
mkdir data/index

cd data/raw

for i in https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles1.xml-p1p162886.bz2 #,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles2.xml-p162887p544644.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles3.xml-p544645p1154617.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles4.xml-p1154618p2654617.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles4.xml-p2654618p2771086.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles5.xml-p2771087p4271086.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles5.xml-p4271087p4731439.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles6.xml-p4731440p6231439.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles6.xml-p6231440p6993503.bz2,https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles6.xml-p6231440p7018650.bz2};
do
    wget $i
done


bzip2 -d *.bz2

for i in *;
do 
    python ../../wikisearch/deps/wikiextractor/WikiExtractor.py --json $i
done

mv */ ../parsed/
