<?php 
function assoc_unique(&$arr,$key){
	$tmp_arr = array();
	foreach ($arr as $k => $v) {
		if (in_array($v[$key], $tmp_arr)) {
			unset($arr[$k]);
		}else{
			$tmp_arr[] = $v[$key]
		}
	}
	return $arr;
}
 ?>