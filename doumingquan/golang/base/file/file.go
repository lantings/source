package main

import (
	"fmt"
	"log"
	"os"
)

func main()  {
	os.Mkdir("astaxie",0777)
	os.MkdirAll("astaxie/test/test",0777)
	filename := "test.txt"
	//create方法创建文件
	res,err:=os.Create(filename)
	if err!=nil{
		log.Fatal(err)
	}
	//fmt.Println(res)
	defer res.Close()
	for i:=0;i<10;i++{

		res.WriteString("this is test!\r\n")
		res.Write([]byte("this is a test!\r\n"))
	}
	res1,err:=os.Open(filename)
	fmt.Println(err,"=")
	if err!=nil{
		fmt.Println(res1,err)
		return
	}
	defer res1.Close()
	buf:=make([]byte,1024)
	res1.Read(buf)
	fmt.Println(res1)

	err2 :=os.Remove("astaxie")
	if err2!=nil{
		fmt.Println(err2)
	}
	os.RemoveAll("astaxie")
}
