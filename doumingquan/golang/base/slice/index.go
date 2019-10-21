package main

import (
   "fmt"
   "unsafe"
)

func main(){
//make定义长度为3的数组***默认值是3个nil***
var numbers = make([]int,6,6)
arr:=[10]int{1,2,3,4,5,6,7,8,9,10}
test:= arr[1:5:7]
println("test=",test)
println("test length=",len(test))
println("test caps=",cap(test))
println("test unsafe.size=",unsafe.Sizeof(test))

//赋值
numbers = []int{4,24,99,46,29,55}
//定义并赋值
letters := []string{"a", "b", "c", "d"}
//对数组进行追加
a:= append(numbers, 1, 2, 3,5,8,13)
letters = append(letters,"f","mingquan","redis")

lets := []string{"test", "edu", "cn", "slice"}
//合并
lets = append(letters,lets...)

 /* 打印子切片从索引 2(包含) 到索引 5(不包含) */
number3 := numbers[2:5]
   printInt(numbers)
   fmt.Println("numbers[1:4] ==", numbers[1:4])
   fmt.Println("numbers[2:5] ==", number3)
   printSlice(letters)
   printInt(a)
   printSlice(lets)
   
}


func printSlice(x []string){
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}

func printInt(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}