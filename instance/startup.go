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
	Token         string            `json:"Token"`
	ChannelID     string            `json:"ChannelID"`
	FishChannelID string            `json:"FishChannelID"`
	Hunting       bool              `json:"Hunting"`
	Fishing       bool              `json:"Fishing"`
	Balls         map[string]string `json:"Balls"`
	FishBalls     map[string]string `json:"FishBalls"`
	AutoBuy       map[string]int    `json:"AutoBuy"`

	Catches             int
	Encounters          int
	FishCatches         int
	AutoBuyLock         bool
	StartTime           time.Time
	Session             *discordgo.Session
	Channel             *discordgo.Channel
	FishChannel         *discordgo.Channel
	Commands            map[string]discord.ApplicationCommand
	CommandsFishChannel map[string]discord.ApplicationCommand
}

var Clients = map[string]*Client{}

func getCommands(session *discordgo.Session, channel *discordgo.Channel) map[string]discord.ApplicationCommand {
	var ApplicationCommandIndex discord.ApplicationCommandIndex
	response, err := session.Request(
		"GET",
		fmt.Sprintf(
			"https://discord.com/api/v9/guilds/%s/application-command-index",
			channel.GuildID,
		),
		nil,
	)

	err = json.Unmarshal(response, &ApplicationCommandIndex)
	if err != nil {
		fmt.Println(session.State.User.Username, "error while unmarshalling application command index,", err)
		return nil
	}

	commands := map[string]discord.ApplicationCommand{}
	for _, command := range ApplicationCommandIndex.ApplicationCommands {
		commands[command.Name] = command
	}

	return commands
}

func StartSession(client Client, group *sync.WaitGroup) {
	session, err := discordgo.New(client.Token)
	if err != nil {
		fmt.Println(client.Token, "error while creating session,", err)
		return

	}

	session.Identify.Intents |= discordgo.IntentMessageContent

	err = session.Open()
	if err != nil {
		fmt.Println(client.Token, "error while opening connection,", err)
		return
	}

	client.Session = session
	client.StartTime = time.Now()
	Clients[session.Token] = &client
	session.State.MaxMessageCount = 1000
	client.Encounters, client.Catches = 0, 0
	session.AddHandler(CaptchaMessage)
	session.AddHandler(CaptchaMessageUpdate)

	if client.Fishing {
		session.AddHandler(FishSpawn)
		client.FishChannel, err = session.Channel(client.FishChannelID)
		if err != nil {
			fmt.Println(session.State.User.Username, "error while finding fishing channel,", err)
			return
		}

		client.CommandsFishChannel = getCommands(session, client.FishChannel)
		go FishCommandSend(session, client.FishChannel)
	}

	if client.Hunting {
		session.AddHandler(PokemonMessage)
		client.Channel, err = session.Channel(client.ChannelID)
		if err != nil {
			fmt.Println(session.State.User.Username, "error while finding channel,", err)
			return
		}

		client.Commands = getCommands(session, client.Channel)
		go PokemonCommandSend(session, client.Channel)
	}

	fmt.Println(session.State.User, "has started grinding!")
	group.Done()
}
