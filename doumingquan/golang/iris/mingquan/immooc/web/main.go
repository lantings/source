package main

import (
	"github.com/kataras/iris"
)

func main() {
	app := iris.Default()
	app.Use(myMiddleware)

	app.Handle("GET", "/ping", func(ctx iris.Context) {
		ctx.JSON(iris.Map{"message": "pong"})
	})
	app.Handle("GET","/", func(ctx iris.Context) {
		ctx.HTML("<h1>welcome to golang framework iris</h1>")
	})
	app.ConfigureHost(func(h *iris.Supervisor) {
		h.RegisterOnShutdown(func() {
			println("server terminated")
		})
	})
	// Listens and serves incoming http requests
	// on http://localhost:8080.
	app.Run(iris.Addr(":8080"))
}

func myMiddleware(ctx iris.Context) {
	ctx.Application().Logger().Infof("Runs before %s", ctx.Path())
	ctx.Next()
}
