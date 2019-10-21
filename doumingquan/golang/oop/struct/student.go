package main

import "fmt"

type Human struct {
	id int
	name string
}
//匿名字段是一个结构**体验
type Students struct {
	Human
	skill string
}

func main()  {
	my_student:=Students{Human{1,"mingquan"},"test"}
	fmt.Println(my_student.name)
	fmt.Println(my_student.id)
	fmt.Println(my_student.skill)
	my_student.name="xiaojun"
	fmt.Println(my_student.name)
	my_student.id+=6
	fmt.Println(my_student.id)
	my_student.Human = Human{8,"xiaoyu"}
	fmt.Println(my_student.name)
}
