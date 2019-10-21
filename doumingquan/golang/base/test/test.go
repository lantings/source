package main

//func main()  {
//	for i:=0;i<10;i++{
//
//	}
//	fmt.Println("sum:", 1)
//
//}

import "fmt"

func main(){
	//for i:=1; i<10;i++  {
	//	for j:=1;j<=i ;j++  {
	//		//fmt.Printf("%d*%d=%d ",j,i,j*i)
	//	}
	//	fmt.Println("")
	//}
	//冒泡法
	arr:=[]int{10,88,56,94,77,22,89}
	length:=len(arr)
	for i:=0;i<length;i++{
		for j:=0;j<length-1-i;j++{
			if (arr)[j]>(arr)[j+1] {
				arr[j],arr[j+1]=arr[j+1],arr[j]
			}
		}
	}
	fmt.Println(arr)
}






