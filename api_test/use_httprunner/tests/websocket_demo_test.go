package tests

import (
   "testing"

   "github.com/httprunner/httprunner/v4/hrp"
)

func TestWebSocketProtocol(t *testing.T) {
   testcase := &hrp.TestCase{
      Config: hrp.NewConfig("run request with WebSocket protocol").
         SetBaseURL("ws://echo.websocket.events").
         WithVariables(map[string]interface{}{
            "n":    5,
            "a":    12.3,
            "b":    3.45,
            "file": "./demo_file_load_ws_message.txt",
         }),
      TestSteps: []hrp.IStep{
         hrp.NewStep("open connection").
            WebSocket().
            OpenConnection("/").
            WithHeaders(map[string]string{"User-Agent": "HttpRunnerPlus"}).
            Validate().
            AssertEqual("status_code", 101, "check open status code").
            AssertEqual("headers.Connection", "Upgrade", "check headers"),
         hrp.NewStep("ping pong test").
            WebSocket().
            PingPong("/").
            WithTimeout(5000),
         hrp.NewStep("read sponsor info").
            WebSocket().
            Read("/").
            WithTimeout(5000).
            Validate().
            AssertContains("body", "Lob.com", "check sponsor message"),
         hrp.NewStep("write json").
            WebSocket().
            Write("/").
            WithTextMessage(map[string]interface{}{"foo1": "${gen_random_string($n)}", "foo2": "${max($a, $b)}"}),
         hrp.NewStep("read json").
            WebSocket().
            Read("/").
            Extract().
            WithJmesPath("body.foo1", "varFoo1").
            Validate().
            AssertLengthEqual("body.foo1", 5, "check json foo1").
            AssertEqual("body.foo2", 12.3, "check json foo2"),
         hrp.NewStep("write and read text").
            WebSocket().
            WriteAndRead("/").
            WithTextMessage("$varFoo1").
            Validate().
            AssertLengthEqual("body", 5, "check length equal"),
         hrp.NewStep("write and read binary file").
            WebSocket().
            WriteAndRead("/").
            WithBinaryMessage("${load_ws_message($file)}"),
         hrp.NewStep("write something redundant").
            WebSocket().
            Write("/").
            WithTextMessage("have a nice day!"),
         hrp.NewStep("write something redundant").
            WebSocket().
            Write("/").
            WithTextMessage("balabala ..."),
         hrp.NewStep("close connection").
            WebSocket().
            CloseConnection("/").
            WithTimeout(30000).
            WithCloseStatus(1000).
            Validate().
            AssertEqual("status_code", 1000, "check close status code"),
      },
   }

   // run testcase
   var err = hrp.NewRunner(t).Run(testcase)
   if err != nil {
      t.Fatalf("run testcase error: %v", err)
   }
}