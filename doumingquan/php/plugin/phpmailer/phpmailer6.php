<?php 
	public function mail(){
    	# from:https://github.com/PHPMailer/PHPMailer
    	$mail = new PHPMailer(true);
    	// var_dump($mail);
    	try {
		    //服务器设置
	    	$mail->SMTPDebug = SMTP::DEBUG_SERVER;          	// Enable verbose debug output
		    $mail->isSMTP();                               		// Send using SMTP
		    $mail->Host       = 'smtp.163.com';            		// Set the SMTP server to send through
		    $mail->SMTPAuth   = true;                       	// Enable SMTP authentication
		    $mail->Username   = 'mqyy2015@163.com';         	// SMTP username
		    $mail->Password   = 'BYUKPOSJHBNKZNVR';          	// SMTP 授权码非登录密码
		    // $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Enable TLS encryption; `PHPMailer::ENCRYPTION_SMTPS` encouraged
		    $mail->Port       = 25;                             // TCP port to connect to, use 465 for `PHPMailer::ENCRYPTION_SMTPS` above

		    //接收者
		    $mail->setFrom($mail->Username, 'mingquan');		//发送人
		    $mail->addAddress('469688010@qq.com', 'john');    	//接受人1
		    $mail->addAddress('768429319@qq.com','lanting');    //接受人2
		    // $mail->addReplyTo('info@example.com', 'Information');
		    // $mail->addCC('cc@example.com');
		    // $mail->addBCC('bcc@example.com');

		    // 附件
		    // $mail->addAttachment('/var/tmp/file.tar.gz');         // Add attachments
		    $mail->addAttachment('images/180308032959266.jpg', 'new.jpg');    // Optional name

		    // 内容
		    $mail->isHTML(true);            // Set email format to HTML
		    $mail->Subject = 'Here is the subject';
		    $mail->Body    = 'This is the HTML message body <b>in bold!</b>';
		    $mail->AltBody = 'This is the body in plain text for non-HTML mail clients';

		    $mail->send();
		    echo 'Message has been sent';
		} catch (Exception $e) {
		    echo "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
		}
	}
 ?>