import os
import sys
import re
import json
import csv
import urllib.request
import codecs

client_id = "UWVUkNseKo37aoyl40Uy"
client_secret = "uPP2aapn6Y"
search_keyword = "데이트하기 좋은 곳"  # 검색할 키워드 설정
category = "데이트"  # 키워드에 대한 카테고리, 1열에 넣을 카테고리
result_list = []  # 검색 결과 저장 리스트
encText = urllib.parse.quote(search_keyword)

for start in range(1, 1001, 100):
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=100" + "&sort=sim" + "&start=" + str(
        start)
    print(url)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        text_data = response_body.decode('utf-8')
        json_data = json.loads(text_data)
        for x in json_data['items']:
            result = re.sub('<.+?>', '', x['title'], 0, re.I | re.S)  # 제목만 저장
            result = re.sub('[^ ㄱ-ㅣ가-힣]+', '', result)
            result_list.append(result)  # 리스트에 추가
    else:
        print("Error Code:" + rescode)

file = open(search_keyword + '.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(file)
for i in range(0, len(result_list)):
    wr.writerow([category, result_list[i]])  # 여기에 category 가 키워드에 대한 카테고리임

file.close()

# csv 파일 인코딩 변환

infile = codecs.open(search_keyword + '.csv', 'r', encoding='utf-8')
outfile = codecs.open(search_keyword + 'kr.csv', 'w', encoding='euc-kr')

for line in infile:
    line = line.replace(u'\xa0', ' ')  # 가끔 \xa0 문자열로 인해 오류가 발생하므로 변환
    outfile.write(line)

infile.close()
outfile.close()
os.remove(search_keyword + '.csv')  # 원본 csv 파일 삭제
os.rename(search_keyword + 'kr.csv', search_keyword + '.csv')  # 인코딩 변환 파일 이름 바꾸기
