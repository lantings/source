<?php 
function bubbling($arr){
	$length = count($arr);
	$tem=array();
	for ($i=0; $i <$length ; $i++) { 
		for ($j=0; $j <$length-$i-1 ; $j++) { 
			if ($arr[$j]>$arr[$j+1]) {
				$tmp=$arr[$j];
				$arr[$j]=$arr[$j+1];
				$arr[$j+1]=$tmp;
			}
		}
	}
	return $arr;
}
$arrs = [23,5,66,84,56,99,52];

$result = bubbling($arrs);
var_dump($result);
 ?>