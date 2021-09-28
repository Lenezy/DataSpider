from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 爬取网页
    datalist = getData(baseurl)

    savepath = "doubanmovie250.xls"
    # 保存数据
    saveData(datalist, savepath)

    # askURL("https://movie.douban.com/top250?start=")start


# 影片详情的规则
findLink = re.compile(r'<a href="(.*?)">')  # 創建正則表達式對象，表示规则（字符串模式）
# 影片图片
findImg = re.compile(r'<img .*src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):

    global html
    datalist = []
    for i in range(0, 25):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
        # print(item)  # 测试查看电影item全部信息
        data = []  # 保存一部電影的所有信息
        item = str(item)

        # 影片详情链接
        link = re.findall(findLink, item)[0]  # re庫用來通過正則表達式查找制定的字符串,[0]列表拿第一个
        data.append(link)  # 添加链接

        imgSrc = re.findall(findImg, item)[0]
        data.append(imgSrc)  # 添加图片

        titles = re.findall(findTitle, item)  # 片名可能只有一个中文名
        if len(titles) == 2:
            chineseTitle = titles[0]
            data.append(chineseTitle)  # 添加中文名
            otitle = titles[1].replace("/", "")  # 去掉无关符号
            data.append(otitle)  # 添加外文名
        else:
            data.append(titles[0])
            data.append('')  # 外文名留空

        rating = re.findall(findRating, item)[0]
        data.append(rating)  # 添加评分

        judgeNum = re.findall(findJudge, item)[0]
        data.append(judgeNum)  # 评价人数

        inq = re.findall(findInq, item)
        if len(inq) != 0:
            inq = inq[0].replace("。", "")  # 去掉中文句号
            data.append(inq)  # 添加概述
        else:
            data.append(" ")  # 留空

        bd = re.findall(findBd, item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)  # 去掉<br/>
        bd = re.sub('/', " ", bd)  # 替换
        data.append(bd.strip())  # 去掉前后空格

        datalist.append(data)  # 把处理好的一部电影信息放入datalist

    # print(datalist) 打印datalist

    return datalist


def askURL(url):
    # 模拟浏览器头部信息，向豆瓣服务器发送信息
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.63 Safari/537.36",
        "Referer": "https://open.weixin.qq.com/",
        "sec-ch-ua": '"Google Chrome";v = "93", " Not;A Brand";v = "99", "Chromium";v = "93"',
        "sec - ch - ua - mobile": "?0",
        "sec - ch - ua - platform": '"macOS"',
        "Sec - Fetch - Dest": "document",
        "Sec - Fetch - Mode": "navigate",
        "Sec - Fetch - Site": "cross - site",
        "Upgrade - Insecure - Requests": "1"
    }
    # 用户代理表示告诉豆瓣我们是什么浏览器（本质上是告诉浏览器我们能接受什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('doubanmovieTop250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for n in range(0, 8):
        sheet.write(0, n, col[n])  # 列名
    for i in range(0, 2):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存数据表


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    print("爬取完毕！")
