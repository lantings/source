@extends("admin.layout.app")
@section("main")
  <!-- Main content -->
  <section class="content">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">商品列表</h3>
          </div>
          <!-- /.card-header -->
          <div class="card-body">
            <table id="example2" class="table table-bordered table-hover">
              <thead>
              <tr>
                <th>id</th>
                <th>商品名称</th>
                <th>商品标题</th>
                <th>商品简介</th>
                <th>商品价格</th>
                <th>商品图片</th>

                <th>操作</th>
              </tr>
              </thead>
              <tbody>
            @foreach($data as $v)
              <tr>
                <td>{{$v->id}}</td>
                <td>{{$v->goodsname}}</td>
                <td>{{$v->title}}</td>
                <td width="100px" height="60px">{!!$v->content!!}</td>
                <td>{{$v->price}}</td>
                <td><img src="{{substr($v->pic,1)}}" alt="" width="60" height="60"></td>
                <td>
                  <a href="{{url('admin/goods/'.$v->id.'/edit')}}"> <button type="submit" class="btn  btn-primary ">修改</button></a>
                  <a href="javascript:" onclick="del_goods({{$v->id}})"><button type="submit" class="btn  btn-danger ">删除</button></a>
                  <script>
                    function del_goods(id){
                      $.post("/admin/goods/"+id,{'_token':"{{csrf_token()}}","_method":"delete"},function(res){
                      if(res){
                        alert("删除成功")
                      }else{
                        alert("删除失败")
                      }
                      })
                    }

                  </script>
                </td>
              </tr>
              @endforeach
              </tbody>

            </table>
          </div>
          <!-- /.card-body -->
        </div>
      </div>
    </div>
  </section>
@endsection