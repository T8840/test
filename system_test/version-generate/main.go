package main

import (
	"log"

	"github.com/andmarios/go-versiongen"
)

func main() {
	versiongen.DirtyString = "+"
	versiongen.IgnoreFiles = []string{"version.go", "template_autogenerated.go"}
	err := versiongen.Create()
	if err != nil {
		log.Fatalln(err)
	}
}