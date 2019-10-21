package main
import "fmt"
func main(){
	var t string
	fmt.Println(t)
	var arr  = []int{12,89,24,56,9,76,36}
	num:=len(arr)
	for i:=0;i<num ; i++ {
		for j:=0;j<num-1-i ; j++ {
			if (arr)[j] >(arr)[j+1]{
				arr[j],arr[j+1]=arr[j+1],arr[j]
			}
		}
	}
	fmt.Println(arr)
}
