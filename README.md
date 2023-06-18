# Bài tập lớn số 2 - Nhập môn khoa học dữ liệu - Nhóm 2 - Lớp NMKHDL.1_K3N2_2223

## Thành viên

| Thành viên               | Phân công công việc                       | Mức độ hoàn thành |
| ------------------------ | ----------------------------------------- | ----------------- |
| A42718 - Lê Thảo Quyên   | Bản dịch Tiếng Việt, Hiệu đính Slide                       | 100%              |
| A41316 - Nguyễn Hữu Khoa | Thực hiện Slide tóm tắt, ghi chép và chuyển đổi mã nguồn | 100%              |

## Các file báo cáo

1. [Bản dịch Tiếng Việt](chapter7_vi.pdf)
2. [Slide tóm tắt](slide/Chapter7_summary.pdf)
3. File mã nguồn được lưu trong thư mục [src](src/) gồm:
   - [python2](src/python2/): là file mã nguồn gốc được lấy từ sách
   - [python3](src/python3/): là file mã nguồn đã được chuyển đổi cú pháp sang python3
     - [Data_Preparation_1.ipynb](src/python3/Data_Preparation_1.ipynb): Chuẩn bị dữ liệu tải dữ liệu lên Elasticsearch
     - [Data_Preparation_2.ipynb](src/python3/Data_Preparation_2.ipynb): Chuẩn bị dữ liệu: Chuyển dữ liệu từ Elasticsearch sang Neo4j
     - [Exploration_n_Recommendation.ipynb](src/python3/Exploration_n_Recommendation.ipynb): Khám phá dữ liệu và đề xuất món ăn

4. Chương cung cấp gồm 3 file dữ liệu:
   - Ingerdients.txt: Chứa tên các nguyên liệu
   - Recipes.json: Chứa công thức nấu ăn
   - Elasticsearch index.zip: Bao gồm 'gastronomical' Elasticsearch index để bạn có thể bỏ qua bước chuẩn bị dữ liệu [phần 1](src/python3/Data_Preparation_1.ipynb) mà vẫn có thể tiếp tục với bước chuẩn bị dữ liệu [phần 2](src/python3/Data_Preparation_2.ipynb)

## Các thay đổi của mã nguồn so với sách gốc

Do có sự cập nhật về cả python cũng như các thư viện, code cũ trong sách đã không còn có thể chạy được nếu không thực hiện một số thay đổi. Dưới đây là các lưu ý về thay đổi của mã nguồn so với sách gốc (chỉ liệt kê đối với 2 thư viện chính là `py2neo` và `elasticsearch`)

1. Sử dụng `NodeMatcher` thay cho `merge_one`: Trong Py2neo phiên bản 3, phương thức `merge_one` đã được gỡ bỏ. Thay vào đó, bạn có thể sử dụng lớp `NodeMatcher` để thực hiện các thao tác tương tự. Ví dụ:

   - Python 2: `graph_db.merge_one(label, property_key, property_value)`

   - Python 3: `matcher.match(label, property_key=property_value).first()`

2. Loại bỏ tham số `doc_type` trong `client.search`: Trong phiên bản Elasticsearch 7.x, tham số `doc_type` đã bị loại bỏ và thay thế bằng đối tượng `Document`. Do đó, bạn chỉ cần xóa tham số `doc_type` khỏi cuộc gọi `client.search`. Ví dụ:

   - Python 2: `client.search(index=indexName, doc_type=docType, body=searchbody)`

   - Python 3: `client.search(index=indexName, body=searchbody)`

3. Kể từ ES8, SSL/TLS được BẬT theo mặc định cho các máy khách HTTP. Để có thể sử dụng `elasticsearch` ta cần tắt SSL trong cấu hình `elaticsearch.yml` như sau:

```yml
# Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
xpack.security.http.ssl:
  enabled: false
  keystore.path: certs/http.p12

# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
  enabled: false
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
```

4. Từ phiên bản py2neo v3, `cypher.excute` đã được thay thế bằng `graph.run` và trả về một `Cursor` thay vì `RecordList`. 

> The previous version of py2neo allowed Cypher execution through Graph.cypher.execute(). This facility is now instead accessible via Graph.run() and returns a lazily-evaluated Cursor rather than an eagerly-evaluated RecordList.

Đọc thêm:  https://stackoverflow.com/questions/37530309/attributeerror-graph-object-has-no-attribute-cypher-in-migration-of-data-fr

5. Từ phiên bản v4, `find_one` không còn được sử dụng nữa mà thay vào đó là `first` với `NodeMatcher`.

> py2neo v4 has a first function that can be used with a NodeMatcher. 

Đọc thêm: https://py2neo.org/v4/matching.html#py2neo.matching.NodeMatch.first

6. In py2neo v4, the `create_unique` function has been removed. To create a relationship between a user and a recipe and ensure uniqueness, you can use the `merge` function instead

## Hướng dẫn chạy chương trình

1. Tạo môi trường ảo bằng lệnh `python3 -m venv venv`
2. Tải `elasticsearch 8.8.1` and `kibana 8.8.1` từ https://www.elastic.co/downloads/elasticsearch và https://www.elastic.co/downloads/kibana
3. Giải nén và chạy file thực thi từ thư mục `bin`: `bin/elasticsearch.bat` và `bin/kibana.bat` và làm theo hướng dẫn để config Elasticsearch khi chạy lần đầu bằng Kibana
4. Cài đặt các thư viện cần thiết: `pip install -r requirements.txt`
5. Cài đặt Oracle Java 17 và Neo4j Community Edition từ https://www.oracle.com/java/technologies/downloads/ và https://neo4j.com/download-center/
6. Khởi động Neo4j và tạo mật khẩu cho Neo4j cũng như cài đặt thành một dịch vụ Windows
7. Chạy `elasticsearch.bat` trong thư mục `bin` của Elasticsearch
8. Khởi chạy môi trường ảo bằng lệnh `source venv/bin/activate`
9. Thứ tự chạy các file mã nguồn:
- [Data_Preparation_1.py](src/python3/DataPreparation1.py)
- [Data_Preparation_2.py](src/python3/DataPreparation2.py)
- [Exploration_n_Recommendation.ipynb](src/python3/Exploration_n_Recommendation.ipynb) 

## Cập nhật

Theo dõi Repo trên Github tại [đây](https://github.com/kztera/BTL-2-NMKHDL)

> Chương 7 được lấy từ cuốn sách Introducing Data Science: Big Data, Machine Learning, and more, using Python tools của Davy Cielen, Arno D. B. Meysman, Mohamed Ali.