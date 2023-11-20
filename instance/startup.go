package instance

import (
	"encoding/json"
	"fmt"
	"github.com/bwmarrin/discordgo"
	"main/discord"
	"sync"
	"time"
)

type Client struct {
	Token     string            `json:"Token"`
	ChannelID string            `json:"ChannelID"`
	Grind     bool              `json:"Grind"`
	Balls     map[string]string `json:"Balls"`
	AutoBuy   map[string]int    `json:"AutoBuy"`

	Catches    int
	Encounters int
	StartTime  time.Time
	Session    *discordgo.Session
	Channel    *discordgo.Channel
	Commands   map[string]discord.ApplicationCommand
}

var Clients = map[string]*Client{}

func StartSession(client Client, group *sync.WaitGroup) {
	session, err := discordgo.New(client.Token)
	if err != nil {
		fmt.Println(client.Token, "error while creating session,", err)
		return
	}

	session.Identify.Intents |= discordgo.IntentMessageContent
	session.AddHandler(PokemonMessage)

	err = session.Open()
	if err != nil {
		fmt.Println(client.Token, "error while opening connection,", err)
		return
	}

	session.State.MaxMessageCount = 100
	client.Channel, err = session.Channel(client.ChannelID)
	if err != nil {
		fmt.Println(session.State.User.Username, "error while finding channel,", err)
		return
	}

	var ApplicationCommandIndex discord.ApplicationCommandIndex
	response, err := session.Request(
		"GET",
		fmt.Sprintf(
			"https://discord.com/api/v9/guilds/%s/application-command-index",
			client.Channel.GuildID,
		),
		nil,
	)

	err = json.Unmarshal(response, &ApplicationCommandIndex)
	if err != nil {
		fmt.Println(session.State.User.Username, "error while unmarshalling application command index,", err)
		return
	}

	client.Commands = map[string]discord.ApplicationCommand{}
	for _, command := range ApplicationCommandIndex.ApplicationCommands {
		client.Commands[command.Name] = command
	}

	client.Session = session
	client.StartTime = time.Now()
	client.Encounters, client.Catches = 0, 0
	Clients[session.Token] = &client

	go PokemonCommandSend(session, client.Channel)
	fmt.Println(session.State.User, "has started grinding!")
	group.Done()
}
