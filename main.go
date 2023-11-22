package main

import (
	"encoding/json"
	"fmt"
	"main/instance"
	"os"
	"os/signal"
	"sync"
	"syscall"
)

type Config struct {
	Clients []instance.Client `json:"Clients"`
}

var config Config

func init() {
	configFile, _ := os.ReadFile("config.json")
	err := json.Unmarshal(configFile, &config)
	if err != nil {
		fmt.Println("error when unmarshalling config,", err)
		return
	}
}

func main() {
	fmt.Println("Starting sessions...")

	var group sync.WaitGroup
	for _, client := range config.Clients {
		if client.Fishing || client.Hunting {
			group.Add(1)
			go instance.StartSession(client, &group)
		}
	}

	group.Wait()
	fmt.Println("PokeGrinder is running, press CTRL+C to exit!")

	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc

	for _, client := range instance.Clients {
		client := client
		group.Add(1)
		go func() {
			err := client.Session.Close()
			if err != nil {
				fmt.Println(
					client.Session.State.User.Username,
					"error while closing session,", err,
				)
			}
			group.Done()
		}()
	}
	group.Wait()
}
