curl -X POST \
  http://172.26.16.90/danastudio/dodox/filemanager/file/upload \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NjQ5ODczNzIsImlhdCI6MTU2NDM4MjU3MiwiaXNzIjoiZGFuYXN0dWRpb19hdXRoX3NlcnZlciIsIm1vZHVsZXMiOlsiYWNjZXNzIiwiZGV2ZWxvcCIsIndvcmtmbG93IiwidmF1bHQiLCJkZXZjZW50ZXIiLCJvcGVyYXRpbmciXSwicm9sZV9pZCI6ImRldmVsb3BlciIsInJvbGVfbmFtZSI6IuW8gOWPkeiAhSIsInRrdmVyc2lvbiI6MSwidXNlcl9pZCI6IkFXcWFabUNoY2tVd0RSSTluUFZrIiwidXNlcl9uYW1lIjoiZGF0YXRvbSJ9.b4yzZoAJBrSl7y444giQB0cM1gKlgeV3_h6kLEY3bMEIbd4bRCkoXOPPPLZIfYQw5092dNJYQ1MVmRsyFm8aGVmlr_oIzfr08oojZElZzRjm-kdcIoEWJDmXN7yMzAqEu4PhB7HhNF8qqigqwCrmlwehRRymqfapXcX0zWMLqfTIi8xNIfM4G28ExOH9EZOW2LMDljmEk4-PaEm435ByIC6G_q_Z_GZT1VCqq6GHWoGSqnfuvoO7tINc5uCF7F2_mjV61qhogMn5bJG9K0PEUEaEh3dOH0mQu0L_w2Ey5JBJ7ZWwH8nPp0fkJMNPsJhiHlrph88sw7KMWsRLY_vrT3AzCENYyNUD42WuniZtQE0cRBloHdXpe65QGmQGD8qcoe3NcBBHeW97d3zwLrYZHZJnIpEOahhGtvUyxkjJCTl_w4mNSO339q_yYzukmsdE5wyLIjje91UtSrUEiTJQazZrMbn8i25tZTq6eWntxYI4LEynikgOll3cIQsBiL8icd1wweudSZoAeZRWOk4c0otfbJPA6jsabxwjWKC8X1eDDixkoyWtGFe0oeEL2OqPXO7yfeuUeC5jeHNtz3cgRcF8FXRzSpFwoR8CDGxv4HCo9OFALMlhzGzjS1EAFeTX6aQY5ucJ7DgVbJ2xNRwSyCtdPbUyTg8Ld3XI_O2AENY' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 2588' \
  -H 'Content-Type: multipart/form-data; boundary=--------------------------344996046817945279062489' \
  -H 'Host: 172.26.16.90' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F filepath=/var/dana/dodox/filemanager/file/admin/1 \
  -F force=true \
  -F file=@/opt/uplaod.py