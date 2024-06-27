用于处理 https://data.baai.ac.cn/details/BAAI-IndustryCorpus 智源开源的行业预训练数据集

bash 下载链接:
源文件 1.4T,得下个几天

```
wget --header="Cookie: lastVisitedPage=https://hub.baai.ac.cn/; guidance-2024=yes; hubapi_session=eyJpdiI6Im10elo2U1ZuWkpIcGo4azVIcVVMamc9PSIsInZhbHVlIjoiOGdsNFZEY2Y2bndQVGFzSTBuUzdqM1dzOG9VblJYV242UkNMemdlKzBMdU04TmJCcC9uMko2MXZCb0tYbEg4cVFocnkxL3ZscGR6Y09Iajd3Y3IzeFg5SmZOTHJ6RE1DaStMR0g3SFAxV0MwcVgxU2k0ZUNISmRGRmYyMEpHU1EiLCJtYWMiOiI3YjlkMjVmNzQ0ZTFkOGQ5OTc0Yjg5YTIxMjI2NzFiMjE0NTU5ZDExNzE3NzI2ZTk5MDQyNDQwZjBkOGYwMjE1In0%3D" "https://resources.ks3-cn-beijing.ksyuncs.com/data/IndustryCorpus1_0/IndustryCorpus.tar?AccessKeyId=AKLTNasiLRBBTcOgPqzlkPzu1w&Expires=1719127593&Signature=NnbANTRIxipNJ7lfqS07ApOODLg%3D"
```

1. 解压

   `tar -xvf IndustryCorpus.tar`

2. 将中文的文件夹名字改成英文
3. unzip 中文文件夹下的所有文件

   `python3 unzip.py`

4.
