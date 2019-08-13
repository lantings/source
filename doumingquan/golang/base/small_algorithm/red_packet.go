package main
import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    for i := 0; i < 10; i ++{
        redPackage(10, 600)
        fmt.Println("")
    }
}

// 随机红包
// remainCount: 剩余红包数
// remainMoney: 剩余红包金额（单位：分)
func randomMoney(remainCount, remainMoney int)int{
    if remainCount == 1{
        return remainMoney
    }

    rand.Seed(time.Now().UnixNano())

    var min = 1
    max := remainMoney / remainCount * 2
    money := rand.Intn(max) + min
    return money
}

// 发红包
// count: 红包数量
// money: 红包金额（单位：分)
func redPackage(count, money int)  {
    for i := 0; i < count; i++ {
        m := randomMoney(count - i, money)
        fmt.Printf("%d  ",  m)
        money -= m
    }
}