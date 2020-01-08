@extends("admin.layout.app")
@section("main")
<!--中间的内容部分开始-->
    <!-- Main content -->
    <section class="content">
      <div class="container-fluid">

          <!-- left column -->

            <!-- general form elements -->
            <div class="card card-primary">
              {{--<div class="card-header">--}}
                {{--<h3 class="card-title">Quick Example</h3>--}}
              {{--</div>--}}
              <!-- /.card-header -->
              <!-- form start -->
              <form role="form" action="{{url('admin/cate')}}" method="post"  enctype="multipart/form-data">
                {{csrf_field()}}
                <input type="hidden" name="pid" value="<?php echo isset($_GET['id'])?$_GET['id']:0;?>">
                <input type="hidden" name="path" value="<?php echo isset($_GET['path'])?$_GET['path']:0;?>">
                <div class="card-body">
                  <div class="form-group">
                    {{--<label>已有分类</label>--}}
                    {{--<select class="custom-select">--}}
                      {{--<option>option 1</option>--}}
                      {{--<option>option 2</option>--}}
                      {{--<option>option 3</option>--}}
                      {{--<option>option 4</option>--}}
                      {{--<option>option 5</option>--}}
                    {{--</select>--}}
                  {{--</div>--}}
                  <div class="form-group">
                    <label for="exampleInputPassword1">分类名称</label>
                    <input type="text" class="form-control" name="catename" id="exampleInputPassword1" placeholder="请输入分类名称">
                  </div>
                  <div class="form-group">
                    <label for="exampleInputPassword1">分类标题</label>
                    <input type="text" class="form-control" name="title" id="exampleInputPassword1" placeholder="请输入分类标题">
                  </div>
                  <div class="form-group">
                    <label for="exampleInputPassword1">分类关键字</label>
                    <input type="text" class="form-control" name="keywords" id="exampleInputPassword1" placeholder="请输入关键字">
                  </div>
                   <div class="form-group">
                      <label for="exampleInputPassword1">描述</label>
                      <input type="text" class="form-control" name="desc" id="exampleInputPassword1" placeholder="请输入关键字">
                   </div>
                </div>
                <div class="form-group">
                  <label for="exampleInputPassword1">排序</label>
                  <input type="text" class="form-control" name="sorts" id="exampleInputPassword1" placeholder="请输入排序">
                </div>
            </div>
                <div class="card-footer">
                  <button type="submit" class="btn btn-primary">提交</button>
                </div>
              </form>
            </div>
      </div>
    </section>
 <!--中间的内容部分结束-->
 @endsection
