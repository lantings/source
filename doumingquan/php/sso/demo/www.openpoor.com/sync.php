<?php  
$redirect = empty($_GET['redirect']) ? 'www.openpoor.com' : $_GET['redirect'];  

  //echo "redirect = ".$redirect."<br/>";
  //echo "code = ".$_GET['code']."<br/>";exit;

if(empty($_GET['code'])){    
  header('Loaction:http://'.urldecode($redirect));  
  exit;  
}  
  
$apps = array(  
  'www.myspace.com/slogin.php',  
  'www.mingc.com/slogin.php'  
);  
?>  
<!DOCTYPE html>  
<html>  
<head>  
<meta charset="UTF-8"/>  
<?php foreach($apps as $v): ?> 
<!-- 使用src进行跨域操作  -->
<script type="text/javascript" src="http://<?php echo $v.'?code='.$_GET['code'] ?>"></script>  
<?php endforeach; ?>  
<title>passport</title>  
</head>  
<body>  
<script type="text/javascript">  
window.onload=function(){  
  location.replace('<?php echo $redirect; ?>');  
}  
</script>  
</body>  
</html>  