<?php

namespace App\Http\Controllers\Admin;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Validator;

class CateController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $data = self::getTree();
        return view("admin.cate.list",['data'=>$data]);
    }

    public static function getTree(){
        $cates = DB::select('select *,concat(path,",",id) as paths  from cate where status=1 order by paths ');
        foreach($cates as $k=>$v){
            $arr = explode(",",$v->path);
            $len = count($arr)-1;
            $cates[$k]->catename = str_repeat('|----',$len).$v->catename;
            $cates[$k]->size = $len;
        }
        return $cates;
    }


    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view("admin.cate.add");
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $data = $request->except("_token");
        $rule=[
            'catename'=>'required',
        ];
        $message = [
            'catename.required'=>'分类名称不能为空!',
        ];
        $validator = validator::make($data,$rule,$message);
        if($validator->passes()){
            $result = DB::table('cate')->insert($data);
            if($result){
                return redirect('/admin/cate')->with('success','分类修改成功');
            }else{
                return back()->with("分类修改失败");
            }
        }else{
            return back()->withErrors($validator);
        }
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        $info = self::getTree();
        $data = DB::table("cate")->find(intval($id));
        return view("admin.cate.edit",compact('data','info'));
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
        $data = $request->only('catename','title','keywords','desc','sorts');
        $info = DB::table("cate")->where('id','=',intval($id))->update($data);
        if($info){
            return redirect("admin/cate")->with("success","修改成功");
        }else{
            return back()->with("error","修改成功");
        }

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
        $data = DB::table("cate")->where('id',intval($id))->update($data);
        if($data){
            echo 1;
        }else{
            echo 0;
        }
    }
}
