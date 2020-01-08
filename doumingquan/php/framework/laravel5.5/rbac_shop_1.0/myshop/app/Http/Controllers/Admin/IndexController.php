<?php
/**
 * Created by PhpStorm.
 * User: ASUS
 * Date: 2019/12/1
 * Time: 10:17
 */
namespace App\Http\Controllers\Admin;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class IndexController extends Controller{
    public function index(){
        echo "this is laravel54";
        return view('admin.index.index');
    }
}