@extends("admin.layout.app")
@section("main")
  <!-- Main content -->
  <section class="content">
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">订单列表</h3>
          </div>
          <!-- /.card-header -->
          <div class="card-body">
            <table id="example2" class="table table-bordered table-hover">
              <thead>
              <tr>
                <th>id</th>
                <th>订单号</th>
                <th>商品名称</th>
                <th>商品图片</th>
                <th>消费者</th>
                <th>价格</th>
                <th>数量</th>
                <th>总金额</th>
                <th>订单状态</th>
                <th>支付方式</th>
              </tr>
              </thead>
              <tbody>
            @foreach($data as $v)
              <tr>
                <td>{{$v->id}}</td>
                <td>{{$v->orderno}}</td>
                <td>{{$v->goodsname}}</td>
                <td><img src="{{substr($v->pic,1)}}" alt="" width="60" height="60"></td>
                <td>{{$v->user_id}}</td>
                <td>{{$v->price}}</td>
                <td>{{$v->num}}</td>
                <td>{{$v->total_money}}</td>
                <td>{{$v->order_status}}</td>
                <td>{{$v->pay_type}}</td>
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