<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>AdminLTE 3 | Log in</title>
    <!-- Tell the browser to be responsive to screen width -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="/admin/style/plugins/fontawesome-free/css/all.min.css">
    <!-- Ionicons -->
    <link rel="stylesheet" href="https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css">
    <!-- icheck bootstrap -->
    <link rel="stylesheet" href="/admin/style/plugins/icheck-bootstrap/icheck-bootstrap.min.css">
    <!-- Theme style -->
    <link rel="stylesheet" href="/admin/style/dist/css/adminlte.min.css">
    <!-- Google Font: Source Sans Pro -->
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700" rel="stylesheet">
</head>
<body class="hold-transition login-page">
<div class="login-box">
    <div class="login-logo">
        <a href="../../index2.html"><b>起点移门</b>管理后台</a>
    </div>
    <!-- /.login-logo -->
    <div class="card">
        <div class="card-body login-card-body" >
            <form class="form-horizontal" method="POST" action="<?php echo e(route('login')); ?>">
                <?php echo e(csrf_field()); ?>

                <p></p>
                <div class="input-group mb-3">
                    <input type="email" class="form-control" name="email" value="<?php echo e(old('email')); ?>" required autofocus placeholder="请输入邮箱">

                    <?php if($errors->has('email')): ?>
                        <span class="help-block">
                                        <strong><?php echo e($errors->first('email')); ?></strong>
                                    </span>
                    <?php endif; ?>

                    <div class="input-group-append">
                        <div class="input-group-text">
                            <span class="fas fa-envelope"></span>
                        </div>
                    </div>
                </div>
                <div class="input-group mb-3">
                    <input id="password" type="password" class="form-control" name="password" required placeholder="请输入密码">

                    <?php if($errors->has('password')): ?>
                        <span class="help-block">
                            <strong><?php echo e($errors->first('password')); ?></strong>
                        </span>
                    <?php endif; ?>

                    <div class="input-group-append">
                        <div class="input-group-text">
                            <span class="fas fa-lock"></span>
                        </div>
                    </div>
                    <p></p>
                </div>
                <p></p>
                <p></p>
            <div class="social-auth-links text-center mb-2">
                <p></p>
                
                    <button type="submit" class="btn btn-block btn-danger"> 登 录  </button>
                
            </div>
            <!-- /.social-auth-links -->
            </form>
            <p class="mb-1">
                
            </p>
            <p class="mb-0">
                
            </p>
        <!-- /.login-card-body -->
    </div>
</div>
<!-- /.login-box -->

<!-- jQuery -->
<script src="/admin/style/plugins/jquery/jquery.min.js"></script>
<!-- Bootstrap 4 -->
<script src="/admin/style/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
<!-- AdminLTE App -->
<script src="/admin/style/dist/js/adminlte.min.js"></script>

</body>
</html>
