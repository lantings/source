<?php 
function func($num1,$num2){
     return function() use($num1,$num2){
         echo  $num1+$num2;
     };
 }

 $content = func(22,44);
 $content();

//(示例2):函数中把匿名函数返回,返回后调用它
 function content(){
     return $func = function($param,$test){
         echo $param+$test;
        
     };
 }
 $data = content();
 $data(3,4);

 ?>