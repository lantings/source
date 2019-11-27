package main

import (
	"archive/zip"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strings"
)


func main() {
	zipFile := "‪‪C:\\Users\\Administrator\\Desktop\\AdminLTE-master.zip";
	dest := "C:/Users/Administrator/Desktop/AletMy";	

	err := DeCompress(zipFile, dest)

	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println("----success----")
	}

}


// 压缩文件
// files 文件数组，可以是不同 dir 下的文件或者 文件夹
// dest 压缩文件存放地址
func Compress(files []*os.File, dest string) error {
	d,_ := os.Create(dest)
	// 关闭文件资源
	defer d.Close()

	w := zip.NewWriter(d)
	defer w.Close()

	for _, file := range files {
		err := compress(file, "", w)
		if err != nil {
			return err
		}
	}

	return nil
}

func compress(file *os.File, prefix string, zw *zip.Writer) error {
	info, err := file.Stat()

	if err != nil {
		return err
	}

	if info.IsDir() {
		prefix = prefix + "/" + info.Name()
		fileInfos, err := file.Readdir(-1)

		if err != nil {
			return err
		}

		for _, fi := range fileInfos {
			f, err := os.Open(file.Name() + "/" + fi.Name())
			if err != nil {
				return err
			}

			err = compress(f, prefix, zw)
			if err != nil {
				return err
			}
		}
	} else {
		header, err := zip.FileInfoHeader(info)
		header.Name = prefix + "/" +header.Name
		if err != nil {
			return err
		}

		writer, err := zw.CreateHeader(header)
		if err != nil {
			return err
		}

		_, err = io.Copy(writer, file)
		file.Close()
		if err != nil {
			return err
		}

	}
	return nil
}

// 解压
func DeCompress(zipFile string, dest string) (err error) {
	// 目标文件夹不存在，则创建
	if _, err = os.Stat(dest); err != nil {
		if os.IsNotExist(err) {
			os.MkdirAll(dest, 0755)
		}
	}

	reader, err := zip.OpenReader(zipFile)
	if err != nil {
		fmt.Printf("读取 %s 异常\n", zipFile)
		return err
	}
	defer reader.Close()

	for _, file := range reader.File {
		// log.Println(file.Name)

		if file.FileInfo().IsDir() {
			err := os.MkdirAll(dest + "/" + file.Name, 0755)

			if err != nil {
				log.Println(err)
			}

			continue
		} else {
			err = os.MkdirAll(getDir(dest + "/" + file.Name), 0755)
			if err != nil {
				return err
			}
		}

		rc, err := file.Open()
		if err != nil {
			return err
		}
		defer rc.Close()

		filename := dest + "/" + file.Name
		 w, err := os.Create(filename)
		 if err != nil {
		 	return err
		 }
		 defer w.Close()

		 _, err = io.Copy(w, rc)
		 if err != nil {
		 	return err
		 }

	}

	return
}

func getDir(path string) string {
	return subString(path, 0, strings.LastIndex(path, "/"))
}

func subString(str string, start, end int) string {
	rs := []rune(str)
	length := len(rs)

	if start < 0 || start > length {
		panic("start is wrong")
	}

	if end < start || end >length {
		panic("end is wrong")
	}

	return string(rs[start:end])
}

func CompressZip(src , dest string) (err error) {
	f, err := ioutil.ReadDir(src)
	if err != nil {
		log.Println(err)
	}

	fzip, _ := os.Create(dest)
	w := zip.NewWriter(fzip)

	defer fzip.Close()
	defer w.Close()

	for _, file := range f {
		fw, _ := w.Create(file.Name())
		filecontent, err := ioutil.ReadFile(src + file.Name())

		if err != nil {
			log.Println(err)
		}

		_, err = fw.Write(filecontent)

		if err != nil {
			log.Println(err)
		}

		// log.Println(n)
	}

	return
}