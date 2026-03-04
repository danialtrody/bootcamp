from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from solution.business_logic.budget import Budget
from solution.business_logic.expense import Expense
from solution.business_logic.income import Income

MESSAGE = "message"

app = FastAPI()

budget = Budget()


@app.get("/income", status_code=HTTP_200_OK)
def get_all_income() -> list[Income]:
    return budget.income


@app.post("/income", status_code=HTTP_201_CREATED)
def add_income(income: Income) -> dict:
    try:
        budget.add_income(income)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)
    return {
        MESSAGE: f"Income '{income.description}' of ${income.amount} added successfully."
    }


@app.delete("/income/index/{index}", status_code=HTTP_200_OK)
def delete_income_by_index(index: int) -> dict:
    try:
        budget.remove_income(index)
    except IndexError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    return {MESSAGE: f"Income '{index}' removed successfully."}


@app.delete("/income/description/{description}", status_code=HTTP_200_OK)
def delete_income_by_description(description: str) -> dict:
    try:
        budget.remove_income(description)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    return {MESSAGE: f"Income '{description}' removed successfully."}


@app.get("/expense", status_code=HTTP_200_OK)
def get_all_expense() -> list[Expense]:
    return budget.expense


@app.post("/expense", status_code=HTTP_201_CREATED)
def add_expense(expense: Expense) -> dict:
    try:
        budget.add_expense(expense)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
    return {
        MESSAGE: f"Expense '{expense.description}' of ${expense.amount} added successfully."
    }


@app.delete("/expense/index/{index}", status_code=HTTP_200_OK)
def delete_expense_by_index(index: int) -> dict:
    try:
        budget.remove_expense(index)
    except IndexError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    return {MESSAGE: f"Expense '{index}' removed successfully."}


@app.delete("/expense/description/{description}", status_code=HTTP_200_OK)
def delete_expense_by_description(description: str) -> dict:
    try:
        budget.remove_expense(description)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(error))
    return {MESSAGE: f"Expense '{description}' removed successfully."}


@app.get("/summary", response_class=PlainTextResponse, status_code=HTTP_200_OK)
def get_summary() -> str:
    return budget.summary()


@app.delete("/clear", status_code=HTTP_200_OK)
def clear_all_data() -> dict:
    budget.clear_all()
    return {MESSAGE: "Budget Cleared successfully!"}
