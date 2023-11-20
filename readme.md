# PokeGrinder V2
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.
Now coded in Golang for better handling of interactions.

## Supported Features
1. Hunting
- Encounters Pokémon and uses a ball depending on the rarity of the Pokémon.
- Stops if a captcha appears and automatically continues after the captcha is solved.

2. Auto Buy Balls
- Buys balls automatically when you run out of them!
- Number of balls to buy can be specified in `config.json`.

## Upcoming Features
1. Fishing
2. Captcha Solver
- Captcha Solver may take some time since I have to collect data for the new and harder captcha.
The old captcha solver may work but with lower accuracy.

## Config
```json
{
    "Clients": [
        {
            "Token": "", // Your Discord token
            "ChannelID": "", // Discord channel id
            "Grind": true, // Whether to grind or not
            "Balls": {
                "Common": "pb",
                "Uncommon": "pb",
                "Rare": "gb",
                "Super Rare": "ub",
                "Legendary": "mb",
                "Shiny": "mb",
                "Shiny Event": "mb",
                "Shiny Full-odds": "prb"
            },
            "AutoBuy": {
                "pb": 50,
                "gb": 25,
                "ub": 5,
                "mb": 0
            } // Amount of balls to buy when 0 left
        }
        // You can add more clients after this
    ]
}
```

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
- Download the `config.json` file.
- Download the executable file from the release tab.
- The `config.json` and the executable must be in the same folder.
- Run the executable, and the grinder should start.

## Stopping
To stop the program simply close the command prompt or press CTRL+C in the command prompt.

## Disclaimer ⚠️
- This version of PokeGrinder doesn't solve captcha (yet).
- I am of course not responsible for any ban you receive for using this bot.
- Please keep an eye on the bot. Do not be irresponsible if you don't want to get banned.
- Please do not grind on public servers.
