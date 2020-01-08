<?php

namespace App\Http\Controllers\Admin;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Models\Carouse;
use Illuminate\Support\Facades\DB;

class CarouseController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $num=10;
        $data = DB::table("carouses")->orderBy("sort")->paginate($num);;
//        dd($data);
        return view("admin.carouse.list",['data'=>$data]);
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        $data = [];
        return view("admin.carouse.add");
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
//        $data = $request->except("_token");dd($data);
        $carouse = new carouse();
        $this->CreateDate($request,$carouse);
        $upload_filename = GoodsController::upload($request,'pic','admin/carous');
        if($upload_filename=='null'){
            return back()->with("error","请上传图片");
        }
        $carouse->pic=$upload_filename;
        if($carouse->save()){
            return redirect('/admin/carouse')->with('success','轮播图添加成功');
        }else{
            return back()->with('error','轮播图添加失败');
        }
    }

    public function CreateDate($request,$carouse){
        $carouse->title = $request->input('title');
        $carouse->url = $request->input('url');
        $carouse->sort = $request->input('sort');
        $carouse->content = $request->input('content');
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {

    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        $data = DB::table("carouses")->find($id);
//        dd($data);
        return view("admin.carouse.edit",['data'=>$data]);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        $data = $request->only('title','pic','url','sort','content','status');
        $data['pic'] = GoodsController::upload($request,'pic','admin/carouse');
        if($data['pic'] == null){
            unset($data['pic']);
        }
//        dd($data);
        $info = DB::table("carouses")->where('id','=',intval($id))->update($data);
        if($info){
            return redirect("admin/carouse")->with("success","修改成功");
        }else{
            return back()->with("error","修改成功");
        }
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $data['status']=0;
//        $data = DB::table("carouses")->where('id',intval($id))->delete();
        $data = DB::table("carouses")->where('id',intval($id))->update($data);
        if($data){
            echo 1;
        }else{
            echo 0;
        }
    }
}
