package main
import "fmt"
//打印99乘法口诀
func main(){
	fmt.Println("this is very important")
	//for i:=1;i<=9;i++ {
	//	for j:=1;j<=i;j++ {
	//	  fmt.Printf("%d*%d=%d ",j,i,j*i)
	//	}
	//	 fmt.Println(" ")
	//}
	for i:=1; i<=9;i++  {
		for j:=1;j<=i ;j++  {
			fmt.Printf("%d*%d=%d ",j,i,j*i)
		}
		fmt.Println(" ")
	}
}