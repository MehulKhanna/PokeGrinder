package instance

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"main/discord"
	"slices"
	"strings"
	"time"
)

var commandRetryCounter = 0

func check(session *discordgo.Session, message *discordgo.MessageCreate, name string) bool {
	if message.Author.ID != "664508672713424926" ||
		message.Type != 20 {
		return false
	}

	if message.Interaction.User.ID != session.State.User.ID ||
		message.Interaction.Name != name {
		return false
	}

	return true
}

func WaitForUpdate(
	timeout time.Duration,
	session *discordgo.Session,
	message *discordgo.MessageCreate,
	ch chan *discordgo.MessageUpdate,
) {
	handler := func(session *discordgo.Session, update *discordgo.MessageUpdate) {
		if update.BeforeUpdate.ID == message.Message.ID {
			ch <- update
		}
	}

	remove := session.AddHandler(handler)
	time.AfterFunc(timeout, func() {
		remove()
		ch <- nil
	})
}

func WaitForSolve(
	timeout time.Duration,
	session *discordgo.Session,
	message *discordgo.MessageCreate,
	ch chan *discordgo.MessageUpdate,
) {
	handler := func(session *discordgo.Session, update *discordgo.MessageUpdate) {
		if update.BeforeUpdate.ID == message.Message.ID &&
			strings.Contains(message.Content, "continue playing") {
			ch <- update
		}
	}

	remove := session.AddHandler(handler)
	time.AfterFunc(timeout, func() {
		remove()
		ch <- nil
	})
}

func PokemonCommandSend(session *discordgo.Session, channel *discordgo.Channel) {
	client := Clients[session.Token]

	ch := make(chan *discordgo.MessageCreate)
	handler := func(session *discordgo.Session, message *discordgo.MessageCreate) {
		if !check(session, message, "pokemon") {
			return
		}

		ch <- message
	}

	remove := session.AddHandler(handler)
	go discord.SendCommand(session, channel, client.Commands["pokemon"])

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

	PokemonCommandSend(session, channel)
	commandRetryCounter += 1
}

func PokemonMessage(session *discordgo.Session, message *discordgo.MessageCreate) {
	client := Clients[session.Token]

	if !check(session, message, "pokemon") {
		return
	}
	err := session.State.MessageAdd(message.Message)
	if err != nil {
		fmt.Println(session.State.User.Username, "error while adding message to state,", err)
		return
	}

	if strings.Contains(message.Content, "Please wait") {
		time.AfterFunc(500*time.Millisecond, func() {
			PokemonCommandSend(session, client.Channel)
		})

		return
	} else if strings.Contains(message.Embeds[0].Description, "captcha") {
		fmt.Println(fmt.Sprintf(
			"%s | A captcha appeared!",
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
				PokemonCommandSend(session, client.Channel)
			})
		}

		return
	}

	client.Encounters += 1

	var order []string
	ballsPriority := []string{"mb", "db", "prb", "ub", "gb", "pb"}
	for rarity, ball := range client.Balls {
		if strings.Contains(message.Embeds[0].Footer.Text, rarity) {
			order = ballsPriority[slices.Index(ballsPriority, ball):]
		}
	}

	var button *discordgo.Button
	actionRow := message.Components[0].(*discordgo.ActionsRow).Components
	for _, ball := range order {
		for _, element := range actionRow {
			if element.(*discordgo.Button).CustomID == ball {
				button = element.(*discordgo.Button)
				break
			}
		}

		if button != nil {
			break
		}
	}

	ch := make(chan *discordgo.MessageUpdate)
	go WaitForUpdate(10*time.Second, session, message, ch)
	if button != nil {
		discord.ClickButton(session, message.Message, button)
	}

	update := <-ch
	time.AfterFunc(8500*time.Millisecond, func() {
		PokemonCommandSend(session, client.Channel)
	})

	if update != nil {
		if strings.Contains(update.Embeds[0].Description, "caught") {
			client.Catches += 1
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
