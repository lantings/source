@extends("admin.layout.app")
@section("main")
  <!-- Main content -->
  <section class="content">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">轮播图列表</h3>
          </div>
          <!-- /.card-header -->
          <div class="card-body">
            <table id="example2" class="table table-bordered table-hover">
              <thead>
              <tr>
                <th>id</th>
                <th>轮播图名称</th>
                <th>轮播图标题</th>
                <th>轮播图内容(s)</th>
                <th>轮播图图片</th>
                <th>轮播图链接地址</th>
                <th>排序</th>
                <th>操作</th>
              </tr>
              </thead>
              <tbody>
            @foreach($data as $v)
              <tr>
                <td>{{$v->id}}</td>
                <td>{{$v->title}}</td>
                <td>{{$v->url}}</td>
                <td>{{$v->content}}</td>
                <td><img src="{{substr($v->pic,1)}}" alt="" width="40" height="40"></td>
                <td>{{$v->url}}</td>
                <td>{{$v->sort}}</td>
                <td>
                  <a href="{{url('admin/carouse/'.$v->id.'/edit')}}"><button type="submit" class="btn  btn-primary ">修改</button></a>
                  <a href="javascript:" onclick="del_carouse({{$v->id}})"><button type="submit" class="btn  btn-danger ">删除</button></a>
                  <script>
                    function del_carouse(id){
//                      alert(id)
                      $.post("/admin/carouse/"+id,{'_token':"{{csrf_token()}}","_method":"delete"},function(res){
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
        {{$data->render()}}
      </div>
    </div>
  </section>
@endsection