## 巨潮资讯网 PDF爬虫 & PDF解析

1. 爬虫爬取下载巨潮资讯网指定公司的年报PDF，以及招股意向（说明）文件PDF
2. 解析PDF中的文字和图片，获取keywords列表中指定关键字的出现频数

## Structure

    spider.py           爬虫
    pdf2txt.py          爬虫所得PDF批量转txt
    main.py             统计keywords列表中每个关键字频数
    extract_text.js     指定PDF转txt
    quick_start.py      快速下载指定公司年报
    keywords.txt        需要统计的关键字列表
    company_id.txt      需要爬取PDF的公司stock代码列表

## Installation

### Python Dependencies

```bash
pip install requests xlwt PyPDF2
```

### Node.js Dependencies

```bash
npm install pdf-text-extract
```

## Usage

### Quick Start - Download Single Company Reports

```bash
python quick_start.py <stock_code>
```

Example:

```bash
python quick_start.py 000888   # 峨眉山旅游
```

### Full Workflow

First, set `keywords.txt` and `company_id.txt` if u need more keywords for statistic or more company to crawl on cninfo.

```
python spider.py        # put PDF files in /pdf directory
python pdf2txt.py       # then covert all /pdf into /txt
python main.py          # make statistics
```

Output Excel files will be saved in `/xls` directory.

## Remark

### Why extract_text.JS?

Some bugs occurred when using PDFMiner & PyPDF2 for extracting text, cause some compression of images seems illegal for those wheels. And both libraries run too slow. So I pick the JS library instead which is enough for text only extracting demand and also works out faster.

```
# Usage of extract_text.js
node extract_text.js pdf_input_path txt_output_path
```

### Spider Details

Query format:

    column: szse                    # 深交所
            sse                     # 沪交所
    plate:  sz                      # 深圳，对应深交所
            sh                      # 上海，对应沪交所
    category:
            (empty)                 # 搜索其他报文，如招股意向，此时配合searchkey检索
            category_ndbg_szsh      # 年报板块

**Important**: The API has been updated. Use `searchkey` parameter instead of `stock` parameter.

```python
# Updated query method (2026)
def szseAnnual(page, stock):
    query_path = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    headers['User-Agent'] = random.choice(User_Agent)
    query = {'pageNum': page,
             'pageSize': 30,
             'tabName': 'fulltext',
             'column': 'szse',  # 深交所
             'stock': '',       # ← Keep empty
             'searchkey': stock,  # ← Use searchkey instead
             'secid': '',
             'plate': 'sz',
             'category': 'category_ndbg_szsh',  # 年度报告
             'trade': '',
             'seDate': '2020-01-01~2026-02-15'  # Updated date range
             }

    namelist = requests.post(query_path, headers=headers, data=query)
    result = namelist.json()
    if result and 'announcements' in result and result['announcements']:
        return result['announcements']
    return []

```
