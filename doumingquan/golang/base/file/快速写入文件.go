package main

import (
	"fmt"
	"io/ioutil"
	"log"
)

func main(){

	byte2:=ioutil.WriteFile("D:/phpStudy/WWW/test/index.php",[]byte("你好，hello world"),0777)
	fmt.Println(byte2)
	byte1,err:=ioutil.ReadFile("D:/phpStudy/WWW/test/index.php")//读取一个文件
	if err!=nil{
		log.Fatal(err)
	}
	fmt.Println(string(byte1))
	//byte2=os.Remove("D:/phpStudy/WWW/test/index.php")
	fmt.Println(byte2)
	dirname,err :=ioutil.ReadDir("../")
	for k,v:=range dirname{
		fmt.Println(k,"=",v.Name())
		fmt.Println(v.IsDir())
		fmt.Println(v.Mode())
		fmt.Println(v.ModTime())
		fmt.Println(v.Size())
		fmt.Println(v.Sys())
	}
}