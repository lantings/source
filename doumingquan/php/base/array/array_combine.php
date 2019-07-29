<?php 
$rows = array(
    array('id' => 1, 'name' => 'lenbo'),
    array('id' => 2, 'name' => 'niuniu'),
    array('id' => 3, 'name' => 'liuliu'),
);
// 第一个参数作为key,第二个作为值,键值个数对等(array_combine(): Both parameters should have an equal number of elements)
$row = array_combine(array_column($rows,'name'), $rows);
echo "<pre>";
print_r($row);//die;


$arr1 = ['a','b','c','d','e'];
$arr2 = [1,2,3,4,5];
$arr = array_combine($arr1,$arr2);
echo "<pre>";
print_r($arr);//die;


 ?>