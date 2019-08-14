package main
import "fmt"
//var申明全局变量
var(
	    mingquan string
	    xiaojun  string
	)
func main(){
	fmt.Println("this is very important")
	f:="runoob"
	//var f string = "Runoob"
	fmt.Println(f)
	var t int
	s,t:=1,5
	fmt.Println(s,t)
    mingquan="mingquan"
    xiaojun="yaoxiaojun"
	fmt.Println(mingquan,xiaojun)

	//数据交换，数据类型要相同
	mingquan,xiaojun = xiaojun,mingquan
	fmt.Println(mingquan,xiaojun)

	//直接申明变量
	a, b, c:= 5, 7, "abc"
	fmt.Println(a,b,c)
}