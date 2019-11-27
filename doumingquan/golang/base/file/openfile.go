package main

import (
	"fmt"
	"log"
	"os"
)

func main(){
	userfile :="mingquan.txt"
	ming,err :=os.Create(userfile)
	if err!=nil{
		fmt.Println(ming,err)
		//return
	}

	//filepath := "D:/phpStudy/WWW/test/index.php"
	filepath:=userfile
	fmt.Println(filepath)
	file,err :=os.OpenFile(filepath,os.O_RDWR,0666)
	if err!=nil{
		log.Fatal(err)
	}
	defer file.Close()
	//file.Close()
	bytes :=[]byte("测试golang的写入功能")
	bw,err :=file.Write(bytes)
	if err!=nil{
		log.Fatal(err)
	}
	log.Printf("wrote %d bytes",bw)
}
