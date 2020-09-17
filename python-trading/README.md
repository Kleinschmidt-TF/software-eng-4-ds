### Python Trading Engine ###

The goal of this workshop is to devise a very basic trading engine.
The business analyst of a trading firm handed you the UML Diagram of the portfolio trading engine and asked you to deliver a quick prototype.
You also have a previsional architecture at hand, that you will build and anssemble progressively, brick by brick.

**TODO** : 
We will first focus on the Operation Layer alone. 
Write the code for the main classes with the right attributes and methods, and a main class that tests the engine.
You can chose to implement a minimalistic text-based interaction to get the user input, or go for a very simple web client or a python gui if you have the necessary skill and knowledge.

Classes that need to be implemented : 

- Asset
- Order
- Portfolio
- Exceptions

- A test class that reads a Daily Stock Price CSV file (you can get that directly though ***alphavantage.co*** API that we will be using later), and give the user the possibilitu to either Buy, Sell, or Pass, for every day in the dataset, while tracking his balance

### Hints for implementation ###

- Retrieve a daily price CSV file for a stock<br>
- Load it in a Pandas Dataframe<br>
- iterate over the CSV and send each daily price to the console or gui to give the user (trader) the opportunity to buy sell or pass.<br>
  (this will simulate a realtime stream.)
- Use DataFrame.iterrows to iterate over the CSV and iteratively fire the price for each day <br>
  it is a *generator* which yields both the index and row (as a Series):
  ```
  df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})

  for index, row in df.iterrows():
    print(row['c1'], row['c2'])
  ```
 - Use the provided code for a minimalistic console stub/example for managing user input & text-based interface <br>
   (**ask trainer for a demo and code**)
   
 - Do NOT forget to use **proper logging and debugging** as demo'ed by the trainer<br>
 
 - **Write Adequate Tests**. (No, That is not "optional"...)
   Do not forget to split the work : if one partners codes, the other writes the corresponding tests (simultaneously) , then alternate.
 
 - **Implement a Trading Log File** that keeps track of all performed operation<br>
   IRL this file is mandatory fo auditing the trading institution and is sent to regulation authorities.
   
### Pride Contest ###  

  - One or Two groups shall demo their trading interface and shall have the privilege of our gratitude and admiration.
  - All Projects shall be sent to the trainer and audited by the last day
  - The coolest programs win the following prizes : <br>
        - most clean & readable code<br>
        - most robust& well tested code<br>
        - most intuitive interface<br>
        - most humorous version (honour prize :-) )<br>
  
  ***You're Now On, PLACE YOUR BETS !*** 
   
 
