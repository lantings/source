<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});
Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
Route::get('/', 'admin\PostController@index')->name('home');
Route::resource('posts', 'admin\PostController');
Route::resource('users', 'admin\UserController');
Route::resource('roles', 'admin\RoleController');
Route::resource('permissions', 'admin\PermissionController');

Route::get('/index','admin\Indexcontroller@index');
Route::resource('/admin/user','admin\UserController');
Route::resource('/admin/goods','admin\GoodsController');
Route::resource('/admin/cate','admin\CateController');
Route::resource('/admin/carouse','admin\CarouseController');
Route::any('/admin/orders','admin\OrdersController@index');