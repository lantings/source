package main

import (
	"fmt"
	"math/rand"
	"time"
)

var (
	family_names=[]string{"窦"}

	first_names=[]string{"春","夏","秋","冬","芳","菲","丽","君","媛","云","颖","燕","然"}

	generate_names = make(map[string][]string)

	name = make([]string,0)
)
func main(){
	for i:=0;i<100 ;i++  {
		name = append(name,GetRandomName())
	}
	fmt.Println(name)
}

func init(){

	for _,ln:=range family_names{
		if ln !="欧阳"{
			generate_names[ln]=[]string{"静","晓","红","美","思"}
		}else{
			//generate_names["欧阳"] =[]string{"宗","的","永","其","光"}
		}
	}
}

//生成随机数
func GetRandomInt(start,end int) int{
	<-time.After(1 * time.Nanosecond)
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	return start + r.Intn(end-start)
}

func GetRandomName()(name string){
	family_name := "窦"
	fmt.Println(family_name)
	last_name := first_names[GetRandomInt(0,len(first_names)-1)]
	//fmt.Println(last_name)
	middle_name := generate_names[family_name][GetRandomInt(0,len(family_name)-1)]
	//fmt.Println(middle_name)
	return family_name + middle_name + last_name
}

