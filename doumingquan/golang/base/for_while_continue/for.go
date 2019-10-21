package main

import "fmt"

func main()  {
	//var b int =15
	//var a = 16
	fmt.Println("")
	number:=[6]int{1,2,3,4,5}
	//第一种种 种for循环的方式
	for i:=0;i<len(number) ; i++ {
		fmt.Println("a的值为",number[i])
	}
	//第二种for循环的方式
	for _,x:=range number{
		fmt.Printf("第%d位x的值是%d\n",x,x)
	}
}
