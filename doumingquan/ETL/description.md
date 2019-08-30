use software datax configure json file,

use 'python /datax/bin/datax.py ***/**.json' 

curl -i -C - -X PUT -T /opt/datatom/xinghuansftp/yibaoju/yyxx.csv "http://172.17.148.189:31734/webhdfs/v1/tmp/detuo/yyxx.csv?op=CREATE&data=true&guardian_access_token=IdnsKV9cgCVkfF00VEka-M8IUIMT.TDH" -H "Content-Type:application/octet-stream"

load DATA inPATH '/tmp/detuo/yyqx.csv' INTO TABLE `yibaoju_txt`.`material_info`

