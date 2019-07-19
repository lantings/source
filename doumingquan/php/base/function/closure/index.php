<?php 
	//匿名函数
	function func($param){
	     return function() use($param,$params){
	        echo $param+$params;
	     };
	 }
	$content = func(222,33);
	$content();
 ?>