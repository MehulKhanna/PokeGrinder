# PokeGrinder V2
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.
Now in Golang for better handling of interactions.

## Supported Features
1. Hunting
- Encounters Pokémon and uses a ball depending on the rarity of the Pokémon.
- Stops if a captcha appears and automatically continues after the captcha is solved.

2. Fishing
- Spawns a fish, pulls the fishing rod and uses a ball depending on the rarity of the Pokémon.
- It has the data for every fish's rarity, so it knows the rarity even though Pokémeow doesn't show it.

3. Auto Buy Balls
- Buys balls automatically when you run out of them (works with both hunting and fishing)!
- Number of balls to buy can be specified in `config.json`.

4. Multiple Accounts
- You can run multiple accounts at once!

## Upcoming Features
1. Captcha Solver
- Captcha Solver may take some time since I have to collect data for the new and harder captcha.
The old captcha solver may work but with lower accuracy.

2. Logging Tables
- Format logs in tables for multiple accounts.

## Config
```json
{
    "Clients": [
        {
            "Token": "", // Your discord token
            "ChannelID": "", // Channel ID for hunting
            "FishChannelID": "", // Channel ID for fishing
            "Hunting": true, // Disable/Enable Hunting
            "Fishing": true, // Disable/Enable Fishing
            "Balls": {
                "Common": "pb",
                "Uncommon": "pb",
                "Rare": "gb",
                "Super Rare": "ub",
                "Legendary": "mb",
                "Shiny": "mb",
                "Shiny Event": "mb",
                "Shiny Full-odds": "prb"
            }, // Which ball to use for which rarity during hunting
            "FishBalls": {
                "Common": "pb",
                "Uncommon": "gb",
                "Rare": "ub",
                "Super Rare": "ub",
                "Legendary": "db",
                "Shiny": "mb",
                "Shiny Event": "mb",
                "Shiny Full-odds": "prb"
            }, // Which ball to use for which rarity during fishing
            "AutoBuy": {
                "pb": 50,
                "gb": 25,
                "ub": 5,
                "mb": 1
            } // How many balls to auto-buy when you have 0 left.
        }
        // You can add more clients after this with the same type of config as above
    ]
}
```
- Use different channels for each account.
- Hunting and fishing for different accounts can be in the same server.
- The Hunting and Fishing channels for the same account must be in different servers/guilds.

## Get Token ?

<strong>Run code (Discord Console - [Ctrl + Shift + I])</strong>

```js
window.webpackChunkdiscord_app.push([
  [Math.random()],
  {},
  req => {
    for (const m of Object.keys(req.c)
      .map(x => req.c[x].exports)
      .filter(x => x)) {
      if (m.default && m.default.getToken !== undefined) {
        return copy(m.default.getToken());
      }
      if (m.getToken !== undefined) {
        return copy(m.getToken());
      }
    }
  },
]);
console.log('%cWorked!', 'font-size: 50px');
console.log(`%cYou now have your token in the clipboard!`, 'font-size: 16px');
```

## Launching
- Download the `config.json` file and the `fishes.json` file.
- Download the executable file for your operating system from the release tab.
- The `config.json`, `fishes.json` and the executable must be in the same folder.
- Run the executable, and the grinder should start.

## Stopping
To stop the program simply close the command prompt or press CTRL+C in the command prompt.

## Disclaimer ⚠️
- This version of PokeGrinder doesn't solve captcha (yet).
- I am of course not responsible for any ban you receive for using this bot.
- Please keep an eye on the bot. Do not be irresponsible if you don't want to get banned.
- Please do not grind on public servers.
