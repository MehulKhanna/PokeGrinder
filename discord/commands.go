package discord

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"net/http"
	"os"
	"strconv"
	"time"
)

func Snowflake() int64 {
	snowflake := strconv.FormatInt((time.Now().UTC().UnixNano()/1000000)-1420070400000, 2) + "0000000000000000000000"
	nonce, _ := strconv.ParseInt(snowflake, 2, 64)

	return nonce
}

func SendCommand(
	session *discordgo.Session,
	channel *discordgo.Channel,
	command ApplicationCommand,
	options ...Options,
) {
	data := Interaction{
		Type:          2,
		ApplicationId: command.ApplicationId,
		GuildId:       channel.GuildID,
		ChannelId:     channel.ID,
		SessionId:     session.State.SessionID,
		Data: InteractionData{
			Version:            command.Version,
			Id:                 command.Id,
			Name:               command.Name,
			Type:               command.Type,
			Options:            options,
			ApplicationCommand: command,
			Attachments:        nil,
		},
		Nonce: strconv.FormatInt(Snowflake(), 10),
	}

	_, err := http.Get("http://127.0.0.1:8000/")
	if err != nil {
		fmt.Println("error while connecting to captcha solver API")
		os.Exit(69)
	}

	_, err = session.Request("POST", "https://discord.com/api/v9/interactions", data)
	if err != nil {
		fmt.Println(err)
	}
}

func ClickButton(
	session *discordgo.Session,
	message *discordgo.Message,
	button *discordgo.Button,
) {
	data := ButtonInteraction{
		Type:          3,
		Nonce:         strconv.FormatInt(Snowflake(), 10),
		GuildId:       message.GuildID,
		ChannelId:     message.ChannelID,
		MessageFlags:  int(message.Flags),
		MessageId:     message.ID,
		ApplicationId: message.Author.ID,
		SessionId:     session.State.SessionID,
		Data: struct {
			ComponentType int    `json:"component_type"`
			CustomId      string `json:"custom_id"`
		}{
			ComponentType: int(button.Type()),
			CustomId:      button.CustomID,
		},
	}

	_, err := session.Request("POST", "https://discord.com/api/v9/interactions", data)
	if err != nil {
		fmt.Println(err)
	}
}
