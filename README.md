# Citrea-Explorer-Summarizer
This small piece of code fetches the basic transaction data from Citrea Testnet via REST API and converts it to a human-readable summary.

Our first step was to locate API Docs and select the one that is fit for the job. For REST API, this was the URL: https://explorer.testnet.citrea.xyz/api-docs
Then, we found the GET endpoint that accepts a tx hash input and returns its whole underlying data. This was the URL for that: https://explorer.testnet.citrea.xyz/api/v2/transactions/
After defining the source of data, we started creating a basic Python code to:
  - Define the URL for fetching data
  - Define the TX Hash object that accepts user input
  - Define the Response object that returns a constructed URL call, combining the above URL with the given TX Hash
  - Create an if statement to: (We needed this if statement because we had to create an exit way for the situations in which we failed to fetch data)
      - Convert the JSON data from the constructed URL to a Python dictionary (I'm not sure why we had to do this)
      - Extract all relevant data from the defined dictionary by using necessary keys like "To", "From", "Timestamp", "Value"
      - Convert the default timestamp data into a more readable version (This part is a bit complicated for me)
      - Convert the VALUE data to its corresponding outlook with decimals
      - Assemble the final sentence by defining a summary object with f-strings

We used the following libraries for this project:
  - requests
  - json
  - datetime
