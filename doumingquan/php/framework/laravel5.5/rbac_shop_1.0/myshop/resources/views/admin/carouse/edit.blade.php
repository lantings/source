@extends("admin.layout.app")
@section("main")
<!--中间的内容部分开始-->
    <!-- Main content -->
    <section class="content">
      <div class="container-fluid">
            <div class="card card-primary">
              <form role="form" action="{{url('admin/carouse/'.$data->id)}}" method="post"  enctype="multipart/form-data">
               <input type="hidden" name="_method" value="put">
                {{csrf_field()}}
                <div class="card-body">
                  <div class="form-group">
                  <div class="form-group">
                    <label for="exampleInputPassword1">轮播图标题</label>
                    <input type="text" class="form-control" name="title" id="exampleInputPassword1" placeholder="请输入轮播图标题" value="{{$data->title}}">
                  </div>
                  <div class="form-group">
                          <div id="queue"></div>
                          <input id="file_upload" name="pic" type="file" multiple="true">
                          <img src="{{substr($data->pic,1)}}" alt="" width="60" height="60">
                  </div>
                  {{--<div class="form-group">--}}
                    {{--<label for="exampleInputPassword1">轮播图图片</label>--}}
                    {{--<input type="text" class="form-control" name="pic" id="exampleInputPassword1" placeholder="请输入分类标题">--}}
                  {{--</div>--}}
                  <div class="form-group">
                    <label for="exampleInputPassword1">轮播图链接地址</label>
                    <input type="text" class="form-control" name="url" id="exampleInputPassword1" placeholder="请输入关键字" value="{{$data->url}}">
                  </div>
                <div class="form-group">
                          <label for="exampleInputPassword1">排序</label>
                          <input type="text" class="form-control" name="sort" id="exampleInputPassword1" placeholder="请输入排序" value="{{$data->sort}}">
                </div>
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
