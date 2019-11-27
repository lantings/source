package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"regexp"
	"strings"
)

func main() {
	baidu,err :=http.Get("http://www.baidu.com/")
	if err!=nil{
		log.Fatal(err)
		fmt.Println("http get error")
	}
	//fmt.Println(baidu)
	defer baidu.Body.Close()
	body,err:=ioutil.ReadAll(baidu.Body)
	if err!=nil{
		log.Fatal(err)
		fmt.Println("http read error")
		return
	}
	html:=string(body)
	//fmt.Println(html)
	re,_:=regexp.Compile("\\<[\\S\\s]+?\\>")
	html = re.ReplaceAllLiteralString(html,strings.ToLower(html))
	//fmt.Println(html)
	re,_=regexp.Compile("\\<style[\\S\\s]+?\\</style\\>")
	html = re.ReplaceAllLiteralString(html,"")
	//fmt.Println(html)
	re,_=regexp.Compile("\\<script[\\S\\s]+?\\</script\\>")
	html = re.ReplaceAllLiteralString(html,"")
	//fmt.Println(html)
	re,_=regexp.Compile("\\<[\\S\\s]+?\\>")
	html = re.ReplaceAllLiteralString(html,"\n")

	re,_=regexp.Compile("\\s{2,}")
	html = re.ReplaceAllLiteralString(html,"\n")

	html = strings.TrimSpace(html)
	fmt.Println(html)
}




