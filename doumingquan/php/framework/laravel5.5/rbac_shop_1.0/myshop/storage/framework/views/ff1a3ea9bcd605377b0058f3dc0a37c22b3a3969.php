<?php $__env->startSection('content'); ?>
    <div class="container">
        <div class="row">
            <div class="col-md-10 col-md-offset-1">
                <div class="panel panel-default">
                    <div class="panel-heading"><h3>Posts</h3></div>
                    <div class="panel-heading">Page <?php echo e($posts->currentPage()); ?> of <?php echo e($posts->lastPage()); ?></div>
                    <?php $__currentLoopData = $posts; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $post): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <div class="panel-body">
                            <li style="list-style-type:disc">
                                <a href="<?php echo e(route('posts.show', $post->id )); ?>"><b><?php echo e($post->title); ?></b><br>
                                    <p class="teaser">
                                        <?php echo e(str_limit($post->body, 100)); ?> 
                                    </p>
                                </a>
                            </li>
                        </div>
                    <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                </div>
                <div class="text-center">
                    <?php echo $posts->links(); ?>

                </div>
            </div>
        </div>
    </div>
<?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.app', array_except(get_defined_vars(), array('__data', '__path')))->render(); ?>