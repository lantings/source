<?php 
// 常见的三个使用场景
// 1、从二维数组中获取某一列的值，返回一个新的数组。
$rows = array(
    array('id' => 1, 'name' => 'lenbo'),
    array('id' => 2, 'name' => 'niuniu'),
    array('id' => 3, 'name' => 'liuliu'),
);
$ids = array_column($rows, 'id');

print_r($ids);// 得到$ids = array(1, 2, 3);

// 2.从二维数组中返回以$index_key => $column的键值对
// 使用场景：枚举值映射。
// $rows = array(
//     array('code' => 'h5', 'text' => 'H5浏览器'),
//     array('code' => 'alipay', 'text' => '支付宝浏览器'),
//     array('code' => 'wechat', 'text' => '微信浏览器'),
// );
// $map = array_column($rows, 'text', 'code');

// echo $map['h5'];// H5浏览器
// echo $map['alipay'];// 支付宝浏览器
// echo $map['wechat'];// 微信浏览器

// 3、 将某列的值作为二维数组的索引
$rows = array(
    array('code' => 'h5', 'text' => 'H5浏览器'),
    array('code' => 'alipay', 'text' => '支付宝浏览器'),
    array('code' => 'wechat', 'text' => '微信浏览器'),
);
$map = array_column($rows, 'text', 'code');

print_r($map);// array('code' => 'alipay', 'text' => '支付宝浏览器')




 ?>