package main
import(
	"fmt"
)
func main(){
	var a int = 20
	var b int = 30
	c:=10
	d:=20
	m:=float32(a)/float32(b)
	n:=float32(c)/float32(d)
	//n:=string(c)/string(d)
	fmt.Println(m,n)
}