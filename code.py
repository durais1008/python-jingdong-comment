import requests
import pandas as pd
import time


def get_jd_comments(product_id, max_comments=500):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    comments = []
    page = 0
    while len(comments) < max_comments:
        page += 1
        url = f'https://club.jd.com/comment/productPageComments.action?productId={product_id}&score=0&sortType=5&page={page}&pageSize=10'
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            for comment in data['comments']:
                comments.append({
                    'content': comment['content'],
                    'creationTime': comment['creationTime'],
                    'score': comment['score']
                })
                if len(comments) >= max_comments:
                    break
            time.sleep(2)  # 避免高频请求
        except Exception as e:
            print(f'第{page}页出错：{e}')
            break

    df = pd.DataFrame(comments)
    df.to_excel(f'jd_comments_{product_id}.xlsx', index=False)
    print(f'已保存{len(comments)}条评论')


# 使用：替换product_id为商品ID（从商品URL获取）
get_jd_comments(product_id='100087064005', max_comments=500)  # 爬取500条评论