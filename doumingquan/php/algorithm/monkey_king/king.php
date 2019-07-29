<?php 
// $n猴子总数，$m 数字
function ($m,$n){
	$monkey = range(1, $n);
	$i=0;
	while(count($monkey)>1){
		if(($i+1)%$m==0){
			unset($monkey[$i]);
		}else{
			array_push($monkey, $monkey[$i]);//把没有被数到的猴子放到末尾
			unset($monkey[$i]);
		}
		$i++;
	}
	return current($monkey);
}
 ?>