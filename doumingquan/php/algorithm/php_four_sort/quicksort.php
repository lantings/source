<?php 
function quicksort($arr){
	//判断数组个数等于1，返回
	$length = count($arr);
	if ($length<1) {
		return $arr;
	}else{
		$left = $right = [];
		for ($i=1; $i <$length ; $i++) { 
			if($arr[$i]>$arr[0]){
				$right[]=$arr[$i];
			}else{
				$left[]=$arr[$i];
			}
		}
		$left  = quicksort($left);
		$right = quicksort($right);
		return array_merge($left,array($arr[0]),$right);
	}
	
	
}
$arrs = [23,5,66,84,56,99,52];

$result = quicksort($arrs);
var_dump($result);