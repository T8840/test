package main

import (
   "crypto/tls"
   "flag"
   "io"
   "io/ioutil"
   "log"
   "net/http"
   "strconv"
   "time"

   "github.com/myzhan/boomer"
)

var (
   client             *http.Client
   verbose            bool
   timeout            int
   postFile           string
   contentType        string
   disableCompression bool
   disableKeepalive   bool
)

func worker() {
   // 需要替换你的url
   request, err := http.NewRequest("GET", "https://httpbin.org/get", nil)
   if err != nil {
      log.Fatalf("%v\n", err)
   }

   request.Header.Set("Content-Type", contentType)

   startTime := time.Now()
   response, err := client.Do(request)
   elapsed := time.Since(startTime)

   if err != nil {
      log.Printf("%v\n", err)
      boomer.RecordFailure("http", "error", 0.0, err.Error())
   } else {
      boomer.RecordSuccess("http", strconv.Itoa(response.StatusCode),
         elapsed.Nanoseconds()/int64(time.Millisecond), response.ContentLength)

      if verbose {
         body, err := ioutil.ReadAll(response.Body)
         if err != nil {
            log.Printf("%v\n", err)
         } else {
            log.Printf("Status Code: %d\n", response.StatusCode)
            log.Println(string(body))
         }

      } else {
         io.Copy(ioutil.Discard, response.Body)
      }

      response.Body.Close()
   }
}

func main() {
   flag.IntVar(&timeout, "timeout", 10, "Seconds to max. wait for each response")
   flag.StringVar(&postFile, "post-file", "", "File containing data to POST. Remember also to set --content-type")
   flag.StringVar(&contentType, "content-type", "text/plain", "Content-type header")

   flag.BoolVar(&disableCompression, "disable-compression", false, "Disable compression")
   flag.BoolVar(&disableKeepalive, "disable-keepalive", false, "Disable keepalive")

   flag.BoolVar(&verbose, "verbose", false, "Print debug log")

   flag.Parse()

   log.Printf(`HTTP benchmark is running with these args:
	method: GET
	url: https://httpbin.org
	timeout: %d
	post-file: %s
	content-type: %s
	disable-compression: %t
	disable-keepalive: %t
	verbose: %t`, timeout, postFile, contentType, disableCompression, disableKeepalive, verbose)

   http.DefaultTransport.(*http.Transport).MaxIdleConnsPerHost = 2000
   tr := &http.Transport{
      TLSClientConfig: &tls.Config{
         InsecureSkipVerify: true,
      },
      MaxIdleConnsPerHost: 2000,
      DisableCompression:  disableCompression,
      DisableKeepAlives:   disableKeepalive,
   }
   client = &http.Client{
      Transport: tr,
      Timeout:   time.Duration(timeout) * time.Second,
   }

   task := &boomer.Task{
      Name:   "worker",
      Weight: 10,
      Fn:     worker,
   }

   boomer.Run(task)
}
