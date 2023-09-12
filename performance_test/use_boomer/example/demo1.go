package main

import (
    "github.com/myzhan/boomer"
    "net/http"
    "time"
)

func visitWebsite() {
    start := time.Now()
    resp, err := http.Get("https://httpbin.org/")
	elapsed := time.Since(start)

    if err == nil && resp.StatusCode == 200 {
        boomer.RecordSuccess("http", "GET /", elapsed.Nanoseconds()/int64(time.Millisecond), int64(10))
    } else {
        boomer.RecordFailure("http", "GET /", elapsed.Nanoseconds()/int64(time.Millisecond), err.Error())
    }
}

func main() {
    task := &boomer.Task{
        Name:   "visitWebsite",
        Weight: 10,
        Fn:     visitWebsite,
    }

    boomer.Run(task)

}
