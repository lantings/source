package main
// from:  https://www.jianshu.com/p/1227c5145cd8
import "fmt"

type Person struct {
	name string
	age int
}
type Student struct {
	Person
	id int
	score int
}

func main()  {
	person:=Person{"mike",18}
	person.showInfo()
	person.setAge(20)
	fmt.Println(person)

	student:=Student{Person{"mingquan",24},100,50}
	student.showInfo()
	student.read()
	fmt.Println(student)
}

func (person *Person) showInfo(){
	fmt.Printf("my name is %s,my age is %d",person.name,person.age)
}

func (person *Person) setAge(age int)  {
	person.age = age
}

func (student *Student) showInfo()  {
	fmt.Println("I am a good student")
}
func (student *Student) read(){
	fmt.Println("I am reading a book")
}
