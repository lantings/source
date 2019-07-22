<?php 
//from: https://www.cnblogs.com/johnson108178/p/8007585.html
	function createRange($number){
	    $data = [];
	    for($i=0;$i<$number;$i++){
	        $data[] = time();
	    }
	    return $data;
	}
	$result = createRange(10); // 这里调用上面我们创建的函数
	foreach($result as $value){
	    sleep(1);//这里停顿1秒，我们后续有用
	    echo $value.'<br />';
	}

	function createRanges($number){
	    for($i=0;$i<$number;$i++){
	        yield time();
	    }
	}

	$result = createRanges(10); // 这里调用上面我们创建的函数
	foreach($result as $value){
	    sleep(1);
	    echo $value.'<br />';
	}
 ?>