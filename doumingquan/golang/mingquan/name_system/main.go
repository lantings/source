package main

import (
	"fmt"
	"math/rand"
	"time"
)

var (
	family_names=[]string{"赵","钱","孙","李","周","吴","郑","王","冯","陈","褚","卫","蒋","沈","韩","杨","张","欧阳","诸葛","上官","司马","太史"}

	first_names=[]string{"金","木","水","火","土","春","夏","秋","冬","山","石","田","天","地","玄","黄","宇","宙","洪","荒"}

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
			generate_names[ln]=[]string{"飞","前","茂","百","方","书","生","无","一","用"}
		}else{
			generate_names["欧阳"] =[]string{"宗","的","永","其","光"}
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
	family_name := family_names[GetRandomInt(0,len(family_names)-1)]
	//fmt.Println(family_name)
	last_name := first_names[GetRandomInt(0,len(first_names)-1)]
	//fmt.Println(last_name)
	middle_name := generate_names[family_name][GetRandomInt(0,len(family_name)-1)]
	//fmt.Println(middle_name)
	return family_name + middle_name + last_name
}

