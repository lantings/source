@extends("admin.layout.app")
@section("main")
  <!-- Main content -->
  <section class="content">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">分类列表</h3>
          </div>
          <!-- /.card-header -->
          <div class="card-body">
            <table id="example2" class="table table-bordered table-hover">
              <thead>
              <tr>
                <th>id</th>
                <th>分类名称</th>
                <th>分类标题</th>
                <th>分类关键字(s)</th>
                <th>分类描述</th>
                <th>添加子分类</th>
                <th>排序</th>
                <th>操作</th>
              </tr>
              </thead>
              <tbody>
            @foreach($data as $v)
              <tr>
                <td>{{$v->id}}</td>
                <td>{{$v->catename}}</td>
                <td>{{$v->title}}</td>
                <td>{{$v->keywords}}</td>
                <td>{{$v->desc}}</td>
                <th><a href="{{url('admin/cate/create?id='.$v->id.'&path='.$v->path.','.$v->id)}}">添加子分类</a></th>
                <td>{{$v->sorts}}</td>
                <td>
                  <a href="{{url('admin/cate/'.$v->id.'/edit')}}"><button type="submit" class="btn  btn-primary ">修改</button></a>
                  <a href="javascript:" onclick="del_cate({{$v->id}})"><button type="submit" class="btn  btn-danger ">删除</button></a>
                  <script>
                    function del_cate(id){
                      alert(id)
                      $.post("/admin/cate/"+id,{'_token':"{{csrf_token()}}","_method":"delete"},function(res){
                        if(res==1){
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