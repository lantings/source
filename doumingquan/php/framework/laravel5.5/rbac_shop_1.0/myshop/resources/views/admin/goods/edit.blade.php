@extends("admin.layout.app")
@section("main")
<!--中间的内容部分开始-->
    <!-- Main content -->
    <section class="content">
      <div class="container-fluid">
            <!-- general form elements -->
            <div class="card card-primary">
              {{--<div class="card-header">--}}
                {{--<h3 class="card-title">Quick Example</h3>--}}
              {{--</div>--}}
              <!-- /.card-header -->
              <!-- form start -->
              <form role="form" action="{{url('admin/goods/'.$goods->id)}}" method="post"  enctype="multipart/form-data">
                {{csrf_field()}}
                  <input type="hidden" name="_method" value="put">
                <div class="card-body">

                  <div class="form-group">
                    <label for="exampleInputPassword1">商品名称</label>
                    <input type="text" class="form-control" name="goodsname" id="exampleInputPassword1" placeholder="请输入商品名称" value="{{$goods->goodsname}}">
                  </div>
                  <div class="form-group">
                        <label>商品分类</label>
                        <select class="custom-select" name="cate_id">
                            <option  value=""></option>
                            @foreach($data as $v)
                                @if ($goods->cate_id==$v->id)
                                <option  value="{{$v->id}}" selected>{{$v->catename}}</option>
                                @else
                                 <option  value="{{$v->id}}"> {{$v->catename}}</option>
                                @endif
                            @endforeach
                        </select>
                  </div>
                  <div class="form-group">
                    <label for="exampleInputPassword1">商品标题</label>
                    <input type="text" class="form-control" name="title" id="exampleInputPassword1" placeholder="请输入商品标题" value="{{$goods->title}}">
                  </div>
                  <div class="form-group">
                      <label for="exampleInputPassword1">商品价格</label>
                      <input type="text" class="form-control" name="price" id="exampleInputPassword1" placeholder="请输入商品标题" value="{{$goods->price}}">
                  </div>
                  <div class="form-group">
                      <label for="exampleInputPassword1">商品活动价格</label>
                      <input type="text" class="form-control" name="hdprice" id="exampleInputPassword1" placeholder="请输入商品标题" value="{{$goods->hdprice}}">
                  </div>
                  <div class="form-group">
                        <label for="exampleInputPassword1">数量</label>
                        <input type="text" class="form-control" name="num" id="exampleInputPassword1" placeholder="请输入商品数量" value="{{$goods->num}}">
                  </div>
                  <div class="form-group">
                    <label for="exampleInputPassword1">商品关键字</label>
                    <input type="text" class="form-control" name="keywords" id="exampleInputPassword1" placeholder="请输入关键字" value="">
                  </div>
                   <div class="form-group">
                      <label for="exampleInputPassword1">商品简介</label>
                       <script type="text/plain" name="content" id="myEditor" style="width:1000px;height:240px;" >{!! $goods->content !!}
                       </script>;
                      {{--<input type="text" class="form-control" name="content" id="exampleInputPassword1" placeholder="请输入关键字" value="{{$goods->content}}">--}}
                   </div>
                </div>
                <div class="form-group">
                      <div id="queue"></div>
                      <input id="file_upload" name="file_upload" type="file" multiple="true">
                      <img src="{{substr($goods->pic,1)}}" alt="" width="60px" height="60px">
                </div>

                  {{--<div class="form-group">--}}
                    {{--<label for="exampleInputFile">图片上传</label>--}}
                    {{--<div class="input-group">--}}
                      {{--<div class="custom-file">--}}
                        {{--<input type="file" class="custom-file-input" id="exampleInputFile">--}}
                        {{--<label class="custom-file-label" for="exampleInputFile">选择图片</label>--}}
                      {{--</div>--}}
                      {{--<div class="input-group-append">--}}
                        {{--<span class="input-group-text" id="">Upload</span>--}}
                      {{--</div>--}}
                    {{--</div>--}}
                  {{--</div>--}}

                <div class="card-footer">
                  <button type="submit" class="btn btn-primary">提交</button>
                </div>
              </form>
            </div>
      </div>
    </section>
 <!--中间的内容部分结束-->
<script type="text/javascript">
    <?php $timestamp = time();?>
    $(function() {
        $('#file_upload').uploadify({
            'formData'     : {
                'timestamp' : '<?php echo $timestamp;?>',
                'token'     : '<?php echo md5('unique_salt' . $timestamp);?>'
            },
            'swf'      : '/admin/style/plugins/uploadify/uploadify.swf',
            'uploader' : 'uploadify.php'
        });
    });
</script>
<script>
    var um = UM.getEditor('myEditor');
</script>
 @endsection
