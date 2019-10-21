package main

import "fmt"

var g = []int{25,63,77,55,12,29,55}
func main()  {
	//res:= len(g)
	g[5]+=10
	fmt.Println(g)
	//一维 数组
	var a [10]int
	for i:=0;i<10 ; i++ {
		a[i] =i+100
	}
	fmt.Println(a)
}
