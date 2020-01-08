<?php

namespace App\Http\Controllers\Admin;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class OrdersController extends Controller
{
    public function index(){
        $data = DB::table('shoporders')
            ->join('goods','goods.id','=','shoporders.goods_id')
            ->select('shoporders.*','goods.goodsname','goods.pic')
            ->orderby('shoporders.id','desc')
            ->paginate(10);
        return view("admin.orders.list",['data'=>$data]);
    }
}
