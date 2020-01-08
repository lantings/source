<?php

namespace App\Http\Controllers\Admin;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;
use App\Models\Goods;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;
//use Qiniu\Auth;
//use Qiniu\Storage\UploadManager;

class GoodsController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        //查询分类
//        dd(55);
        $cates = CateController::getTree();
        $title=$request->get('title');
        $cate_id=$request->get('cate_id');
        $data = DB::table("goods")
        ->where(function ($query)use($title,$cate_id){
            if($cate_id){
                $query->where('cate_id',$cate_id);
            }
            if($title){
                $query->where('title','like','%'.$cate_id.'%');
            }
        })
        ->where("is_delete",1)
        ->join('cate','goods.cate_id','=','cate.id')->select('goods.*','cate.catename')->orderby('goods.id','desc')->paginate(10);
//        dd($data);
        return view("admin.goods.list",compact('data','cates'));
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //查询分类
        $cates = CateController::getTree();
//        dd($cates);
        return view("admin.goods.add",['data'=>$cates]);
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
        $goods = new Goods();
        //调用方法 创建数据
        $this->CreateDate($request,$goods);
//       上传七牛云
//        $file = $request->file('file_upload');
//        $tmpPath  = $file->getPathname();    // 获取图片在本地绝对路径
//        $ext      = $file->getClientOriginalExtension();
//        $fileName = time() . rand(1000, 10000) . '.' . $ext;
//        echo $fileName;
//        $accessKey = 'aXMEu3X436hYHuYY_TSj0YL_1b5Ok_jgaivZ1YQk';
//        $secretKey = 'MOxBjlw2xxF5rNv8wYv1700RV_Bx2_lLY5zUrpKl';
//        $bucketName="mingquanphoto";
//        $upManager = new UploadManager();
//        $auth    = new Auth($accessKey, $secretKey);
//        $token = $auth->uploadToken($bucketName);    # 上传空间名称
//        echo $token;
//        list($ret, $error) = $upManager->putFile($token, $fileName, $tmpPath);
//        if ($error !== null) {
//            dd($error);
//        } else {
//            dd($ret);
//        }
        $upload_filename = $this->upload($request,'file_upload','admin/goods');
        if($upload_filename=='null'){
            return back()->with("error","请上传图片");
        }
        $goods->pic=$upload_filename;
        if($goods->save()){
            return redirect('/admin/goods')->with('success','商品添加成功');
        }else{
            return back()->with('error','商品添加失败');
        }
//        $rule=[
//            'goodsname'=>'required',
//            'price'=>'required',
//        ];
//        $message = [
//            'goodsname.required'=>'商品名称不能为空!',
//            'goodsname.price'=>'商品价格不能为空!',
//        ];
//        $validator = validator::make($data,$rule,$message);
//        if($validator->passes()){
//            $result = DB::table('cate')->insert($data);
//            if($result){
//                return redirect('/admin/cate')->with('success','分类修改成功');
//            }else{
//                return back()->with("分类修改失败");
//            }
//        }else{
//            return back()->withErrors($validator);
//        }


    }
    //封装方法创建数据
    public function CreateDate($request,$goods){
        $goods->goodsname = $request->input('goodsname');
        $goods->cate_id = $request->input('cate_id');
        $goods->hdprice = $request->input('hdprice');
        $goods->price = $request->input('price');
        $goods->title = $request->input('title');
        $goods->num = $request->input('num');
//        $goods->pic = $request->input('file_upload');
        $goods->content = $request->input('content');
//        $goods->status = $request->input('is_delete');
    }
/*
 * @request     对象
 * @filename    图片字段名称
 * @module      目录的名称 admin/goods
 */
    public static function upload($request,$filename,$module)
    {
        //检测是否有文件上传
        if($request->hasFile($filename)){
            //随机文件名
            $name = md5(time()+rand(1,999999));
            //获取后缀名
            $type = $request->file($filename)->getClientOriginalExtension();
            $arr = array('jpg','png','jpeg','tiff');
            //判断
            if(!in_array($type,$arr)){
                return back();
            }
            $dir = './uploads/'.$module.'/';
            //将文件移动到指定目录下
            $request->file($filename)->move($dir, $name.'.'.$type);
            return $dir.$name.'.'.$type;
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
        $goods = DB::table("goods")->find(intval($id));
        $data = CateController::getTree();
        return view("admin.goods.edit",compact("data",'goods'));
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
        $data = $request->only('goodsname','cate_id','title','price','hdprice','num','content');
        $upload_filename = $this->upload($request,'file_upload','admin/goods');
        if($upload_filename==null){
            unset($data['pic']);
        }else{
            $data['pic']=$upload_filename;
        }
        $result = DB::table("goods")->where("id",intval($id))->update($data);
        if($result){
            return redirect('/admin/goods')->with('success','商品修改成功');
        }else{
            return back()->with('error','商品修改失败');
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
        $data['is_delete']=0;
        $data = DB::table("goods")->where('id',intval($id))->update($data);
        Log::info("this is test");
        if($data){
            echo 1;
        }else{
            echo 0;
        }
    }
}
