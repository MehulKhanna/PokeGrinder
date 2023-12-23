package instance

import (
	"encoding/json"
	"fmt"
	"github.com/bwmarrin/discordgo"
	"main/discord"
	"os"
	"slices"
	"strings"
	"time"
)

var Fishes map[string]string
var commandRetryCounterFish = 0

func init() {
	file, _ := os.ReadFile("fishes.json")
	err := json.Unmarshal(file, &Fishes)
	if err != nil {
		fmt.Println("error when unmarshalling fishes.json,", err)
		return
	}
}

func FishCommandSend(session *discordgo.Session, channel *discordgo.Channel) {
	client := Clients[session.Token]

	ch := make(chan *discordgo.MessageCreate)
	handler := func(session *discordgo.Session, message *discordgo.MessageCreate) {
		if !check(session, message, "fish spawn") {
			return
		}

		ch <- message
	}

	remove := session.AddHandler(handler)
	go discord.SendCommand(
		session,
		channel,
		client.CommandsFishChannel["fish"],
		client.CommandsFishChannel["fish"].Options[2],
	)

	time.AfterFunc(1500*time.Millisecond, func() {
		remove()
		ch <- nil
	})

	message := <-ch
	if message != nil || commandRetryCounter >= 5 {
		if commandRetryCounter >= 5 {
			commandRetryCounter = 0
		}

		return
	}

	FishCommandSend(session, channel)
	commandRetryCounterFish += 1
}

func FishSpawn(session *discordgo.Session, message *discordgo.MessageCreate) {
	client := Clients[session.Token]
	if !check(session, message, "fish spawn") {
		return
	}

	if strings.Contains(message.Content, "Please wait") {
		time.AfterFunc(500*time.Millisecond, func() {
			FishCommandSend(session, client.FishChannel)
		})

		return

	} else if strings.Contains(message.Embeds[0].Description, "captcha") {
		fmt.Println(fmt.Sprintf(
			"%s | A captcha appeared in the fishing channel!",
			session.State.User.Username,
		))

		ch := make(chan *discordgo.MessageUpdate)
		go WaitForSolve(93*time.Second, session, message, ch)
		update := <-ch

		if update == nil {
			fmt.Println(fmt.Sprintf(
				"%s | Timed out while waiting for the captcha to be solved!",
				session.State.User.Username,
			))
		} else {
			fmt.Println(fmt.Sprintf(
				"%s | The captcha has been solved!",
				session.State.User.Username,
			))

			time.AfterFunc(500*time.Millisecond, func() {
				FishCommandSend(session, client.FishChannel)
			})
		}

		return

	} else if !strings.Contains(message.Embeds[0].Description, "cast out an") {
		return
	}

	ch := make(chan *discordgo.MessageUpdate)
	go WaitForUpdate(20000*time.Millisecond, session, message, ch)

	update := <-ch
	if update == nil {
		fmt.Println(fmt.Sprintf(
			"%s | Timed out while waiting for the fish spawn to be updated.",
			session.State.User.Username,
		))

		return
	}

	if strings.Contains(update.Embeds[0].Description, "Not even a nibble...") {
		time.AfterFunc(23*time.Second, func() {
			FishCommandSend(session, client.FishChannel)
		})

		return
	}

	ch = make(chan *discordgo.MessageUpdate)
	go WaitForUpdate(2000*time.Millisecond, session, message, ch)
	go discord.ClickButton(
		session,
		update.Message,
		message.Components[0].(*discordgo.ActionsRow).Components[0].(*discordgo.Button),
	)

	update = <-ch
	if update == nil {
		fmt.Println(fmt.Sprintf(
			"%s | Timed out while waiting for the fish spawn to be updated 2.",
			session.State.User.Username,
		))
	}

	if !strings.Contains(update.Embeds[0].Description, "fished out a wild") {
		time.AfterFunc(23*time.Second, func() {
			FishCommandSend(session, client.FishChannel)
		})

		return
	}

	var order []string
	ballsPriority := []string{"db", "mb", "prb", "ub", "gb", "pb"}
	rarity := Fishes[strings.Split(update.Embeds[0].Description, "**")[3]]
	order = ballsPriority[slices.Index(ballsPriority, client.FishBalls[rarity]):]

	var button *discordgo.Button
	actionRow := message.Components[0].(*discordgo.ActionsRow).Components
	for _, ball := range order {
		for _, element := range actionRow {
			if element.(*discordgo.Button).CustomID == ball+"_fish" {
				button = element.(*discordgo.Button)
				break
			}
		}

		if button != nil {
			break
		}
	}

	ch = make(chan *discordgo.MessageUpdate)
	go WaitForUpdate(10*time.Second, session, message, ch)
	if button != nil {
		discord.ClickButton(session, message.Message, button)
	}

	update = <-ch
	time.AfterFunc(23*time.Second, func() {
		FishCommandSend(session, client.FishChannel)
	})

	if update != nil {
		if strings.Contains(update.Embeds[0].Description, "caught") {
			client.FishCatches += 1
		}

		if !client.AutoBuyLock {
			for index, sub := range []string{
				"Pokeballs : 0",
				"Greatballs: 0",
				"Ultraballs: 0",
				"Masterballs: 0",
			} {
				amount := client.AutoBuy[[]string{"pb", "gb", "ub", "mb"}[index]]
				if strings.Contains(update.Embeds[0].Footer.Text, sub) && amount > 0 {
					client.AutoBuyLock = true
					go func() {
						time.Sleep(2000 * time.Millisecond)
						_, err := session.ChannelMessageSend(
							message.ChannelID,
							fmt.Sprintf(";s b %d %d", index+1, amount),
						)

						if err != nil {
							fmt.Println(session.State.User.Username, "error while buying balls,", err)
						}

						client.AutoBuyLock = false
					}()
					break
				}
			}
		}
	}

	fmt.Println(fmt.Sprintf(
		"%s | Encounters: %d | Catches: %d | Fish Catches: %d",
		session.State.User.Username, client.Encounters, client.Catches,
		client.FishCatches,
	))

	return
}
