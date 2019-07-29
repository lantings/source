<?php 
$num = 50
$page = 20;
//array_slice可以实现分页
$length = ceil($num/$page);
for ($i=0; $i < $length ; $i++) { 
	$offset = $i*$page;
	$datas = array_slice($data, $offset,$page)
}
return $data;

function page_array($count,$page,$array,$order){    
    global $countpage; #定全局变量    
    $page=(empty($page))?'1':$page; #判断当前页面是否为空 如果为空就表示为第一页面     
       $start=($page-1)*$count; #计算每次分页的开始位置    
    if($order==1){    
      $array=array_reverse($array);    
    }       
    $totals=count($array);      
    $countpage=ceil($totals/$count); #计算总页面数    
    $pagedata=array();    
    $pagedata=array_slice($array,$start,$count);    
    return $pagedata;  #返回查询数据    
}

 ?>