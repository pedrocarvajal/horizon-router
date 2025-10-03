# Weekly Trading Account Report Generator

## Variables

Today is: {today}
Broker account number (`broker_account_number`) is: 3000085718


Use this reference to calculate the current week's date range (Monday to Sunday) for data analysis.

## Objective

Generate a weekly account performance report by analyzing trading data from snapshots and deals endpoints to create a Telegram community notification message.

## Required Analysis

### 1. Weekly Performance Calculation

- Calculate total profit/loss for the week from all deals
- Determine week opening vs closing balance from snapshots
- Calculate percentage change from initial balance

### 2. Trade Analysis

- Identify the deal with highest profit (best winner)
- Identify the deal with largest loss (worst loser)
- Count total number of trades executed
- Calculate win rate percentage

### 3. Account Status

- Current balance vs initial account balance
- Total accumulated profit/loss since account inception
- Weekly performance as percentage of account

## Output Format

Generate ONLY a natural, flowing Telegram message with this content:

```
This week from [start date] to [end date] we had a [positive/negative] performance with a total profit/loss of $[amount] representing [percentage]% change. We started the week with $[amount] and ended with $[amount]. Our best trade was $[amount] profit on [symbol] while our worst trade was $[amount] loss on [symbol]. In total we executed [number] trades this week. Our account now shows $[amount] with a total accumulated profit of $[amount] since inception, which represents [percentage]% growth overall.
```

## Message Tone Guidelines

- Professional but accessible
- Keep numbers clear and prominent
- End with informative closing
- No explanations or additional commentary
- Direct community notification style
- Feel free to paraphrase and rearrange the message structure to create natural variation
- Each report should sound unique while maintaining all essential information

## Calculation Requirements

- Weekly P&L = sum of all deal profits this week
- Balance change = latest snapshot balance - earliest snapshot balance
- Best trade = deal with highest profit value
- Worst trade = deal with lowest profit value (most negative)
- Total trades = count of all deals this week
- Round monetary values to 2 decimals
- Show percentages with 1 decimal

## Error Handling

- If no data available, return: "No sufficient data available to generate weekly report"
- If API errors occur, return: "Error accessing account data"

## Final Message Only

Return ONLY the formatted Telegram message. No explanations, instructions, or additional text.
