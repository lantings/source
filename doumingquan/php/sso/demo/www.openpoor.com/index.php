<?php  
session_start();  
  //session_destroy();
?>  
<!DOCTYPE html>  
<html>  
<head>  
<meta charset="UTF-8"/>  
<title>sync login</title>  
</head>  
<body>  
  
<?php if(empty($_SESSION['username'])):?>  
hello,游客;请先<a href="login.php">登录</a><a href="http://www.myspace.com/index.php">进入空间</a>  
<?php else: ?>  
hello,<?php echo $_SESSION['username']; ?>;<a href="http://www.myspace.com/index.php">进入空间</a>  
<?php endif; ?>  
  <a href="http://www.openpoor.com/index.php">home</a>  
</body>  
</html>  