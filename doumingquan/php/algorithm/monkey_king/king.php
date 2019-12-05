<?php 
/*
有n只猴子 数字为m
思路：有n只猴子，当数到m的时候那只猴子就T掉，不等于的话就把这个数据加到末尾在把原来那个位置给T掉
*/
function getMonkeyKing($m,$n){
	$monkeys = range(1,$n);
	$i=0;
	while(count($monkeys)>1){
		if(($i+1)%$m==0){
			unset($monkeys[$i]);
		}else{
			array_push($monkeys, $monkeys[$i]);//把没有被数到的猴子放到末尾
			unset($monkeys[$i]);
		}
	$i++;
	}
	return current($monkeys);

}
$result = getMonkeyKing(11,10);
// var_dump($result);


?>