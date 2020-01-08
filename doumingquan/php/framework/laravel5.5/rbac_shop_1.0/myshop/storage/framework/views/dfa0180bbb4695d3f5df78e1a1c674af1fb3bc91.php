<?php $__env->startSection('title', '| Create New Post'); ?>
<?php $__env->startSection('content'); ?>
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
            <h1>Create New Post</h1>
            <hr>
            
            <?php echo e(Form::open(array('route' => 'posts.store'))); ?>


            <div class="form-group">
                <?php echo e(Form::label('title', 'Title')); ?>

                <?php echo e(Form::text('title', null, array('class' => 'form-control'))); ?>

                <br>

                <?php echo e(Form::label('body', 'Post Body')); ?>

                <?php echo e(Form::textarea('body', null, array('class' => 'form-control'))); ?>

                <br>

                <?php echo e(Form::submit('Create Post', array('class' => 'btn btn-success btn-lg btn-block'))); ?>

                <?php echo e(Form::close()); ?>

            </div>
        </div>
    </div>

<?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.app', array_except(get_defined_vars(), array('__data', '__path')))->render(); ?>