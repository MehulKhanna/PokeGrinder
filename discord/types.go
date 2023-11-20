package discord

type ButtonInteraction struct {
	Type          int    `json:"type"`
	Nonce         string `json:"nonce"`
	GuildId       string `json:"guild_id"`
	ChannelId     string `json:"channel_id"`
	MessageFlags  int    `json:"message_flags"`
	MessageId     string `json:"message_id"`
	ApplicationId string `json:"application_id"`
	SessionId     string `json:"session_id"`
	Data          struct {
		ComponentType int    `json:"component_type"`
		CustomId      string `json:"custom_id"`
	} `json:"data"`
}

type SelectOptionInteraction struct {
	Type          int    `json:"type"`
	Nonce         string `json:"nonce"`
	GuildId       string `json:"guild_id"`
	ChannelId     string `json:"channel_id"`
	MessageFlags  int    `json:"message_flags"`
	MessageId     string `json:"message_id"`
	ApplicationId string `json:"application_id"`
	SessionId     string `json:"session_id"`
	Data          struct {
		ComponentType int      `json:"component_type"`
		CustomId      string   `json:"custom_id"`
		Type          int      `json:"type"`
		Values        []string `json:"values"`
	} `json:"data"`
}

type Options struct {
	Type                 int         `json:"type"`
	Name                 string      `json:"name"`
	Value                interface{} `json:"value,omitempty"`
	Description          string      `json:"description"`
	DescriptionLocalized string      `json:"description_localized"`
	NameLocalized        string      `json:"name_localized"`
	Required             bool        `json:"required,omitempty"`
	MinValue             int         `json:"min_value,omitempty"`
	MaxValue             int         `json:"max_value,omitempty"`
	Options              []Options   `json:"options,omitempty"`
	Choices              []struct {
		Name  string `json:"name"`
		Value string `json:"value"`
	} `json:"choices,omitempty"`
}

type InteractionData struct {
	Version            string             `json:"version"`
	Id                 string             `json:"id"`
	Name               string             `json:"name"`
	Type               int                `json:"type"`
	Options            []Options          `json:"options"`
	ApplicationCommand ApplicationCommand `json:"application_command"`
	Attachments        []interface{}      `json:"attachments"`
}

type Interaction struct {
	Type          int             `json:"type"`
	ApplicationId string          `json:"application_id"`
	GuildId       string          `json:"guild_id"`
	ChannelId     string          `json:"channel_id"`
	SessionId     string          `json:"session_id"`
	Data          InteractionData `json:"data"`
	Nonce         string          `json:"nonce"`
}
type Application struct {
	Id          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Icon        string `json:"icon"`
	Bot         struct {
		Id                   string      `json:"id"`
		Username             string      `json:"username"`
		Discriminator        string      `json:"discriminator"`
		Bot                  bool        `json:"bot"`
		PublicFlags          int         `json:"public_flags"`
		Flags                int         `json:"flags"`
		GlobalName           interface{} `json:"global_name"`
		Avatar               string      `json:"avatar"`
		AccentColor          interface{} `json:"accent_color"`
		AvatarDecorationData interface{} `json:"avatar_decoration_data"`
		Banner               interface{} `json:"banner"`
		BannerColor          interface{} `json:"banner_color"`
	} `json:"bot"`
}

type ApplicationCommand struct {
	Id               string    `json:"id"`
	Type             int       `json:"type"`
	ApplicationId    string    `json:"application_id"`
	Version          string    `json:"version"`
	Name             string    `json:"name"`
	Description      string    `json:"description"`
	Options          []Options `json:"options,omitempty"`
	IntegrationTypes []int     `json:"integration_types"`
}

type ApplicationCommandIndex struct {
	Applications        []Application        `json:"applications"`
	ApplicationCommands []ApplicationCommand `json:"application_commands"`
	Version             string               `json:"version"`
}
