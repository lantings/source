<?php 
header("content-type:text/html;charset=utf-8");
function readTxt()
{
    # code...
    $handle = fopen("./test.txt", 'rb');

    while (feof($handle)===false) {
        # code...
        yield fgets($handle);
    }

    fclose($handle);
}
// echo 999;
foreach (readTxt() as $key => $value) {
    # code...
    echo $value.'<br />';
}
 ?>