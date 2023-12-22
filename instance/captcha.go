package instance

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"
)

func CaptchaMessage(session *discordgo.Session, message *discordgo.MessageCreate) {
	if message.Author.ID != "664508672713424926" ||
		message.Type != 20 {
		return
	}

	if len(message.Embeds) == 0 {
		return
	}

	if message.Interaction.User.ID != session.State.User.ID ||
		!strings.Contains(message.Embeds[0].Description, "captcha") {
		return
	}

	_ = session.State.MessageAdd(message.Message)

	resp, err := http.Get("http://127.0.0.1:8000/solve/" + message.Embeds[0].Image.URL)
	if err != nil {
		fmt.Println("Unable to contact the solver API! Please solve the captcha yourself!")
		log.Fatalln(err)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	sb := string(body)
	_, err = session.ChannelMessageSend(message.ChannelID, strings.Split(sb, "\"")[3])
	if err != nil {
		fmt.Println("Couldn't send captcha answer!")
		return
	}
}

func CaptchaMessageUpdate(session *discordgo.Session, message *discordgo.MessageUpdate) {
	if message.Author == nil {
		return
	}

	if message.Author.ID != "664508672713424926" ||
		message.Type != 20 {
		return
	}

	if len(message.Embeds) == 0 {
		return
	}

	if message.Interaction.User.ID != session.State.User.ID ||
		!strings.Contains(message.Embeds[0].Description, "captcha") {
		return
	}

	retriesLeft, err := strconv.Atoi(strings.Split(message.Embeds[0].Description, "**")[5])
	if err != nil {
		fmt.Println("Error getting retries left")
	} else {
		if retriesLeft == 1 {
			return
		}
	}

	_ = session.State.MessageAdd(message.Message)

	resp, err := http.Get("http://127.0.0.1:8000/solve/" + message.Embeds[0].Image.URL)
	if err != nil {
		fmt.Println("Unable to contact the solver API! Please solve the captcha yourself!")
		log.Fatalln(err)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	sb := string(body)
	_, err = session.ChannelMessageSend(message.ChannelID, strings.Split(sb, "\"")[3])
	if err != nil {
		fmt.Println("Couldn't send captcha answer!")
		return
	}
}
