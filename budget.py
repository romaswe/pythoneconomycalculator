import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Config
path = os.getenv('PATH_TO_FILES')
fileName = os.getenv('IMPORT_FILE_NAME')
fileSufix = os.getenv('FILE_SUFFIX')
moneyColumn = os.getenv('COLUMN_WITH_MONEY')
infoColum = os.getenv('COLUMN_WITH_INFO')
csvDelimiter = os.getenv('CSV_DELIMITER_SEPARATOR')
csvDecimal = os.getenv('CSV_DECIMAL_SEPARATOR')
myAccount = os.getenv('MY_SAVINGS_ACCOUNT_IDENTIFIER')
# End Config


def readCSV(fileName):
    print("Reading CSV file...")
    # Read CSV
    dataFrame = pd.read_csv(
        fileName, delimiter=csvDelimiter, decimal=csvDecimal)
    return dataFrame


def saveToCSV(dataFrame, fileName):
    # Save to CSV
    dataFrame.to_csv(fileName, sep=csvDelimiter,
                     index=False, decimal=csvDecimal)


def getExpenses(dataFrame):
    # Filter dataFrame for negative values
    expenses = dataFrame[dataFrame[moneyColumn] < 0]
    print("Expenses: " + str(calculateTotal(expenses)))
    return expenses


def getIncomes(dataFrame):
    # Filter dataFrame for positive values
    incomes = dataFrame[dataFrame[moneyColumn] > 0]
    return incomes


def calculateTotal(dataFrame):
    # Calculate total
    total = dataFrame[moneyColumn].sum()
    return total


def filterIncome(dataFrame, filter):
    # Filter dataFrame for positive values
    incomes = dataFrame[~dataFrame[infoColum].str.contains(filter)]
    print("Filtered income: " + str(calculateTotal(incomes)))
    return incomes


def calculateDiff(income, expenses):
    # Remove transfers from my own account
    filterdIncome = filterIncome(income, myAccount)
    diff = calculateTotal(filterdIncome) + calculateTotal(expenses)
    print("Diff: " + str(diff))
    return diff


def getXtraspar(expenses):
    # Get Xtraspar savings
    xtraspar = expenses[expenses[infoColum].str.contains('Xtraspar')]
    return xtraspar


def getAccountSavings(expenses):
    # Get Savings to my own account
    savings = expenses[expenses[infoColum].str.contains(myAccount)]
    return savings


def getAvanzaSavings(expenses):
    # Get Avanza savings
    avanzaSavings = expenses[expenses[infoColum].str.contains('AVANZA')]
    return avanzaSavings


def getAllSavings(expenses):
    # Get all savings
    xtraspar = getXtraspar(expenses)
    print("Xtraspar savings: " + str(abs(calculateTotal(xtraspar))))
    accountSavings = getAccountSavings(expenses)
    print("Account savings: " + str(abs(calculateTotal(accountSavings))))
    avanzaSavings = getAvanzaSavings(expenses)
    print("Avanza savings: " + str(abs(calculateTotal(avanzaSavings))))
    allSavings = pd.concat([xtraspar, accountSavings, avanzaSavings])
    saveToCSV(allSavings, path + fileName + "_allSavings" + fileSufix)
    return allSavings


def filterMySavingAccount(dataFrame):
    # Filter dataFrame for my savings account
    mySavingAccount = dataFrame[dataFrame[infoColum].str.contains(myAccount)]
    return mySavingAccount


def getSavingAccountDiff(income, expenses):
    # Get savings account diff
    savingAccountIncome = filterMySavingAccount(income)
    savingAccountExpenses = filterMySavingAccount(expenses)
    savingAccountDiff = calculateTotal(
        savingAccountIncome) + calculateTotal(savingAccountExpenses)
    print("Saving account diff: " + str(savingAccountDiff))
    return savingAccountDiff


if __name__ == "__main__":
    csvDataFrame = readCSV(path + fileName + fileSufix)
    incomes = getIncomes(csvDataFrame)
    expenses = getExpenses(csvDataFrame)

    saveToCSV(expenses, (path + fileName + '_expenses' + fileSufix))
    saveToCSV(incomes, (path + fileName + '_incomes' + fileSufix))

    calculateDiff(incomes, expenses)
    getAllSavings(expenses)
    getSavingAccountDiff(incomes, expenses)
